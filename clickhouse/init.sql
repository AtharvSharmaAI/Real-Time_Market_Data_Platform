-- OWNER: P3
--
-- PURPOSE:
-- Initialization script for ClickHouse.
--
-- RESPONSIBILITIES:
-- Init DB.
--
-- DEPENDENCIES:
-- None
--
-- INTERFACES:
-- INPUT: None
-- OUTPUT: None
--
-- IMPLEMENTATION TODO:
-- 1. Init script.

-- Create database if not exists
CREATE DATABASE IF NOT EXISTS market_data;

-- Switch to market_data database
USE market_data;

-- Raw events table schema
CREATE TABLE IF NOT EXISTS raw_events (
    event_id String,
    event_time DateTime64(6, 'UTC'),
    symbol LowCardinality(String),
    price Decimal(18, 4),
    volume Float64,
    exchange LowCardinality(String),
    side LowCardinality(String),
    schema_version String,
    ingest_time DateTime64(6, 'UTC') DEFAULT now()
) ENGINE = MergeTree()
ORDER BY (symbol, event_time, event_id);

-- Processed events table schema
CREATE TABLE IF NOT EXISTS processed_events (
    symbol LowCardinality(String),
    window_start DateTime64(6, 'UTC'),
    window_end DateTime64(6, 'UTC'),
    vwap Decimal(18, 4),
    volume Float64,
    volatility Float64,
    anomaly_flag UInt8,
    anomaly_type LowCardinality(String),
    anomaly_score Float64,
    processed_time DateTime64(6, 'UTC') DEFAULT now()
) ENGINE = MergeTree()
ORDER BY (symbol, window_end);

-- DLQ events table schema
CREATE TABLE IF NOT EXISTS dlq_events (
    event_id String,
    raw_payload String,
    error_message String,
    failed_at DateTime64(6, 'UTC') DEFAULT now()
) ENGINE = MergeTree()
ORDER BY (failed_at, event_id);

-- Anomalies table schema
CREATE TABLE IF NOT EXISTS anomalies (
    symbol LowCardinality(String),
    window_start DateTime64(6, 'UTC'),
    window_end DateTime64(6, 'UTC'),
    vwap Decimal(18, 4),
    volume Float64,
    volatility Float64,
    anomaly_type LowCardinality(String),
    anomaly_score Float64,
    detected_at DateTime64(6, 'UTC') DEFAULT now()
) ENGINE = MergeTree()
ORDER BY (symbol, window_end);

-- VWAP materialized view
CREATE MATERIALIZED VIEW IF NOT EXISTS vwap_view
TO processed_events
AS SELECT
    symbol,
    toStartOfInterval(event_time, INTERVAL 5 SECOND) AS window_start,
    toStartOfInterval(event_time, INTERVAL 5 SECOND) + INTERVAL 5 SECOND AS window_end,
    sum(price * volume) / sum(volume) AS vwap,
    sum(volume) AS volume,
    0.0 AS volatility,
    0 AS anomaly_flag,
    'NONE' AS anomaly_type,
    0.0 AS anomaly_score
FROM raw_events
GROUP BY symbol, window_start, window_end;

-- Anomaly view
CREATE VIEW IF NOT EXISTS anomaly_view AS
SELECT
    symbol,
    window_start,
    window_end,
    vwap,
    volume,
    volatility,
    anomaly_type,
    anomaly_score,
    processed_time
FROM processed_events
WHERE anomaly_flag = 1;
