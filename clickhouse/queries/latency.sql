-- OWNER: P3
--
-- PURPOSE:
-- Latency analytical query.
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
    avg(dateDiff('millisecond', event_time, ingest_time)) AS avg_ingest_latency_ms,
    max(dateDiff('millisecond', event_time, ingest_time)) AS max_ingest_latency_ms,
    quantile(0.95)(dateDiff('millisecond', event_time, ingest_time)) AS p95_ingest_latency_ms,
    quantile(0.99)(dateDiff('millisecond', event_time, ingest_time)) AS p99_ingest_latency_ms
FROM raw_events
WHERE ingest_time >= {start_time:DateTime64}
GROUP BY symbol
ORDER BY p95_ingest_latency_ms DESC;
