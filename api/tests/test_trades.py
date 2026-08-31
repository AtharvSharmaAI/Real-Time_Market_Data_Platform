# OWNER: P3
#
# PURPOSE:
# Test trades routes.
#
# RESPONSIBILITIES:
# Test GET /trades/{symbol}
#
# DEPENDENCIES:
# None
#
# INTERFACES:
# INPUT: None
# OUTPUT: None
#
# IMPLEMENTATION TODO:
# 1. Write tests.

from fastapi.testclient import TestClient
from api.app.main import app
from unittest.mock import patch

client = TestClient(app)

def test_get_trades():
    """
    Test GET /trades/{symbol} returns list of trades.
    """
    mock_trades = [
        {
            "event_id": "mock-evt-123456",
            "event_time": "2026-08-31T14:00:00",
            "symbol": "AAPL",
            "price": 150.25,
            "volume": 100.0,
            "exchange": "NYSE",
            "side": "BUY",
            "schema_version": "1.0.0"
        }
    ]
    with patch("api.app.services.market_service.MarketService.get_trades", return_value=mock_trades):
        response = client.get("/trades/AAPL")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["symbol"] == "AAPL"
        assert data[0]["price"] == 150.25
        assert data[0]["side"] == "BUY"
