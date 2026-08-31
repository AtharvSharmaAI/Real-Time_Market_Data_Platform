-- OWNER: P3
--
-- PURPOSE:
-- Raw events table schema.
--
-- RESPONSIBILITIES:
-- Document intended schema.
--
-- DEPENDENCIES:
-- None
--
-- INTERFACES:
-- INPUT: None
-- OUTPUT: None
--
-- IMPLEMENTATION TODO:
-- 1. Define schema.

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
