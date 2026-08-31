# OWNER: P2
#
# PURPOSE:
# Define input trade schemas and constraints.

from pydantic import BaseModel, Field, field_validator
from datetime import datetime

class RawTradeSchema(BaseModel):
    event_id: str = Field(..., min_length=1)
    event_time: datetime
    symbol: str = Field(..., min_length=1)
    price: float
    volume: float
    exchange: str = Field(..., min_length=1)
    side: str = Field(..., min_length=3)
    schema_version: str = Field("1.0.0")

    @field_validator("price")
    @classmethod
    def validate_price(cls, v):
        if v <= 0:
            raise ValueError("Price must be greater than zero")
        return v

    @field_validator("volume")
    @classmethod
    def validate_volume(cls, v):
        if v <= 0:
            raise ValueError("Volume must be greater than zero")
        return v

    @field_validator("side")
    @classmethod
    def validate_side(cls, v):
        v_upper = v.upper()
        if v_upper not in ("BUY", "SELL"):
            raise ValueError("Side must be BUY or SELL")
        return v_upper
