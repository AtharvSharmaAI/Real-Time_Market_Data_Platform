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

### Docker Mode (Default)
To run the full multi-service architecture including Kafka, Kafka Connect, ClickHouse, Prometheus, and Grafana:
```bash
./scripts/start.sh
```

### Local Process Simulation Mode
If Docker is not running/available, or if you explicitly want to bypass Docker, run the start script with the `--local` flag:
```bash
./scripts/start.sh --local
```

## Stopping the Platform

To terminate all services and background processes:
```bash
./scripts/stop.sh
```

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