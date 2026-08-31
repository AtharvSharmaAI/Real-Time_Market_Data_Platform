# OWNER: P3
#
# PURPOSE:
# Trades API routes.
#
# RESPONSIBILITIES:
# Eventually: GET /trades/{symbol}
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
from api.app.models.responses import TradeResponse
from api.app.services.market_service import MarketService

router = APIRouter()

@router.get("/{symbol}", response_model=List[TradeResponse])
async def get_trades(symbol: str, limit: int = Query(100, ge=1, le=1000)):
    """
    Get raw trade events for a specific symbol.
    """
    try:
        trades = MarketService.get_trades(symbol=symbol, limit=limit)
        return trades
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
