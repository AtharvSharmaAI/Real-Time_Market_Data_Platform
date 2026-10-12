# Setup and Execution Guide

This document describes how to start, test, and demonstrate the Real-Time Market Data Platform.

## Prerequisites
- Docker & Docker Compose
- Python 3.10+
- `uv` package manager (optional, but recommended)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/user/Real-Time_Market_Data_Platform.git
   cd Real-Time_Market_Data_Platform
   ```

2. Initialize virtual environment and dependencies:
   ```bash
   uv venv
   source .venv/bin/activate
   uv pip install -r pyproject.toml
   ```

## Starting the Platform

`docker-compose.yml` is still a skeleton, so `start.sh` runs the generator, processor and API as local processes (logs: `generator.log`, `processor.log`, `api.log`). It switches to `docker compose up` automatically once the compose file defines services.
```bash
./scripts/start.sh            # add --local to force local processes
```
Without Kafka and ClickHouse the pipeline runs in simulation mode, and the API serves mock rows (see `docs/api.md`).

### Frontend
```bash
cd frontend && npm ci && npx vite --host 0.0.0.0 --port 3000
```
Open http://localhost:3000. `/api/*` is proxied to the API on :8000.

### Prometheus and Grafana
These run in Docker with the configs in `monitoring/`. The `--add-host` flags point the scrape targets `processor:8001` and `api:8000` at the local processes.
```bash
M=$PWD/monitoring
docker network create market-monitoring
docker run -d --name prometheus --network market-monitoring -p 9090:9090 \
  --add-host processor:host-gateway --add-host api:host-gateway --add-host connect:host-gateway \
  -v $M/prometheus/prometheus.yml:/etc/prometheus/prometheus.yml:ro \
  -v $M/alerts/alerts.yml:/etc/prometheus/alerts.yml:ro \
  prom/prometheus:v3.1.0
docker run -d --name grafana --network market-monitoring -p 3001:3000 \
  -e GF_AUTH_ANONYMOUS_ENABLED=true -e GF_AUTH_ANONYMOUS_ORG_ROLE=Viewer \
  -v $M/grafana/provisioning/datasources:/etc/grafana/provisioning/datasources:ro \
  -v $M/grafana/provisioning/dashboards/dashboard.yml:/etc/grafana/provisioning/dashboards/dashboard.yml:ro \
  -v $M/grafana/dashboards:/var/lib/grafana/dashboards:ro \
  grafana/grafana:11.4.0
```
- Prometheus: http://localhost:9090 (targets at `/targets`)
- Grafana: http://localhost:3001 (admin/admin). The dashboards are provisioned from `monitoring/grafana/dashboards/`.

All routes and ports are listed in [`docs/api.md`](api.md).

## Stopping the Platform

To terminate all services and background processes:
```bash
./scripts/stop.sh
docker rm -f prometheus grafana   # if started
```
Stop the Vite server with Ctrl+C. Don't run `start.sh` twice without `stop.sh` in between: the PID file is overwritten and the old processes keep holding their ports.

## Running Tests

To run the unified pytest suite across all modules:
```bash
./scripts/run_tests.sh
```

## Running Chaos Experiments

To launch the automated chaos scenarios:
```bash
./scripts/run_experiments.sh
```

## Running the End-to-End Demo

To execute a complete pipeline run:
```bash
./scripts/run_demo.sh
```