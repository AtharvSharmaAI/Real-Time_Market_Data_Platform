# OWNER: P1
#
# PURPOSE:
# Test replay functionality.

import pytest
from generator.src.replay import EventReplayer

def test_dynamic_generation_fallback():
    # If no file is provided, it should fall back to generating simulated events
    replayer = EventReplayer(sample_file="nonexistent_file.json", speed=100.0)
    events = list(replayer.replay(rate_per_second=1000))
    # Check that events are generated successfully
    assert len(events) > 0
    assert "event_id" in events[0]
