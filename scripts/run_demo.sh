#!/bin/bash
# OWNER: SHARED
#
# PURPOSE:
# Run demo scenario.
#
# RESPONSIBILITIES:
# Execute a full end-to-end simulated run showing the pipeline features:
# - Validations
# - Window metrics aggregation
# - Anomaly flags

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

# Enable venv if exists
if [ -d "$PROJECT_ROOT/.venv" ]; then
    source "$PROJECT_ROOT/.venv/bin/activate"
fi

echo "=========================================================="
echo "Real-Time Market Data Platform: End-to-End Pipeline Demo"
echo "=========================================================="
echo ""
echo "Running the streaming processor pipeline over generated market data..."
echo ""

# Run processor main with a small limit so it finishes and outputs metrics
python3 -m processor.src.main

echo ""
echo "=========================================================="
echo "Demo Completed Successfully!"
echo "=========================================================="
