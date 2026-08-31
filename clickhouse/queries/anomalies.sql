-- OWNER: P3
--
-- PURPOSE:
-- Anomalies analytical query.
--
-- RESPONSIBILITIES:
-- Explain the analytical query that will eventually be implemented.
--
-- DEPENDENCIES:
-- None
--
-- INTERFACES:
-- INPUT: None
-- OUTPUT: None
--
-- IMPLEMENTATION TODO:
-- 1. Write query.

SELECT
    symbol,
    anomaly_type,
    count() AS anomaly_count,
    avg(anomaly_score) AS average_score,
    max(anomaly_score) AS peak_score
FROM processed_events
WHERE anomaly_flag = 1
  AND window_start >= {start_time:DateTime64}
GROUP BY symbol, anomaly_type
ORDER BY anomaly_count DESC;
