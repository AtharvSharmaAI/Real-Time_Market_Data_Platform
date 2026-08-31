# OWNER: P3
#
# PURPOSE:
# Anomalies API routes.
#
# RESPONSIBILITIES:
# Eventually:
# GET /anomalies
# GET /anomalies/{symbol}
#
# DEPENDENCIES:
# None
#
# INTERFACES:
# INPUT: Request
# OUTPUT: Response
#
# IMPLEMENTATION TODO:
# 1. Add endpoints.

from fastapi import APIRouter, Query, HTTPException
from typing import List
from api.app.models.responses import AnomalyResponse
from api.app.services.anomaly_service import AnomalyService

router = APIRouter()

@router.get("", response_model=List[AnomalyResponse])
async def get_anomalies(limit: int = Query(100, ge=1, le=1000)):
    """
    Get recent detected anomalies across all symbols.
    """
    try:
        anomalies = AnomalyService.get_anomalies(limit=limit)
        return anomalies
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{symbol}", response_model=List[AnomalyResponse])
async def get_anomalies_by_symbol(symbol: str, limit: int = Query(100, ge=1, le=1000)):
    """
    Get recent detected anomalies for a specific symbol.
    """
    try:
        anomalies = AnomalyService.get_anomalies_by_symbol(symbol=symbol, limit=limit)
        return anomalies
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
