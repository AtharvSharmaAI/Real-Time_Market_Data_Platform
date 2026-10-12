# Unikraft Cloud image: single "core" instance (see main.py). Build with `make uk-build`.

FROM node:22-bookworm AS frontend
WORKDIR /frontend
COPY frontend/package.json frontend/package-lock.json ./
RUN npm ci
COPY frontend/ ./
RUN npm run build

FROM python:3.13-bookworm AS build
RUN pip install --no-cache-dir "fastapi>=0.110" "uvicorn>=0.28" "pydantic>=2" "clickhouse-connect>=0.7"
WORKDIR /app
COPY main.py ./
COPY api/app api/app
COPY generator/src generator/src
COPY generator/faults generator/faults
COPY processor processor
RUN rm -rf processor/tests
COPY --from=frontend /frontend/dist frontend/dist

# Drop runtime-irrelevant stdlib parts (test suite, GUI, installers)
RUN cd /usr/local/lib/python3.13 && \
    rm -rf test idlelib tkinter turtledemo ensurepip lib-dynload/_tkinter* site-packages/pip* && \
    find /usr/local/lib -name __pycache__ -prune -exec rm -rf {} + && \
    python3 -m compileall -q /usr/local/lib/python3.13 /app

# Collect every shared lib python + compiled wheels need (ldd closure), keeping paths
RUN mkdir /rootlibs && \
    find /usr/local/bin/python3 /usr/local/lib -type f -name '*.so*' -o -path /usr/local/bin/python3 \
      | xargs ldd 2>/dev/null \
      | awk '$2 == "=>" && $3 ~ /^\// {print $3} $1 ~ /ld-linux/ {print $1}' | sort -u \
      | xargs -I{} cp --parents -L {} /rootlibs/ && \
    cp --parents /etc/ld.so.cache /rootlibs/

# Slim rootfs, same shape as unikraft-cloud/examples httpserver-python3.12-fastapi
FROM scratch
COPY --from=build /rootlibs /
COPY --from=build /usr/local/lib /usr/local/lib
COPY --from=build /usr/local/bin/python3 /usr/bin/python3
COPY --from=build /app /app

ENV PYTHONPATH=/app \
    PYTHONUNBUFFERED=1 \
    SQLITE_PATH=/data/market.db
