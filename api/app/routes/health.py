# OWNER: P3
#
# PURPOSE:
# Health check API route.
#
# RESPONSIBILITIES:
# Eventually: GET /health
#
# DEPENDENCIES:
# None
#
# INTERFACES:
# INPUT: Request
# OUTPUT: Response
#
# IMPLEMENTATION TODO:
# 1. Add endpoint.

from fastapi import APIRouter
from datetime import datetime, timezone
from api.app.models.responses import HealthResponse
from api.app.database import check_connection

router = APIRouter()

@router.get("", response_model=HealthResponse)
async def get_health():
    """
    Get health status of the API and database connection.
    """
    ch_connected = check_connection()
    status = "healthy" if ch_connected else "degraded"
    clickhouse_status = "connected" if ch_connected else "disconnected"
    
    return HealthResponse(
        status=status,
        clickhouse_status=clickhouse_status,
        timestamp=datetime.now(timezone.utc)
    )
