# OWNER: P1
#
# PURPOSE:
# Test event generator.

import pytest
from generator.src.generator import MarketDataGenerator
from generator.src.config import settings

def test_configurable_symbols():
    # Temporary override configuration settings
    settings.symbols = ["AAPL", "MSFT"]
    gen = MarketDataGenerator(seed=42)
    events = list(gen.generate_events(limit=10))
    assert len(events) == 10
    for e in events:
        assert e["symbol"] in ["AAPL", "MSFT"]

def test_deterministic_seed():
    gen1 = MarketDataGenerator(seed=100)
    events1 = list(gen1.generate_events(limit=5))

    gen2 = MarketDataGenerator(seed=100)
    events2 = list(gen2.generate_events(limit=5))

    for e1, e2 in zip(events1, events2):
        assert e1["symbol"] == e2["symbol"]
        assert e1["price"] == e2["price"]
