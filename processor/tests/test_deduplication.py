# OWNER: P2
#
# PURPOSE:
# Test deduplication logic.

import time
from processor.deduplication.deduplicator import Deduplicator

def test_duplicate_detection():
    dedup = Deduplicator(ttl_seconds=2)
    assert dedup.is_duplicate("evt-1") is False
    assert dedup.is_duplicate("evt-1") is True
    assert dedup.is_duplicate("evt-2") is False

def test_state_ttl():
    dedup = Deduplicator(ttl_seconds=1)
    assert dedup.is_duplicate("evt-1") is False
    time.sleep(1.1)
    # The event should be evicted after TTL expires
    assert dedup.is_duplicate("evt-1") is False
