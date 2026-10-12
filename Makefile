# OWNER: SHARED
# PURPOSE:
# Command targets/scripts as comments/placeholders only.
#
# Expected future commands:
# make start
# make stop
# make test
# make demo
# make experiments
# make clean

# --- Unikraft Cloud (single "core" instance, see main.py / Kraftfile) ---
# Usage: make uk-build ORG=<your-org> && make uk-volume && make uk-run ORG=<your-org>
ORG   ?= $(error set ORG=<your unikraft org>)
METRO ?= fra
IMAGE  = $(ORG)/market-core:latest

uk-build:
	unikraft build . --output $(IMAGE)

uk-volume:  # once: SQLite lives here, the EROFS rootfs is read-only
	unikraft volume create --metro $(METRO) --name market-data --size 1G

# No scale-to-zero: the generator/processor thread must keep running.
# Add -e CLICKHOUSE_HOST=... to use ClickHouse instead of SQLite.
uk-run:
	unikraft run --metro $(METRO) --name market-core \
	  -p 443:8080/tls+http -m 512M \
	  --volume market-data:/data \
	  -e GENERATOR_EVENT_RATE=50 -e DEBUG=false \
	  --image $(IMAGE)

uk-logs:
	unikraft instances logs market-core

.PHONY: uk-build uk-volume uk-run uk-logs
