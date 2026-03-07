#!/usr/bin/env python3
"""PostToolUse hook: auto-format files after Claude writes or edits them."""
import json
import sys
import subprocess
import os

try:
    data = json.load(sys.stdin)
    fp = data.get("tool_input", {}).get("file_path", "")

    if not fp or not os.path.isfile(fp):
        sys.exit(0)

    ext = os.path.splitext(fp)[1]

    if ext == ".py":
        subprocess.run(
            ["ruff", "check", "--fix", "--quiet", fp], stderr=subprocess.DEVNULL
        )
    elif ext in (".ts", ".tsx", ".js", ".jsx", ".css", ".json"):
        subprocess.run(
            ["npx", "prettier", "--write", fp],
            stderr=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
        )

except Exception:
    # Never block Claude on a formatting failure
    pass
