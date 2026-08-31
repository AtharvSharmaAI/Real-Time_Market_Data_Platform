# OWNER: P3
#
# PURPOSE:
# Test health route.
#
# RESPONSIBILITIES:
# Test GET /health
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

client = TestClient(app)

def test_get_health():
    """
    Test GET /health returns expected structure.
    """
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "clickhouse_status" in data
    assert "timestamp" in data
