# OWNER: P3
#
# PURPOSE:
# API response models.
#
# RESPONSIBILITIES:
# Document expected response schemas.
#
# DEPENDENCIES:
# pydantic
#
# INTERFACES:
# INPUT: None
# OUTPUT: Response Model
#
# IMPLEMENTATION TODO:
# 1. Define response models.

from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class HealthResponse(BaseModel):
    status: str
    clickhouse_status: str
    timestamp: datetime

class TradeResponse(BaseModel):
    event_id: str
    event_time: datetime
    symbol: str
    price: float
    volume: float
    exchange: str
    side: str
    schema_version: str

class VWAPResponse(BaseModel):
    symbol: str
    window_start: datetime
    window_end: datetime
    vwap: float
    volume: float

class AnomalyResponse(BaseModel):
    symbol: str
    window_start: datetime
    window_end: datetime
    vwap: float
    volume: float
    volatility: float
    anomaly_flag: bool
    anomaly_type: str
    anomaly_score: float
