# OWNER: P3
#
# PURPOSE:
# Database connection handling.
#
# RESPONSIBILITIES:
# Explain:
# - ClickHouse connection
# - connection pooling
# - query execution
# - error handling
#
# DEPENDENCIES:
# clickhouse-connect
#
# INTERFACES:
# INPUT: None
# OUTPUT: None
#
# IMPLEMENTATION TODO:
# 1. Setup DB connection logic.

import clickhouse_connect
from clickhouse_connect.driver.client import Client
import logging
import os
import re
import sqlite3
import threading
from types import SimpleNamespace
from typing import Optional
from api.app.config import settings

logger = logging.getLogger("api.database")

_client: Optional[Client] = None

# --- SQLite fallback (used when CLICKHOUSE_HOST is unset, e.g. on Unikraft) ---
# ponytail: one shared connection + global lock; fine for one writer thread and a light API load.
USE_SQLITE = not settings.CLICKHOUSE_HOST
_sqlite: Optional[sqlite3.Connection] = None
_sqlite_lock = threading.Lock()

_SQLITE_SCHEMA = """
CREATE TABLE IF NOT EXISTS raw_events (
    event_id TEXT, event_time TEXT, symbol TEXT, price REAL, volume REAL,
    exchange TEXT, side TEXT, schema_version TEXT);
CREATE INDEX IF NOT EXISTS raw_events_sym_time ON raw_events (symbol, event_time);
CREATE TABLE IF NOT EXISTS processed_events (
    symbol TEXT, window_start TEXT, window_end TEXT, vwap REAL, volume REAL, volatility REAL,
    anomaly_flag INTEGER, anomaly_type TEXT, anomaly_score REAL, processed_at TEXT);
CREATE INDEX IF NOT EXISTS processed_sym_end ON processed_events (symbol, window_end);
"""

def _sqlite_conn() -> sqlite3.Connection:
    global _sqlite
    if _sqlite is None:
        os.makedirs(os.path.dirname(settings.SQLITE_PATH) or ".", exist_ok=True)
        _sqlite = sqlite3.connect(settings.SQLITE_PATH, check_same_thread=False)
        _sqlite.executescript(_SQLITE_SCHEMA)
    return _sqlite

def _sqlite_exec(query: str, parameters: Optional[dict] = None):
    # ClickHouse-style %(name)s placeholders -> SQLite :name
    query = re.sub(r"%\((\w+)\)s", r":\1", query)
    with _sqlite_lock:
        cur = _sqlite_conn().execute(query, parameters or {})
        rows = cur.fetchall()
    return SimpleNamespace(column_names=[d[0] for d in cur.description or []], result_rows=rows)

def _sqlite_insert(table: str, row: dict):
    cols = ", ".join(row)
    with _sqlite_lock:
        conn = _sqlite_conn()
        conn.execute(f"INSERT INTO {table} ({cols}) VALUES ({', '.join(':' + c for c in row)})", row)
        conn.commit()

def insert_raw(trade: dict):
    _sqlite_insert("raw_events", {**trade, "event_time": str(trade["event_time"])})

def insert_window(payload: dict):
    _sqlite_insert("processed_events", payload)

def get_client() -> Optional[Client]:
    """
    Get or create a ClickHouse connection client.
    Handles exceptions to prevent the API from crashing during initialization.
    """
    global _client
    if _client is None:
        try:
            _client = clickhouse_connect.get_client(
                host=settings.CLICKHOUSE_HOST,
                port=settings.CLICKHOUSE_PORT,
                username=settings.CLICKHOUSE_USER,
                password=settings.CLICKHOUSE_PASSWORD,
                database=settings.CLICKHOUSE_DATABASE
            )
            logger.info("Successfully connected to ClickHouse.")
        except Exception as e:
            logger.error(f"Failed to connect to ClickHouse: {e}")
            _client = None
    return _client

def check_connection() -> bool:
    """
    Check if the ClickHouse database connection is active.
    """
    if USE_SQLITE:
        try:
            return _sqlite_exec("SELECT 1").result_rows == [(1,)]
        except sqlite3.Error as e:
            logger.error(f"SQLite check failed: {e}")
            return False
    client = get_client()
    if client is None:
        return False
    try:
        res = client.command("SELECT 1")
        return res == 1
    except Exception as e:
        logger.error(f"ClickHouse connection check failed: {e}")
        global _client
        _client = None
        return False

def execute_query(query: str, parameters: Optional[dict] = None):
    """
    Execute an analytical query and return the query result.
    Handles exceptions and logs errors.
    """
    if USE_SQLITE:
        return _sqlite_exec(query, parameters)
    client = get_client()
    if client is None:
        raise ConnectionError("ClickHouse database connection is not available.")
    try:
        return client.query(query, parameters=parameters)
    except Exception as e:
        logger.error(f"Database query failed: {e}\nQuery: {query}")
        raise e
