-- OWNER: P3
--
-- PURPOSE:
-- Anomaly view.
--
-- RESPONSIBILITIES:
-- Document intended anomaly view.
--
-- DEPENDENCIES:
-- None
--
-- INTERFACES:
-- INPUT: None
-- OUTPUT: None
--
-- IMPLEMENTATION TODO:
-- 1. Define view.

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
