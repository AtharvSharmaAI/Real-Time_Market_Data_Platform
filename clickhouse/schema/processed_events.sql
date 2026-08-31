-- OWNER: P3
--
-- PURPOSE:
-- Processed events table schema.
--
-- RESPONSIBILITIES:
-- Document:
-- event/window time
-- symbol
-- window_start
-- window_end
-- vwap
-- volume
-- volatility
-- anomaly_flag
-- anomaly_type
-- anomaly_score
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
