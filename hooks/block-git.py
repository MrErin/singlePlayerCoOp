#!/usr/bin/env python3
"""PreToolUse hook: block git operations. User controls all git."""
import json
import sys

try:
    data = json.load(sys.stdin)
    cmd = data.get("tool_input", {}).get("command", "")

    blocked = [
        "git commit",
        "git add",
        "git push",
        "git merge",
        "git rebase",
        "git checkout -b",
    ]

    for b in blocked:
        if b in cmd:
            print(
                f"Blocked: {b} — user controls all git operations.",
                file=sys.stderr,
            )
            sys.exit(0)

except Exception:
    pass
