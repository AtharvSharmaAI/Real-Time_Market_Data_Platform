-- OWNER: P3
--
-- PURPOSE:
-- Throughput analytical query.
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
    toStartOfInterval(ingest_time, INTERVAL 1 MINUTE) AS interval_time,
    count() AS events_count,
    count() / 60.0 AS events_per_second,
    sum(volume) AS total_volume
FROM raw_events
WHERE ingest_time >= {start_time:DateTime64}
GROUP BY interval_time
ORDER BY interval_time DESC;
