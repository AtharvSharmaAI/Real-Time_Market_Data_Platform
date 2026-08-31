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
from typing import Optional
from api.app.config import settings

logger = logging.getLogger("api.database")

_client: Optional[Client] = None

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
    client = get_client()
    if client is None:
        raise ConnectionError("ClickHouse database connection is not available.")
    try:
        return client.query(query, parameters=parameters)
    except Exception as e:
        logger.error(f"Database query failed: {e}\nQuery: {query}")
        raise e
