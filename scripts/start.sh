#!/bin/bash
# OWNER: SHARED
#
# PURPOSE:
# Start the system.
#
# RESPONSIBILITIES:
# Run start steps:
# - Setup Kafka topics
# - Launch processor, generator, API, and ClickHouse
# - Manage fallback to simulation mode if docker-compose is not running.

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

echo "==============================================="
echo "Starting Real-Time Market Data Platform..."
echo "==============================================="

# Check if --local flag is passed or FORCE_SIMULATION is set to true
USE_DOCKER=true
if [[ "$*" == *"--local"* ]] || [[ "$FORCE_SIMULATION" == "true" ]]; then
    USE_DOCKER=false
fi

if [ "$USE_DOCKER" = "true" ] && docker info >/dev/null 2>&1; then
    echo "Docker detected. Starting containers..."
    docker compose up -d
    echo "Docker containers started successfully."
else
    echo "Starting services in local simulation mode..."
    
    # 1. Initialize Kafka Topics
    echo "Initializing Kafka topics..."
    bash "$PROJECT_ROOT/kafka/topics.sh" || echo "Local Kafka not running; using generator/processor simulation fallback."

    # 2. Run ClickHouse init scripts (if clickhouse-client is local)
    echo "Configuring persistent schemas..."
    if command -v clickhouse-client &> /dev/null; then
        clickhouse-client --queries-file "$PROJECT_ROOT/clickhouse/init.sql" || echo "ClickHouse initialization skipped."
    fi

    # 3. Start local background Python services
    echo "Bootstrapping background streaming services..."
    
    PYTHON_BIN="python3"
    if [ -f "$PROJECT_ROOT/.venv/bin/python" ]; then
        PYTHON_BIN="$PROJECT_ROOT/.venv/bin/python"
    elif [ -f "$PROJECT_ROOT/.venv/bin/python3" ]; then
        PYTHON_BIN="$PROJECT_ROOT/.venv/bin/python3"
    fi
    echo "Using python executable: $PYTHON_BIN"
    
    # Start generator
    $PYTHON_BIN -m generator.src.generator > "$PROJECT_ROOT/generator.log" 2>&1 &
    GEN_PID=$!
    echo "Generator started with PID: $GEN_PID (Logging to generator.log)"
    
    # Start processor
    $PYTHON_BIN -m processor.src.main > "$PROJECT_ROOT/processor.log" 2>&1 &
    PROC_PID=$!
    echo "Processor started with PID: $PROC_PID (Logging to processor.log)"
    
    # Start FastAPI backend
    $PYTHON_BIN -m api.app.main > "$PROJECT_ROOT/api.log" 2>&1 &
    API_PID=$!
    echo "FastAPI backend started with PID: $API_PID (Logging to api.log)"
    
    # Write PIDs to a file for graceful shutdown
    echo "$GEN_PID" > "$PROJECT_ROOT/.services.pids"
    echo "$PROC_PID" >> "$PROJECT_ROOT/.services.pids"
    echo "$API_PID" >> "$PROJECT_ROOT/.services.pids"
fi

echo "Startup complete."
