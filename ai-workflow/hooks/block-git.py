#!/usr/bin/env python3
"""PreToolUse hook: block git write operations. User controls all git."""
import json
import sys

BLOCKED = [
    "git commit",
    "git add",
    "git push",
    "git merge",
    "git rebase",
    "git checkout -b",
    "git reset --hard",
    "git restore .",
    "git clean -f",
    "git stash drop",
]


def main() -> None:
    try:
        data = json.load(sys.stdin)
    except (json.JSONDecodeError, EOFError):
        return

    if data.get("tool_name") != "Bash":
        return

    cmd = data.get("tool_input", {}).get("command", "")

    for b in BLOCKED:
        if b in cmd:
            result = {
                "hookSpecificOutput": {
                    "hookEventName": "PreToolUse",
                    "permissionDecision": "deny",
                    "permissionDecisionReason": (
                        f"Blocked: '{b}' — user controls all git operations."
                    ),
                }
            }
            json.dump(result, sys.stdout)
            sys.exit(0)


if __name__ == "__main__":
    main()
