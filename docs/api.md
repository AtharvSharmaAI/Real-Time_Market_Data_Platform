# API Specification

This document details the HTTP endpoints exposed by the FastAPI backend application.

## Endpoints

### 1. Health Check
- **URL**: `/health`
- **Method**: `GET`
- **Response**:
  ```json
  {
    "status": "OK",
    "mode": "simulation",
    "version": "1.0.0"
  }
  ```

### 2. Get Recent Trades
- **URL**: `/trades`
- **Method**: `GET`
- **Query Parameters**:
  - `limit` (int, default=100)
- **Response**:
  ```json
  [
    {
      "event_id": "evt-b09e4f",
      "symbol": "AAPL",
      "price": 175.25,
      "volume": 100,
      "exchange": "NASDAQ",
      "side": "BUY",
      "event_time": "2026-08-31T12:00:00Z"
    }
  ]
  ```

### 3. Get VWAP Aggregates
- **URL**: `/vwap`
- **Method**: `GET`
- **Query Parameters**:
  - `symbol` (str, optional)
- **Response**:
  ```json
  [
    {
      "symbol": "AAPL",
      "vwap": 175.45,
      "volume": 12500,
      "window_start": "2026-08-31T12:00:00Z",
      "window_end": "2026-08-31T12:00:05Z"
    }
  ]
  ```

### 4. Get Detected Anomalies
- **URL**: `/anomalies`
- **Method**: `GET`
- **Query Parameters**:
  - `symbol` (str, optional)
- **Response**:
  ```json
  [
    {
      "symbol": "AAPL",
      "anomaly_type": "PRICE_SPIKE",
      "anomaly_score": 4.25,
      "processed_at": "2026-08-31T12:00:02Z"
    }
  ]
  ```