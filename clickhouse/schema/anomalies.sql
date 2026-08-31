-- OWNER: P3
--
-- PURPOSE:
-- Anomalies table schema.
--
-- RESPONSIBILITIES:
-- Document anomaly table design.
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
