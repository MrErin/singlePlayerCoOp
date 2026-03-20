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

# Deploy shutil monkeypatch to work around seccomp-blocked chmod syscalls
# (tools like mutmut use shutil.copy2/copytree which call chmod internally)
if [ -z "$VENV_SP" ] && [ -d /project/.venv ]; then
  VENV_SP=$(find /project/.venv/lib -name "site-packages" -type d 2>/dev/null | head -1)
fi
if [ -n "$VENV_SP" ] && [ ! -f "${VENV_SP}/sitecustomize.py" ]; then
  cat > "${VENV_SP}/sitecustomize.py" << 'SITECUSTOM'
"""
Fish tank compatibility patch (auto-deployed by entrypoint.sh).

Python's shutil.copy2/copytree call chmod internally to preserve file
permissions. The fish tank seccomp profile blocks chmod syscalls, causing
PermissionError in tools like mutmut that copy files. This patch replaces
the affected shutil functions with cp-based alternatives.
"""
import shutil
import subprocess
from pathlib import Path


def _copy_file(src, dst, *, follow_symlinks=True):
    subprocess.run(['cp', str(src), str(dst)], check=True)
    return dst


def _copy_tree(src, dst, symlinks=False, ignore=None, copy_function=None,
               ignore_dangling_symlinks=False, dirs_exist_ok=False):
    Path(dst).parent.mkdir(parents=True, exist_ok=True)
    cmd = ['cp', '-r', str(src), str(dst)]
    subprocess.run(cmd, check=True)
    return dst


shutil.copy = _copy_file
shutil.copy2 = _copy_file
shutil.copytree = _copy_tree
SITECUSTOM
fi

exec "$@"
