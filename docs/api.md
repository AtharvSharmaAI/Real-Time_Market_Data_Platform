# API Specification

HTTP endpoints exposed by the FastAPI backend (`api/app/main.py`).

- Base URL (local): `http://localhost:8000`
- Interactive docs: `/docs` (Swagger UI), `/openapi.json`
- The frontend dev server (`http://localhost:3000`) proxies `/api/*` to this API, stripping the `/api` prefix (`frontend/vite.config.js`).

**Mock fallback:** if ClickHouse is unreachable and `DEBUG=true` (the default), `/trades`, `/vwap` and `/anomalies` return generated mock rows instead of failing. Mock trades have `event_id`s starting with `mock-`. With `DEBUG=false` they return `[]`. `/health` reports whether ClickHouse is connected.

## Endpoints

| Method | Path | Description |
|---|---|---|
| GET | `/` | Service info |
| GET | `/health` | API and ClickHouse status |
| GET | `/trades` | Latest raw trades, all symbols |
| GET | `/trades/{symbol}` | Latest raw trades for one symbol |
| GET | `/vwap` | Latest 5-second VWAP windows, all symbols |
| GET | `/vwap/{symbol}` | Latest VWAP windows for one symbol |
| GET | `/anomalies` | Latest anomalous windows, all symbols |
| GET | `/anomalies/{symbol}` | Latest anomalous windows for one symbol |
| GET | `/metrics` | Prometheus metrics for the API process |

All list endpoints take `limit` (int, 1–1000, default 100) and return the newest rows first. `{symbol}` is a ticker such as `AAPL`, `MSFT`, `GOOGL` or `AMZN`.

### `GET /`
```json
{ "message": "Welcome to the Real-Time Market Data API", "version": "0.1.0", "docs_url": "/docs" }
```

### `GET /health`
`status` is `healthy` when ClickHouse answers and `degraded` otherwise.
```json
{ "status": "degraded", "clickhouse_status": "disconnected", "timestamp": "2026-10-12T10:03:56.917230Z" }
```

### `GET /trades`, `GET /trades/{symbol}`
Source: ClickHouse `raw_events`, ordered by `event_time`.
```json
[
  {
    "event_id": "evt-001193-1717",
    "event_time": "2026-10-12T09:19:14.434617Z",
    "symbol": "AAPL",
    "price": 170.34,
    "volume": 883.0,
    "exchange": "NASDAQ",
    "side": "BUY",
    "schema_version": "1.0.0"
  }
]
```

### `GET /vwap`, `GET /vwap/{symbol}`
Source: ClickHouse `processed_events`, ordered by `window_end`.
```json
[
  {
    "symbol": "AAPL",
    "window_start": "2026-10-12T09:19:05Z",
    "window_end": "2026-10-12T09:19:10Z",
    "vwap": 161.6135,
    "volume": 58889.0
  }
]
```

### `GET /anomalies`, `GET /anomalies/{symbol}`
Source: ClickHouse `processed_events` where `anomaly_flag = 1`, ordered by `window_end`. `anomaly_type` is one of `PRICE_SPIKE`, `VOLUME_SPIKE` or `VOLATILITY_SPIKE`, and `anomaly_score` is the z-score.
```json
[
  {
    "symbol": "AMZN",
    "window_start": "2026-10-12T10:03:50Z",
    "window_end": "2026-10-12T10:03:55Z",
    "vwap": 164.01,
    "volume": 10196.0,
    "volatility": 3.5224,
    "anomaly_flag": true,
    "anomaly_type": "VOLATILITY_SPIKE",
    "anomaly_score": 3.44
  }
]
```

### `GET /metrics`
Prometheus text format (default process and Python collectors). Scraped as job `market-data-api`.

## Processor metrics

The stream processor (`processor/src/main.py`) serves its own Prometheus endpoint at `http://localhost:8001/metrics`. Set the port with `PROCESSOR_METRICS_PORT`. It is scraped as job `market-data-processor`, and these are the metrics the Grafana dashboards and `monitoring/alerts/alerts.yml` use:

| Metric | Type | Meaning |
|---|---|---|
| `events_received_total` | counter | Raw events consumed |
| `events_processed_total` | counter | Valid, unique, on-time events assigned to a window |
| `events_invalid_total` | counter | Events failing validation |
| `events_duplicate_total` | counter | Duplicates dropped |
| `events_late_total` | counter | Events behind the watermark, dropped |
| `dlq_events_total` | counter | Events sent to the DLQ |
| `anomalies_detected_total{anomaly_type}` | counter | Anomalous windows |
| `processing_latency_seconds` | histogram | Event time to processing time |

## Local service URLs

| Service | URL | Started by |
|---|---|---|
| Dashboard (Vite) | http://localhost:3000 | `cd frontend && npx vite --port 3000` |
| API | http://localhost:8000 | `scripts/start.sh` |
| Processor metrics | http://localhost:8001/metrics | `scripts/start.sh` |
| Prometheus | http://localhost:9090 | `docker run` (see `docs/setup.md`) |
| Grafana | http://localhost:3001 | `docker run` (see `docs/setup.md`) |
