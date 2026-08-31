-- OWNER: P3
--
-- PURPOSE:
-- VWAP analytical query.
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
    window_start,
    window_end,
    vwap,
    volume
FROM processed_events
WHERE symbol = {symbol:String}
  AND window_start >= {start_time:DateTime64}
  AND window_end <= {end_time:DateTime64}
ORDER BY window_end DESC;
