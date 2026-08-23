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
| Kafka setup | P1 | ⬜ NOT STARTED | WEEK 1 | None | Kafka running |
| processor skeleton + data contract | P2 | ⬜ NOT STARTED | WEEK 1 | None | Skeleton |
| ClickHouse setup | P3 | ⬜ NOT STARTED | WEEK 1 | None | ClickHouse running |
| Prometheus/Grafana setup | P4 | ⬜ NOT STARTED | WEEK 1 | None | Dashboards |
| generator/replay | P1 | ⬜ NOT STARTED | WEEK 2 | Kafka | Event generator |
| Kafka consumer | P2 | ⬜ NOT STARTED | WEEK 2 | Processor skeleton | Data ingestion |
| Kafka->ClickHouse prototype | P3 | ⬜ NOT STARTED | WEEK 2 | ClickHouse | Pipeline |
| basic metrics | P4 | ⬜ NOT STARTED | WEEK 2 | Prometheus | Dashboards |
| malformed-data generation | P1 | ⬜ NOT STARTED | WEEK 3 | Generator | Corrupt data |
| validation + DLQ | P2 | ⬜ NOT STARTED | WEEK 3 | Consumer | Validator |
| DLQ storage | P3 | ⬜ NOT STARTED | WEEK 3 | ClickHouse | Storage tables |
| DLQ dashboard | P4 | ⬜ NOT STARTED | WEEK 3 | Grafana | Dashboards |
| duplicate generation | P1 | ⬜ NOT STARTED | WEEK 4 | Generator | Duplicates |
| deduplication + VWAP | P2 | ⬜ NOT STARTED | WEEK 4 | Validation | VWAP |
| VWAP storage | P3 | ⬜ NOT STARTED | WEEK 4 | ClickHouse | Storage tables |
| duplicate metrics | P4 | ⬜ NOT STARTED | WEEK 4 | Prometheus | Dashboards |
| out-of-order generator | P1 | ⬜ NOT STARTED | WEEK 5 | Generator | Out-of-order |
| event-time + windows | P2 | ⬜ NOT STARTED | WEEK 5 | Deduplication | Windows |
| window queries | P3 | ⬜ NOT STARTED | WEEK 5 | ClickHouse | Queries |
| latency metrics | P4 | ⬜ NOT STARTED | WEEK 5 | Prometheus | Dashboards |
| late events | P1 | ⬜ NOT STARTED | WEEK 6 | Generator | Late data |
| watermark + lateness | P2 | ⬜ NOT STARTED | WEEK 6 | Event-time | Watermarks |
| late-event storage | P3 | ⬜ NOT STARTED | WEEK 6 | ClickHouse | Storage |
| lateness metrics | P4 | ⬜ NOT STARTED | WEEK 6 | Prometheus | Dashboards |
| stable replay | P1 | ⬜ NOT STARTED | WEEK 7 | Generator | Replay |
| volatility | P2 | ⬜ NOT STARTED | WEEK 7 | Windows | Volatility |
| Kafka Connect + FastAPI | P3 | ⬜ NOT STARTED | WEEK 7 | Connect | API |
| complete monitoring | P4 | ⬜ NOT STARTED | WEEK 7 | Prometheus | Complete set |
| anomaly injection | P1 | ⬜ NOT STARTED | WEEK 8 | Generator | Anomalies |
| anomaly detector | P2 | ⬜ NOT STARTED | WEEK 8 | Volatility | Detector |
| anomaly storage/API | P3 | ⬜ NOT STARTED | WEEK 8 | ClickHouse | API |
| anomaly dashboard | P4 | ⬜ NOT STARTED | WEEK 8 | Grafana | Dashboards |
| reproducible chaos inputs | P1 | ⬜ NOT STARTED | WEEK 9 | Generator | Chaos |
| correctness under failure | P2 | ⬜ NOT STARTED | WEEK 9 | Anomaly | Processor |
| consistency checks | P3 | ⬜ NOT STARTED | WEEK 9 | API | Checks |
| chaos experiments | P4 | ⬜ NOT STARTED | WEEK 9 | Prometheus | Experiments |
| evaluation datasets | P1 | ⬜ NOT STARTED | WEEK 10 | Generator | Datasets |
| ground truth + anomaly metrics | P2 | ⬜ NOT STARTED | WEEK 10 | Anomaly | Ground truth |
| optimization | P3 | ⬜ NOT STARTED | WEEK 10 | Pipeline | Optimized perf |
| resilience evaluation | P4 | ⬜ NOT STARTED | WEEK 10 | Chaos | Evaluation |
| final integration | ALL | ⬜ NOT STARTED | WEEK 11 | All | Integration |

## Definition of Done
TBD
