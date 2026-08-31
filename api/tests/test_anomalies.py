# OWNER: P3
#
# PURPOSE:
# Test anomalies routes.
#
# RESPONSIBILITIES:
# Test GET /anomalies
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

def test_get_anomalies():
    """
    Test GET /anomalies returns list of anomalies.
    """
    mock_anomalies = [
        {
            "symbol": "AAPL",
            "window_start": "2026-08-31T14:00:00",
            "window_end": "2026-08-31T14:00:05",
            "vwap": 150.25,
            "volume": 12000.0,
            "volatility": 3.14,
            "anomaly_flag": True,
            "anomaly_type": "VOLUME_SPIKE",
            "anomaly_score": 4.2
        }
    ]
    with patch("api.app.services.anomaly_service.AnomalyService.get_anomalies", return_value=mock_anomalies):
        response = client.get("/anomalies")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["symbol"] == "AAPL"
        assert data[0]["anomaly_type"] == "VOLUME_SPIKE"

def test_get_anomalies_by_symbol():
    """
    Test GET /anomalies/{symbol} returns list of anomalies for specific symbol.
    """
    mock_anomalies = [
        {
            "symbol": "AAPL",
            "window_start": "2026-08-31T14:00:00",
            "window_end": "2026-08-31T14:00:05",
            "vwap": 150.25,
            "volume": 12000.0,
            "volatility": 3.14,
            "anomaly_flag": True,
            "anomaly_type": "VOLUME_SPIKE",
            "anomaly_score": 4.2
        }
    ]
    with patch("api.app.services.anomaly_service.AnomalyService.get_anomalies_by_symbol", return_value=mock_anomalies):
        response = client.get("/anomalies/AAPL")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["symbol"] == "AAPL"
