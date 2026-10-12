# OWNER: P3
#
# PURPOSE:
# VWAP API routes.
#
# RESPONSIBILITIES:
# Eventually: GET /vwap/{symbol}
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

from fastapi import APIRouter, Query, HTTPException
from typing import List
from api.app.models.responses import VWAPResponse
from api.app.services.market_service import MarketService

router = APIRouter()

@router.get("", response_model=List[VWAPResponse])
async def get_vwap_all(limit: int = Query(100, ge=1, le=1000)):
    """
    Same as below, across all symbols.
    """
    return await get_vwap(symbol="", limit=limit)

@router.get("/{symbol}", response_model=List[VWAPResponse])
async def get_vwap(symbol: str, limit: int = Query(100, ge=1, le=1000)):
    """
    Get Volume Weighted Average Price (VWAP) tumbling window calculations for a specific symbol.
    """
    try:
        vwap_data = MarketService.get_vwap(symbol=symbol, limit=limit)
        return vwap_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
