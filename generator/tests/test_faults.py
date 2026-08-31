# OWNER: P1
#
# PURPOSE:
# Test fault injection.

import pytest
from generator.faults.malformed import inject_malformation
from generator.faults.duplicate import inject_duplicate
from generator.faults.late_events import inject_lateness
from generator.faults.anomalies import inject_anomaly
from generator.faults.out_of_order import OutOfOrderInjector
from generator.faults.traffic_burst import TrafficBurstController

def test_duplication():
    event = {"event_id": "evt-1", "symbol": "AAPL"}
    res = inject_duplicate(event, prob=1.0, seed=42)
    assert len(res) == 2
    assert res[0]["event_id"] == res[1]["event_id"]

def test_malformed_events():
    event = {"event_id": "evt-1", "symbol": "AAPL", "price": 10.0, "volume": 100.0, "side": "BUY"}
    # Force corruption
    res = inject_malformation(event, prob=1.0, seed=42)
    # Check if we altered/deleted some fields or values
    assert ("price" not in res) or ("volume" not in res) or ("symbol" not in res) or ("side" not in res) or (res["price"] == -50.0) or (res["volume"] == 0.0) or (isinstance(res.get("price"), str)) or (isinstance(res.get("volume"), str)) or (res.get("side") == "HOLD")

def test_lateness():
    event = {"event_id": "evt-1", "event_time": "2026-08-31T12:00:10.000000"}
    res = inject_lateness(event, prob=1.0, lateness_sec=5.0, seed=42)
    from datetime import datetime
    t_res = datetime.fromisoformat(res["event_time"].replace("Z", "+00:00"))
    t_expected = datetime.fromisoformat("2026-08-31T12:00:05")
    assert t_res.timestamp() == t_expected.timestamp()

def test_traffic_bursts_and_anomalies():
    # Test burst controller
    controller = TrafficBurstController(multiplier=5)
    assert controller.get_current_rate(10) == 10
    controller.activate()
    assert controller.get_current_rate(10) == 50
    
    # Test anomaly injection
    event = {"event_id": "evt-1", "price": 10.0, "volume": 100.0}
    res = inject_anomaly(event, prob=1.0, seed=42)
    assert res["price"] > 10.0 or res["volume"] > 100.0
