-- OWNER: P3
--
-- PURPOSE:
-- DLQ events table schema.
--
-- RESPONSIBILITIES:
-- Document DLQ table design.
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

CREATE TABLE IF NOT EXISTS dlq_events (
    event_id String,
    raw_payload String,
    error_message String,
    failed_at DateTime64(6, 'UTC') DEFAULT now()
) ENGINE = MergeTree()
ORDER BY (failed_at, event_id);
--
