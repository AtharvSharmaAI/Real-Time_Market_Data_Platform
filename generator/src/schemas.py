# OWNER: P1
#
# PURPOSE:
# Define the canonical event schema.

from pydantic import BaseModel, Field
from datetime import datetime

class MarketTradeEvent(BaseModel):
    event_id: str
    event_time: datetime
    symbol: str
    price: float
    volume: float
    exchange: str
    side: str
    schema_version: str = "1.0.0"
