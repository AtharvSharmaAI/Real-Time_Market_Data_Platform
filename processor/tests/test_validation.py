# OWNER: P2
#
# PURPOSE:
# Test validation logic.

import pytest
from processor.validation.validator import validate_event
from processor.validation.errors import (
    MissingFieldException,
    InvalidTypeException,
    DomainConstraintException
)

def test_valid_event():
    event = {
        "event_id": "evt-123",
        "event_time": "2026-08-31T12:00:00.000000Z",
        "symbol": "AAPL",
        "price": 150.50,
        "volume": 100.0,
        "exchange": "NASDAQ",
        "side": "BUY",
        "schema_version": "1.0.0"
    }
    trade = validate_event(event)
    assert trade.event_id == "evt-123"
    assert trade.symbol == "AAPL"
    assert trade.price == 150.50
    assert trade.volume == 100.0

def test_missing_field():
    event = {
        "event_id": "evt-123",
        "event_time": "2026-08-31T12:00:00.000000Z",
        # "symbol" missing
        "price": 150.50,
        "volume": 100.0,
        "exchange": "NASDAQ",
        "side": "BUY"
    }
    with pytest.raises(MissingFieldException):
        validate_event(event)

def test_invalid_type():
    event = {
        "event_id": "evt-123",
        "event_time": "invalid-date",
        "symbol": "AAPL",
        "price": 150.50,
        "volume": 100.0,
        "exchange": "NASDAQ",
        "side": "BUY"
    }
    with pytest.raises(InvalidTypeException):
        validate_event(event)

def test_domain_constraint():
    event = {
        "event_id": "evt-123",
        "event_time": "2026-08-31T12:00:00.000000Z",
        "symbol": "AAPL",
        "price": -150.50, # negative price
        "volume": 100.0,
        "exchange": "NASDAQ",
        "side": "BUY"
    }
    with pytest.raises(DomainConstraintException):
        validate_event(event)
