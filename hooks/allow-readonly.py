#!/usr/bin/env python3
"""PreToolUse hook: auto-allow safe read-only commands.

Parses compound commands (pipes, &&, ||, ;) and allows them if ALL
individual commands are in the safe read-only list. This eliminates
permission churn for diagnostic/informational commands.

Must be listed BEFORE block-dangerous.py in settings.json hooks.
"""
import json
import re
import sys

# Safe read-only commands that can be combined freely
SAFE_COMMANDS = {
    # File inspection (read-only)
    "cat",
    "head",
    "tail",
    "less",
    "more",
    "wc",
    "file",
    "stat",
    "ls",
    "tree",
    "find",  # find is read-only
    # System info (read-only)
    "uname",
    "hostname",
    "date",
    "whoami",
    "id",
    "uptime",
    "free",
    "df",
    "du",
    "ps",
    "top",
    "htop",
    "env",
    "printenv",
    # Text processing (read-only when no files modified)
    "grep",
    "egrep",
    "fgrep",
    "awk",
    "sed",  # sed without -i is read-only
    "cut",
    "sort",
    "uniq",
    "tr",
    "basename",
    "dirname",
    "realpath",
    "readlink",
    # Network info (read-only)
    "ping",
    "curl",  # curl without -X POST/PUT/DELETE is read-only
    "wget",  # wget to stdout is read-only
    "dig",
    "nslookup",
    "host",
    "ip",  # ip addr show, ip route show, etc.
    "netstat",
    "ss",
    # Misc safe commands
    "echo",
    "printf",
    "true",
    "false",
    "pwd",
    "which",
    "type",
    "command",
    "hash",
    # Git read-only
    "git",  # blocked commands handled by block-git.py
    # Python/node version checks
    "python3",
    "python",
    "node",
    "npm",
    "npx",
    "pip",
    "pip3",
}


def is_safe_command(cmd: str) -> bool:
    """Check if a single command is safe (read-only).

    Returns True if the command is in the safe list and doesn't
    contain dangerous modifiers.
    """
    cmd = cmd.strip()
    if not cmd:
        return True  # Empty parts are safe

    # Extract the base command (first word)
    parts = cmd.split()
    if not parts:
        return True

    base_cmd = parts[0]

    # Handle commands with paths (e.g., /usr/bin/cat)
    if "/" in base_cmd:
        base_cmd = base_cmd.rsplit("/", 1)[-1]

    # Check if base command is in safe list
    if base_cmd not in SAFE_COMMANDS:
        return False

    # Additional safety checks for specific commands
    # sed with -i modifies files
    if base_cmd == "sed" and "-i" in cmd:
        return False

    # curl with -X POST/PUT/DELETE/PATCH modifies state
    if base_cmd == "curl" and re.search(r"-X\s+(POST|PUT|DELETE|PATCH)", cmd):
        return False

    # npm install modifies node_modules
    if base_cmd == "npm" and "install" in cmd:
        return False

    # pip install modifies site-packages
    if base_cmd in ("pip", "pip3") and "install" in cmd:
        return False

    return True


def split_compound_command(cmd: str) -> list[str]:
    """Split a compound command into individual commands.

    Handles: | (pipe), && (and), || (or), ; (sequential), $(...) subshells
    """
    # First, normalize whitespace
    normalized = " ".join(cmd.split())

    # Split on shell operators
    # This regex splits on |, &&, ||, ; while preserving what's between
    parts = re.split(r"\|\|?|&&|;|\$\(|\`", normalized)

    return [p.strip() for p in parts if p.strip()]


def check_all_safe(cmd: str) -> bool:
    """Check if all parts of a compound command are safe."""
    parts = split_compound_command(cmd)

    for part in parts:
        if not is_safe_command(part):
            return False

    return True


def main() -> None:
    try:
        data = json.load(sys.stdin)
    except (json.JSONDecodeError, EOFError):
        return

    tool_name = data.get("tool_name", "")
    if tool_name != "Bash":
        return

    cmd = data.get("tool_input", {}).get("command", "")
    if not cmd:
        return

    # If all parts are safe, auto-allow
    if check_all_safe(cmd):
        result = {
            "hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "permissionDecision": "allow",
                "permissionDecisionReason": "Auto-allowed: all commands are read-only",
            }
        }
        json.dump(result, sys.stdout)
        sys.exit(0)

    # Otherwise, fall through to normal permission handling
    # (don't output anything, just exit)


if __name__ == "__main__":
    main()
