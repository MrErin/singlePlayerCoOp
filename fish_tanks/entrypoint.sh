#!/bin/bash
# Detect and activate existing virtual environments
# Does NOT auto-install - uses what's already in the project

PROJECT_DIR="/project"

echo "========================================"
echo "  Fish Tank Environment"
echo "  $(date)"
echo "========================================"

# Python: Activate .venv if it exists
if [ -f "$PROJECT_DIR/.venv/bin/activate" ]; then
    echo "Found Python .venv - activating"
    source "$PROJECT_DIR/.venv/bin/activate"
    export VIRTUAL_ENV="$PROJECT_DIR/.venv"
fi

# Node.js: Add local node_modules/.bin to PATH if it exists
if [ -d "$PROJECT_DIR/node_modules/.bin" ]; then
    echo "Found node_modules - adding to PATH"
    export PATH="$PROJECT_DIR/node_modules/.bin:$PATH"
fi

# Report environment status
echo ""
echo "Environment ready. Using project's installed packages."
echo "Run commands via: .venv/bin/<tool> or npx <tool>"
echo ""

# Execute Claude with all arguments
exec claude "$@"
