# OWNER: P2
#
# PURPOSE:
# Test watermark logic.

from datetime import datetime, timedelta
from processor.event_time.watermark import WatermarkTracker
from processor.event_time.late_events import LateEventHandler

def test_watermark_generation():
    tracker = WatermarkTracker(delay_seconds=3)
    t1 = datetime(2026, 8, 31, 12, 0, 10)
    
    # Init watermark
    wm = tracker.update(t1)
    assert wm == t1 - timedelta(seconds=3)
    
    # Stale/late event should not move watermark forward
    t2 = datetime(2026, 8, 31, 12, 0, 5)
    wm = tracker.update(t2)
    assert wm == t1 - timedelta(seconds=3)

    # Future event should advance watermark
    t3 = datetime(2026, 8, 31, 12, 0, 15)
    wm = tracker.update(t3)
    assert wm == t3 - timedelta(seconds=3)

def test_late_event_handling():
    tracker = WatermarkTracker(delay_seconds=3)
    handler = LateEventHandler(tracker)
    
    t1 = datetime(2026, 8, 31, 12, 0, 10)
    tracker.update(t1)
    
    # Watermark is at 12:00:07
    # 12:00:08 is after watermark -> not late
    assert handler.is_late(datetime(2026, 8, 31, 12, 0, 8)) is False
    
    # 12:00:06 is before watermark -> late
    assert handler.is_late(datetime(2026, 8, 31, 12, 0, 6)) is True
