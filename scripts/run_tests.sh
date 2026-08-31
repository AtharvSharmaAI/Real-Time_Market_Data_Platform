#!/bin/bash
# OWNER: SHARED
#
# PURPOSE:
# Run tests.
#
# RESPONSIBILITIES:
# Execute pytest across all project subdirectories (generator, processor, api).

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

echo "==============================================="
echo "Running pytest test suite..."
echo "==============================================="

# Enable venv if exists
if [ -d "$PROJECT_ROOT/.venv" ]; then
    source "$PROJECT_ROOT/.venv/bin/activate"
fi

pytest "$PROJECT_ROOT/generator/tests" "$PROJECT_ROOT/processor/tests" "$PROJECT_ROOT/api/tests" --import-mode=importlib

echo "Test execution complete."
