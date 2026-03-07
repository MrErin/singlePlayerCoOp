#!/usr/bin/env python3
"""PreToolUse hook: block dangerous system commands.

Prevents AI agents from executing commands that modify file permissions,
ownership, or other system-level state. These operations should only be
performed by the user directly.

Catches both direct invocations and commands embedded in pipelines,
subshells, and command chains (&&, ||, ;).
"""
import json
import re
import sys

# Commands that modify permissions or ownership
PERMISSION_COMMANDS = [
    "chmod",
    "chown",
    "chgrp",
    "setfacl",
    "umask",
]

# Commands that modify system state dangerously
SYSTEM_COMMANDS = [
    "sudo",
    "su ",
    "pkill",
    "killall",
    "kill -9",
    "shutdown",
    "reboot",
    "systemctl",
    "mkfs",
    "dd if=",
    "mount",
    "umount",
    "fdisk",
    "parted",
    "iptables",
    "nft",
    "useradd",
    "userdel",
    "usermod",
    "groupadd",
    "groupdel",
    "passwd",
]

# Destructive file operations
DESTRUCTIVE_COMMANDS = [
    "rm -rf /",
    "rm -rf ~",
    "rm -rf $HOME",
    "shred",
    "> /dev/sd",
]


def check_command(cmd: str) -> str | None:
    """Check if a command contains any blocked operations.

    Splits on shell operators (&&, ||, ;, |, $()) to catch
    commands hidden in pipelines or chains.

    Returns the matched blocked command string, or None if safe.
    """
    # Normalize whitespace
    normalized = " ".join(cmd.split())

    # Split on shell operators to inspect each sub-command
    parts = re.split(r"[;&|]+|\$\(|\)", normalized)

    for part in parts:
        stripped = part.strip()
        if not stripped:
            continue

        for blocked in PERMISSION_COMMANDS:
            # Match as a word boundary to avoid false positives
            # e.g., "chmod" should match but "echo chmod" context matters
            # We match if the command starts with or contains the blocked
            # command as a standalone word
            pattern = rf"(?:^|.*\s){re.escape(blocked)}(?:\s|$)"
            if re.search(pattern, stripped):
                return blocked

        for blocked in SYSTEM_COMMANDS:
            if blocked in stripped:
                return blocked.strip()

        for blocked in DESTRUCTIVE_COMMANDS:
            if blocked in stripped:
                return blocked

    return None


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

    match = check_command(cmd)
    if match:
        reason = (
            f"Blocked: '{match}' — agents cannot modify file permissions, "
            f"ownership, or system state. Run this manually if needed."
        )
        # Output JSON with deny decision for Claude Code hook protocol
        result = {
            "hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "permissionDecision": "deny",
                "permissionDecisionReason": reason,
            }
        }
        json.dump(result, sys.stdout)
        sys.exit(0)


if __name__ == "__main__":
    main()
