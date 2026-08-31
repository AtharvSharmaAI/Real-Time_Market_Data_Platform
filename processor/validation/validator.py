# OWNER: P2
#
# PURPOSE:
# Validate raw events.
#
# RESPONSIBILITIES:
# Validate incoming payloads.

from typing import Dict, Any
from pydantic import ValidationError as PydanticValidationError
from processor.validation.schema import RawTradeSchema
from processor.validation.errors import (
    ValidationError,
    MissingFieldException,
    InvalidTypeException,
    DomainConstraintException
)

def validate_event(event: Dict[str, Any]) -> RawTradeSchema:
    """
    Validate a raw input event dictionary against schema and domain rules.
    Converts generic Pydantic validation errors into custom domain exceptions.
    """
    if not isinstance(event, dict):
        raise ValidationError("Event must be a dictionary.")

    # Check for missing fields explicitly before schema parse for granular errors
    required_fields = ["event_id", "event_time", "symbol", "price", "volume", "exchange", "side"]
    for field in required_fields:
        if field not in event or event[field] is None:
            raise MissingFieldException(f"Required field '{field}' is missing.")

    try:
        trade = RawTradeSchema(**event)
        return trade
    except PydanticValidationError as e:
        for error in e.errors():
            loc = error.get("loc", [None])[0]
            msg = error.get("msg", "")
            type_err = error.get("type", "")
            
            # Categorize the error
            if "greater than zero" in msg:
                raise DomainConstraintException(f"Domain constraint failed on field '{loc}': {msg}")
            elif "BUY or SELL" in msg:
                raise DomainConstraintException(f"Domain constraint failed on field '{loc}': {msg}")
            elif "type_error" in type_err or "parsing" in type_err or "datetime" in type_err:
                raise InvalidTypeException(f"Invalid type on field '{loc}': {msg}")
            else:
                raise ValidationError(f"Validation failed on field '{loc}': {msg}")
