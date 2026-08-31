# OWNER: P2
#
# PURPOSE:
# Test windowing logic.

from datetime import datetime
from processor.windows.tumbling_window import TumblingWindowAssigner
from processor.windows.state import WindowStateStore

def test_tumbling_windows_assignment():
    assigner = TumblingWindowAssigner(size_seconds=5)
    
    t1 = datetime(2026, 8, 31, 12, 0, 3, 123456)
    start1, end1 = assigner.assign(t1)
    assert start1 == datetime(2026, 8, 31, 12, 0, 0)
    assert end1 == datetime(2026, 8, 31, 12, 0, 5)

    t2 = datetime(2026, 8, 31, 12, 0, 8, 999999)
    start2, end2 = assigner.assign(t2)
    assert start2 == datetime(2026, 8, 31, 12, 0, 5)
    assert end2 == datetime(2026, 8, 31, 12, 0, 10)

def test_window_finalization():
    store = WindowStateStore()
    start = datetime(2026, 8, 31, 12, 0, 0)
    end = datetime(2026, 8, 31, 12, 0, 5)
    
    event = {"event_id": "evt-1", "price": 100.0}
    store.add_to_window("AAPL", start, end, event)
    
    events = store.get_events("AAPL", start, end)
    assert len(events) == 1
    assert events[0] == event
    
    store.purge_window("AAPL", start, end)
    assert len(store.get_events("AAPL", start, end)) == 0
