# OWNER: P3
#
# PURPOSE:
# Anomaly data service logic.
#
# RESPONSIBILITIES:
# Explain anomaly queries and filtering.
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

logger = logging.getLogger("api.services.anomaly")

class AnomalyService:
    @staticmethod
    def get_anomalies(limit: int = 100) -> List[Dict[str, Any]]:
        """
        Retrieve recent anomaly events.
        Queries the ClickHouse processed_events table where anomaly_flag is true.
        """
        query = """
            SELECT symbol, window_start, window_end, vwap, volume, volatility, anomaly_flag, anomaly_type, anomaly_score 
            FROM processed_events 
            WHERE anomaly_flag = 1 
            ORDER BY window_end DESC 
            LIMIT %(limit)s
        """
        parameters = {"limit": limit}
        
        try:
            if not check_connection():
                raise ConnectionError("ClickHouse connection not available.")
            
            result = execute_query(query, parameters=parameters)
            columns = result.column_names
            return [dict(zip(columns, row)) for row in result.result_rows]
            
        except Exception as e:
            logger.warning(f"Failed to fetch anomalies from ClickHouse: {e}. Falling back to mock data if in debug mode.")
            if settings.DEBUG:
                return AnomalyService._get_mock_anomalies(limit=limit)
            return []

    @staticmethod
    def get_anomalies_by_symbol(symbol: str, limit: int = 100) -> List[Dict[str, Any]]:
        """
        Retrieve recent anomaly events for a given symbol.
        Queries the ClickHouse processed_events table where anomaly_flag is true.
        """
        query = """
            SELECT symbol, window_start, window_end, vwap, volume, volatility, anomaly_flag, anomaly_type, anomaly_score 
            FROM processed_events 
            WHERE anomaly_flag = 1 AND symbol = %(symbol)s 
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
            logger.warning(f"Failed to fetch anomalies for symbol {symbol} from ClickHouse: {e}. Falling back to mock data if in debug mode.")
            if settings.DEBUG:
                return AnomalyService._get_mock_anomalies(symbol=symbol, limit=limit)
            return []

    @staticmethod
    def _get_mock_anomalies(symbol: str = None, limit: int = 100) -> List[Dict[str, Any]]:
        anomalies = []
        symbols = [symbol] if symbol else ["AAPL", "GOOGL", "MSFT", "AMZN"]
        now = datetime.now(timezone.utc)
        now_rounded = now - timedelta(seconds=now.second % 5, microseconds=now.microsecond)
        
        for i in range(min(limit, 5)):
            window_end = now_rounded - timedelta(seconds=i * 60)
            window_start = window_end - timedelta(seconds=5)
            sym = random.choice(symbols).upper()
            anomaly_type = random.choice(["PRICE_SPIKE", "VOLUME_SPIKE", "VOLATILITY_SPIKE"])
            
            anomalies.append({
                "symbol": sym,
                "window_start": window_start,
                "window_end": window_end,
                "vwap": round(150.0 + random.uniform(10.0, 50.0), 2),
                "volume": float(random.randint(5000, 20000)),
                "volatility": round(random.uniform(2.5, 5.0), 4),
                "anomaly_flag": True,
                "anomaly_type": anomaly_type,
                "anomaly_score": round(random.uniform(3.0, 5.5), 2)
            })
        return anomalies
