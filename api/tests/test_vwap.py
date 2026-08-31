# OWNER: P3
#
# PURPOSE:
# Test VWAP routes.
#
# RESPONSIBILITIES:
# Test GET /vwap/{symbol}
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

def test_get_vwap():
    """
    Test GET /vwap/{symbol} returns list of VWAP windows.
    """
    mock_vwap = [
        {
            "symbol": "AAPL",
            "window_start": "2026-08-31T14:00:00",
            "window_end": "2026-08-31T14:00:05",
            "vwap": 150.25,
            "volume": 500.0
        }
    ]
    with patch("api.app.services.market_service.MarketService.get_vwap", return_value=mock_vwap):
        response = client.get("/vwap/AAPL")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["symbol"] == "AAPL"
        assert data[0]["vwap"] == 150.25
        assert data[0]["volume"] == 500.0
