# ClickHouse Database Design

This document details the tables and analytical purposes of the ClickHouse database.

## Tables

### 1. `trades`
Stores verified individual trade logs.
- **Engine**: `MergeTree`
- **Primary Key**: `(symbol, event_time)`
- **Schema**:
  - `event_id` (String)
  - `symbol` (String)
  - `price` (Float64)
  - `volume` (Float64)
  - `exchange` (String)
  - `side` (String)
  - `event_time` (DateTime)

### 2. `vwap_aggregates`
Stores pre-calculated tumbling window metrics.
- **Engine**: `ReplacingMergeTree` (based on window end and symbol)
- **Primary Key**: `(symbol, window_start)`
- **Schema**:
  - `symbol` (String)
  - `vwap` (Float64)
  - `volume` (Float64)
  - `window_start` (DateTime)
  - `window_end` (DateTime)

### 3. `anomalies`
Stores records of statistical anomalies.
- **Engine**: `MergeTree`
- **Primary Key**: `(symbol, processed_at)`
- **Schema**:
  - `symbol` (String)
  - `anomaly_type` (String)
  - `anomaly_score` (Float64)
  - `processed_at` (DateTime)