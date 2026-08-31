# OWNER: P3
#
# PURPOSE:
# Market data service logic.
#
# RESPONSIBILITIES:
# Explain database/business logic separation.
#
# DEPENDENCIES:
# None
#
# INTERFACES:
# INPUT: None
# OUTPUT: None
#
# IMPLEMENTATION TODO:
# 1. Setup service.

import logging
from typing import List, Dict, Any
from datetime import datetime, timedelta, timezone
import random

from api.app.database import execute_query, check_connection
from api.app.config import settings

logger = logging.getLogger("api.services.market")

class MarketService:
    @staticmethod
    def get_trades(symbol: str, limit: int = 100) -> List[Dict[str, Any]]:
        """
        Retrieve raw trade events for a given symbol.
        Queries the ClickHouse raw_events table.
        """
        query = """
            SELECT event_id, event_time, symbol, price, volume, exchange, side, schema_version 
            FROM raw_events 
            WHERE symbol = %(symbol)s 
            ORDER BY event_time DESC 
            LIMIT %(limit)s
        """
        parameters = {"symbol": symbol, "limit": limit}
        
        try:
            if not check_connection():
                raise ConnectionError("ClickHouse connection not available.")
            
            result = execute_query(query, parameters=parameters)
            columns = result.column_names
            return [dict(zip(columns, row)) for row in result.result_rows]
            
        except Exception as e:
            logger.warning(f"Failed to fetch trades from ClickHouse: {e}. Falling back to mock data if in debug mode.")
            if settings.DEBUG:
                return MarketService._get_mock_trades(symbol, limit)
            return []

    @staticmethod
    def get_vwap(symbol: str, limit: int = 100) -> List[Dict[str, Any]]:
        """
        Retrieve volume weighted average price (VWAP) window data for a symbol.
        Queries the ClickHouse processed_events table.
        """
        query = """
            SELECT symbol, window_start, window_end, vwap, volume 
            FROM processed_events 
            WHERE symbol = %(symbol)s 
            ORDER BY window_end DESC 
            LIMIT %(limit)s
        """
        parameters = {"symbol": symbol, "limit": limit}
        
        try:
            if not check_connection():
                raise ConnectionError("ClickHouse connection not available.")
                
            result = execute_query(query, parameters=parameters)
            columns = result.column_names
            return [dict(zip(columns, row)) for row in result.result_rows]
            
        except Exception as e:
            logger.warning(f"Failed to fetch VWAP from ClickHouse: {e}. Falling back to mock data if in debug mode.")
            if settings.DEBUG:
                return MarketService._get_mock_vwap(symbol, limit)
            return []

    @staticmethod
    def _get_mock_trades(symbol: str, limit: int) -> List[Dict[str, Any]]:
        trades = []
        base_price = 150.0 + random.uniform(-10.0, 10.0)
        now = datetime.now(timezone.utc)
        for i in range(min(limit, 10)):
            trades.append({
                "event_id": f"mock-evt-{random.randint(100000, 999999)}",
                "event_time": now - timedelta(seconds=i * 2),
                "symbol": symbol.upper(),
                "price": round(base_price + random.uniform(-1.0, 1.0), 2),
                "volume": float(random.randint(10, 500)),
                "exchange": random.choice(["NYSE", "NASDAQ", "BATS"]),
                "side": random.choice(["BUY", "SELL"]),
                "schema_version": "1.0.0"
            })
        return trades

    @staticmethod
    def _get_mock_vwap(symbol: str, limit: int) -> List[Dict[str, Any]]:
        vwaps = []
        base_price = 150.0 + random.uniform(-10.0, 10.0)
        now = datetime.now(timezone.utc)
        now_rounded = now - timedelta(seconds=now.second % 5, microseconds=now.microsecond)
        for i in range(min(limit, 10)):
            window_end = now_rounded - timedelta(seconds=i * 5)
            window_start = window_end - timedelta(seconds=5)
            vwaps.append({
                "symbol": symbol.upper(),
                "window_start": window_start,
                "window_end": window_end,
                "vwap": round(base_price + random.uniform(-0.5, 0.5), 2),
                "volume": float(random.randint(1000, 5000))
            })
        return vwaps
