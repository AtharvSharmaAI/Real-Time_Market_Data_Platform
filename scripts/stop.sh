#!/bin/bash
# OWNER: SHARED
#
# PURPOSE:
# Stop the system.
#
# RESPONSIBILITIES:
# Stop containers or kill background simulation processes.

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

echo "==============================================="
echo "Stopping Real-Time Market Data Platform..."
echo "==============================================="

if docker info >/dev/null 2>&1; then
    echo "Docker detected. Stopping containers..."
    docker compose down || docker-compose down || true
    echo "Docker containers stopped."
fi

# Stop any background python services
if [ -f "$PROJECT_ROOT/.services.pids" ]; then
    echo "Stopping background simulation services..."
    while read -r pid; do
        if kill -0 "$pid" >/dev/null 2>&1; then
            kill "$pid"
            echo "Killed service PID: $pid"
        fi
    done < "$PROJECT_ROOT/.services.pids"
    rm "$PROJECT_ROOT/.services.pids"
fi

echo "Teardown complete."
