#!/usr/bin/env python3
"""PreToolUse hook: block agent workarounds for fish tank restrictions.

When agents hit a fish tank limitation (e.g., seccomp-blocked chmod), they
sometimes try to work around it by writing patch files or manipulating the
environment. These workarounds are fragile, unpredictable, and undermine the
security model. This hook blocks the most common patterns.

Inspects both Write/Edit (file content) and Bash (environment manipulation)
tool calls.

Content patterns (shutil monkeypatch, os.chmod, ctypes) are only checked for
files outside known project source directories. This avoids false positives
when the project's own code legitimately uses os.chmod or similar calls.
Filename blocks (sitecustomize.py, usercustomize.py) apply globally.
"""
import json
import re
import sys


# Directories that contain project source code. Files under these paths are
# allowed to use os.chmod, shutil, etc. — the content patterns only apply
# to files OUTSIDE these directories (i.e., ad-hoc workaround scripts).
PROJECT_SOURCE_PREFIXES = (
    "/project/src/",
    "/project/lib/",
    "/project/tests/",
    "/project/test/",
    "/project/app/",
    "/project/apps/",
    "/project/packages/",
    # Relative paths (Claude sometimes uses these)
    "src/",
    "lib/",
    "tests/",
    "test/",
    "app/",
    "apps/",
    "packages/",
)

# Patterns in file content that indicate an agent is trying to patch
# around fish tank restrictions rather than reporting the issue.
# Only checked for files OUTSIDE PROJECT_SOURCE_PREFIXES.
BLOCKED_CONTENT_PATTERNS = [
    # Monkeypatching shutil copy functions
    (r"shutil\.copy2?\s*=", "shutil monkeypatch"),
    (r"shutil\.copytree\s*=", "shutil monkeypatch"),
    # Direct chmod/chown via Python stdlib
    (r"os\.chmod\s*\(", "os.chmod call"),
    (r"os\.chown\s*\(", "os.chown call"),
    (r"os\.fchmod\s*\(", "os.fchmod call"),
    (r"os\.fchown\s*\(", "os.fchown call"),
    # ctypes syscall invocation for chmod/chown
    (r"ctypes.*chmod", "ctypes chmod bypass"),
    (r"ctypes.*chown", "ctypes chown bypass"),
    (r"libc.*chmod", "libc chmod bypass"),
    (r"libc.*chown", "libc chown bypass"),
]

# Filenames that agents should not create (infrastructure managed by entrypoint)
BLOCKED_FILENAMES = [
    "sitecustomize.py",
    "usercustomize.py",
]

# Bash patterns that indicate environment manipulation to bypass restrictions
BLOCKED_BASH_PATTERNS = [
    # Injecting a custom sitecustomize via PYTHONPATH
    (r"PYTHONPATH=.*sitecustomize", "PYTHONPATH sitecustomize injection"),
    (r"PYTHONPATH=.*usercustomize", "PYTHONPATH usercustomize injection"),
    # Directly invoking python to patch shutil before running a tool
    (r"python3?\s+-c\s+.*shutil\.\w+\s*=", "python -c shutil monkeypatch"),
]


def check_write_or_edit(data: dict) -> str | None:
    """Check Write/Edit tool inputs for blocked content patterns."""
    tool_input = data.get("tool_input", {})

    # Check filename
    file_path = tool_input.get("file_path", "")
    filename = file_path.rsplit("/", 1)[-1] if "/" in file_path else file_path
    for blocked_name in BLOCKED_FILENAMES:
        if filename == blocked_name:
            return (
                f"Blocked: agents cannot create '{blocked_name}'. "
                f"This file is managed by the fish tank entrypoint. "
                f"Report the underlying error to the user instead."
            )

    # Content patterns only apply outside project source directories.
    # Project code is allowed to use os.chmod, shutil, etc. legitimately.
    if any(file_path.startswith(prefix) for prefix in PROJECT_SOURCE_PREFIXES):
        return None

    # Check content (Write tool) or new_string (Edit tool)
    content = tool_input.get("content", "") or tool_input.get("new_string", "")
    if not content:
        return None

    for pattern, label in BLOCKED_CONTENT_PATTERNS:
        if re.search(pattern, content):
            return (
                f"Blocked: file contains '{label}'. Agents cannot write code "
                f"that patches around fish tank security restrictions. "
                f"Report the underlying error to the user instead."
            )

    return None


def check_bash(data: dict) -> str | None:
    """Check Bash tool inputs for environment manipulation patterns."""
    cmd = data.get("tool_input", {}).get("command", "")
    if not cmd:
        return None

    for pattern, label in BLOCKED_BASH_PATTERNS:
        if re.search(pattern, cmd, re.IGNORECASE):
            return (
                f"Blocked: '{label}'. Agents cannot manipulate the Python "
                f"environment to bypass fish tank restrictions. "
                f"Report the underlying error to the user instead."
            )

    return None


def main() -> None:
    try:
        data = json.load(sys.stdin)
    except (json.JSONDecodeError, EOFError):
        return

    tool_name = data.get("tool_name", "")

    reason = None
    if tool_name in ("Write", "Edit", "MultiEdit"):
        reason = check_write_or_edit(data)
    elif tool_name == "Bash":
        reason = check_bash(data)

    if reason:
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
