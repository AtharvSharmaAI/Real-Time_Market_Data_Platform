# Data Contract Specifications

This document defines the schemas and validation criteria applied across the stream processing platform.

## Event Schema (Pydantic / JSON)

Every incoming trade event in the `market-data` topic must match the following json format:

```json
{
  "event_id": "string (uuid4)",
  "symbol": "string (AAPL | MSFT | GOOGL | AMZN)",
  "price": "positive float (> 0.0)",
  "volume": "positive float (> 0.0)",
  "exchange": "string (NASDAQ | NYSE)",
  "side": "string (BUY | SELL)",
  "event_time": "string (ISO-8601 UTC timestamp)"
}
```

## Validation Rules

1. **Type Constraint**:
   - `price` and `volume` must be numeric float/int types.
2. **Bounds Constraint**:
   - `price` > 0
   - `volume` > 0
3. **Enum Values**:
   - `exchange` must be either `NASDAQ` or `NYSE`.
   - `side` must be either `BUY` or `SELL`.
4. **DLQ Offloading**:
   - Any record violating the above schemas is rejected, incrementing the validation error metrics, and written to `market-data-dlq`.