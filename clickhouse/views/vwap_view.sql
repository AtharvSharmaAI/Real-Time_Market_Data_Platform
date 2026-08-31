-- OWNER: P3
--
-- PURPOSE:
-- VWAP materialized view.
--
-- RESPONSIBILITIES:
-- Document intended materialized view.
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
