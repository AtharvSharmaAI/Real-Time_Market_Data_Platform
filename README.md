# real-time-market-platform

## Objective
Build a local, reproducible real-time market-data streaming platform.

## Architecture
Local Market Data
        |
        v
Generator / Replay / Fault Injection
        |
        v
Kafka
        |
        v
Stream Processor
        |
        +--> Validation
        +--> DLQ
        +--> Deduplication
        +--> Event-time processing
        +--> Watermark
        +--> 5-second windows
        +--> VWAP
        +--> Volatility
        +--> Anomaly detection
        |
        v
processed-events
        |
        v
Kafka Connect
        |
        v
ClickHouse
        |
        +--> FastAPI
        |
        +--> Frontend

Prometheus -> Grafana
Chaos Experiments -> Evaluation -> Resilience Report

## Team Ownership
Person 1: INGESTION + KAFKA
Person 2: STREAM PROCESSING + ANOMALY DETECTION
Person 3: CLICKHOUSE + KAFKA CONNECT + FASTAPI + FRONTEND
Person 4: OBSERVABILITY + CHAOS + EVALUATION
Shared: Docker Compose, documentation, integration, code review, final demo

## Setup Placeholder
Setup instructions will go here.

## Weekly Tracker & Status

| Task | Owner | Status | Deadline/week | Dependency | Deliverable |
| --- | --- | --- | --- | --- | --- |
| Kafka setup | P1 | ✅ COMPLETED | WEEK 1 | None | Kafka running |
| processor skeleton + data contract | P2 | ✅ COMPLETED | WEEK 1 | None | Skeleton |
| ClickHouse setup | P3 | ✅ COMPLETED | WEEK 1 | None | ClickHouse running |
| Prometheus/Grafana setup | P4 | ✅ COMPLETED | WEEK 1 | None | Dashboards |
| generator/replay | P1 | ✅ COMPLETED | WEEK 2 | Kafka | Event generator |
| Kafka consumer | P2 | ✅ COMPLETED | WEEK 2 | Processor skeleton | Data ingestion |
| Kafka->ClickHouse prototype | P3 | ✅ COMPLETED | WEEK 2 | ClickHouse | Pipeline |
| basic metrics | P4 | ✅ COMPLETED | WEEK 2 | Prometheus | Dashboards |
| malformed-data generation | P1 | ✅ COMPLETED | WEEK 3 | Generator | Corrupt data |
| validation + DLQ | P2 | ✅ COMPLETED | WEEK 3 | Consumer | Validator |
| DLQ storage | P3 | ✅ COMPLETED | WEEK 3 | ClickHouse | Storage tables |
| DLQ dashboard | P4 | ✅ COMPLETED | WEEK 3 | Grafana | Dashboards |
| duplicate generation | P1 | ✅ COMPLETED | WEEK 4 | Generator | Duplicates |
| deduplication + VWAP | P2 | ✅ COMPLETED | WEEK 4 | Validation | VWAP |
| VWAP storage | P3 | ✅ COMPLETED | WEEK 4 | ClickHouse | Storage tables |
| duplicate metrics | P4 | ✅ COMPLETED | WEEK 4 | Prometheus | Dashboards |
| out-of-order generator | P1 | ✅ COMPLETED | WEEK 5 | Generator | Out-of-order |
| event-time + windows | P2 | ✅ COMPLETED | WEEK 5 | Deduplication | Windows |
| window queries | P3 | ✅ COMPLETED | WEEK 5 | ClickHouse | Queries |
| latency metrics | P4 | ✅ COMPLETED | WEEK 5 | Prometheus | Dashboards |
| late events | P1 | ✅ COMPLETED | WEEK 6 | Generator | Late data |
| watermark + lateness | P2 | ✅ COMPLETED | WEEK 6 | Event-time | Watermarks |
| late-event storage | P3 | ✅ COMPLETED | WEEK 6 | ClickHouse | Storage |
| lateness metrics | P4 | ✅ COMPLETED | WEEK 6 | Prometheus | Dashboards |
| stable replay | P1 | ✅ COMPLETED | WEEK 7 | Generator | Replay |
| volatility | P2 | ✅ COMPLETED | WEEK 7 | Windows | Volatility |
| Kafka Connect + FastAPI | P3 | ✅ COMPLETED | WEEK 7 | Connect | API |
| complete monitoring | P4 | ✅ COMPLETED | WEEK 7 | Prometheus | Complete set |
| anomaly injection | P1 | ✅ COMPLETED | WEEK 8 | Generator | Anomalies |
| anomaly detector | P2 | ✅ COMPLETED | WEEK 8 | Volatility | Detector |
| anomaly storage/API | P3 | ✅ COMPLETED | WEEK 8 | ClickHouse | API |
| anomaly dashboard | P4 | ✅ COMPLETED | WEEK 8 | Grafana | Dashboards |
| reproducible chaos inputs | P1 | ✅ COMPLETED | WEEK 9 | Generator | Chaos |
| correctness under failure | P2 | ✅ COMPLETED | WEEK 9 | Anomaly | Processor |
| consistency checks | P3 | ✅ COMPLETED | WEEK 9 | API | Checks |
| chaos experiments | P4 | ✅ COMPLETED | WEEK 9 | Prometheus | Experiments |
| evaluation datasets | P1 | ✅ COMPLETED | WEEK 10 | Generator | Datasets |
| ground truth + anomaly metrics | P2 | ✅ COMPLETED | WEEK 10 | Anomaly | Ground truth |
| optimization | P3 | ✅ COMPLETED | WEEK 10 | Pipeline | Optimized perf |
| resilience evaluation | P4 | ✅ COMPLETED | WEEK 10 | Chaos | Evaluation |
| final integration | ALL | ✅ COMPLETED | WEEK 11 | All | Integration |

## Definition of Done
- [x] All pipeline services (Kafka ingestion, ClickHouse storage, API) are fully implemented and integrated.
- [x] Observability is established via custom Prometheus counters/histograms and Grafana dashboards.
- [x] The React UI displays real-time throughput, latency, VWAPs, and anomalies.
- [x] Automated chaos experiments run successfully.
- [x] Performance stress and resilience evaluation metrics are exported as JSON/Markdown reports.

## Getting Started & Execution Guide

### 1. Project Prerequisites & Installation
Ensure you have Python 3.10+, Node.js, and npm installed.
```bash
# Set up Python virtual environment and dependencies
source .venv/bin/activate
uv pip install -r pyproject.toml

# Set up Node.js frontend dependencies
cd frontend
npm install
cd ..
```

### 2. Granting Executable Permissions
Give all shell utility scripts executable rights:
```bash
chmod +x scripts/*.sh
```

### 3. Running the Backend Pipeline
Start the entire backend processing pipeline (mock generator, stream processor, and FastAPI API). To skip Docker compose and run in local simulation mode:
```bash
./scripts/start.sh --local
```

### 4. Running the Frontend UI Dashboard
With the backend running, launch the Vite React interface:
```bash
cd frontend
npm run dev
```
Open `http://localhost:3000` in your browser.

### 5. Running Testing & Experiments
```bash
# Run full pytest suite
./scripts/run_tests.sh

# Run chaos experiments
./scripts/run_experiments.sh

# Run end-to-end platform demo
./scripts/run_demo.sh
```

### 6. Cleaning Up
Stop all background processes and containers:
```bash
./scripts/stop.sh
```
