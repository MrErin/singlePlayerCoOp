#!/bin/bash
# /usr/local/bin/entrypoint.sh
# Auto-detect Python project source path and set PYTHONPATH

# Auto-detect Python project source path
if [ -z "$PYTHONPATH" ]; then
  DETECTED=""
  # Strategy 1: Read pyproject.toml for src layout
  if [ -f /project/pyproject.toml ]; then
    # Check for [tool.setuptools.packages.find] with src directory
    if grep -q 'where.*=.*\["src"\]' /project/pyproject.toml 2>/dev/null; then
      DETECTED="/project/src"
    fi
  fi
  # Strategy 2: Check for src/ directory with __init__.py or package dirs
  if [ -z "$DETECTED" ] && [ -d /project/src ]; then
    DETECTED="/project/src"
  fi
  # Strategy 3: Fall back to project root (flat layout)
  if [ -z "$DETECTED" ]; then
    DETECTED="/project"
  fi
  # Also add venv site-packages if venv exists
  VENV_SP=""
  if [ -d /project/.venv ]; then
    VENV_SP=$(find /project/.venv/lib -name "site-packages" -type d 2>/dev/null | head -1)
  fi
  if [ -n "$VENV_SP" ]; then
    export PYTHONPATH="${DETECTED}:${VENV_SP}"
  else
    export PYTHONPATH="${DETECTED}"
  fi
fi

exec "$@"
