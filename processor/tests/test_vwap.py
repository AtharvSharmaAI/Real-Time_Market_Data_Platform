# OWNER: P2
#
# PURPOSE:
# Test VWAP calculation.

from processor.analytics.vwap import calculate_vwap

def test_one_trade():
    trades = [{"price": 10.0, "volume": 5.0}]
    assert calculate_vwap(trades) == 10.0

def test_multiple_trades():
    trades = [
        {"price": 10.0, "volume": 5.0},
        {"price": 20.0, "volume": 10.0}
    ]
    # Sum(10*5 + 20*10) / Sum(5+10) = 250 / 15 = 16.6667
    assert calculate_vwap(trades) == 16.6667

def test_different_volumes():
    trades = [
        {"price": 15.0, "volume": 100.0},
        {"price": 16.0, "volume": 200.0}
    ]
    # Sum(15*100 + 16*200) / 300 = 4700 / 300 = 15.6667
    assert calculate_vwap(trades) == 15.6667

def test_zero_invalid_volume():
    trades = [
        {"price": 10.0, "volume": -5.0},
        {"price": 20.0, "volume": 0.0},
        {"price": 15.0, "volume": 10.0}
    ]
    assert calculate_vwap(trades) == 15.0
