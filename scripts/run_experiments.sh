#!/bin/bash
# OWNER: SHARED
#
# PURPOSE:
# Run all chaos experiments.
#
# RESPONSIBILITIES:
# Execute chaos runner.

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

echo "==============================================="
echo "Running chaos experiments orchestrator..."
echo "==============================================="

# Enable venv if exists
if [ -d "$PROJECT_ROOT/.venv" ]; then
    source "$PROJECT_ROOT/.venv/bin/activate"
fi

python3 "$PROJECT_ROOT/chaos/runner.py"

echo "Chaos experiments runner completed."
