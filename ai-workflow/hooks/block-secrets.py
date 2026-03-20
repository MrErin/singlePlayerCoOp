#!/usr/bin/env python3
"""PreToolUse hook: block all access to secret and credential files.

The Read tool deny list covers direct reads via the Read tool. This hook
covers every other access path agents commonly use:

  Bash: cat, grep, awk, sed, head, tail, sort, wc, diff, base64,
        python3 -c "open('.env')", find -exec cat, etc.
  Write/Edit/MultiEdit: agents writing to or overwriting secret files.

MUST be listed BEFORE allow-readonly.py in the Bash hook chain.
allow-readonly.py auto-approves commands like `cat` and `grep` — if it
runs first on a command like `cat .env`, the command is approved before
this hook ever sees it.

Known limitation: shell variable indirection (e.g., F=.env; cat $F) cannot
be detected by static command scanning. All other direct access patterns are
covered.
"""

import json
import re
import sys


# Each rule: (compiled pattern, human-readable label for the deny message).
# Patterns are matched against the full command string (Bash) or file path
# (Write/Edit/MultiEdit). Order does not matter — first match wins.
_RULES: list[tuple[re.Pattern[str], str]] = [
    (
        # .env, .env.local, .env.production, .envrc, etc.
        # Negative lookbehind blocks "dotenv" (the library name).
        # .env.example is stripped before this check — see _sanitize().
        re.compile(r"(?<![.\w])\.env(?:rc|\.[a-zA-Z0-9_+.\-]+)?(?![a-zA-Z0-9_])"),
        ".env file",
    ),
    (
        # SSH private key files by conventional name
        re.compile(r"\bid_(?:rsa|ed25519|ecdsa|dsa)\b"),
        "SSH private key",
    ),
    (
        # Files with secret-material extensions.
        # Requires at least one non-separator character before the dot
        # to avoid matching bare extension tokens.
        re.compile(r"\S+\.(?:pem|key|p12|pfx)\b"),
        "certificate or private key file",
    ),
    (
        re.compile(r"\.aws[/\\]credentials"),
        "AWS credentials file",
    ),
    (
        # .netrc stores FTP/HTTP credentials
        re.compile(r"(?<![.\w])\.netrc\b"),
        ".netrc credentials file",
    ),
    (
        # secrets/ or secret/ as a path component
        re.compile(r"\bsecrets?/"),
        "secrets directory",
    ),
    (
        # Files named with "credential" and a config-like extension.
        # More specific than bare "credential" to avoid false positives
        # on git-credential subcommands and similar.
        re.compile(
            r"\bcredentials?\.(?:json|ya?ml|toml|ini|conf|cfg|env|txt)\b",
            re.IGNORECASE,
        ),
        "credentials file",
    ),
]

_GUIDANCE = (
    "To find what variables the app needs, read .env.example or search "
    "source code for os.getenv / process.env / config lookups. "
    "If an actual secret value is needed to complete a task, stop and "
    "ask the user to check or provide it."
)


def _sanitize(text: str) -> str:
    """Remove references to .env.example before secret-pattern checks.

    .env.example is a safe template file — not a secret. Without this step,
    the .env pattern would match the .env prefix inside .env.example.
    """
    return re.sub(r"\.env\.example\b", "", text)


def _blocked_label(text: str) -> str | None:
    """Return a human-readable label if text references a secret file, else None."""
    sanitized = _sanitize(text)
    for pattern, label in _RULES:
        if pattern.search(sanitized):
            return label
    return None


def _deny(label: str) -> None:
    result = {
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": (
                f"Blocked: command references a {label}. "
                f"Agents must not read or write secret files directly. "
                f"{_GUIDANCE}"
            ),
        }
    }
    json.dump(result, sys.stdout)
    sys.exit(0)


def main() -> None:
    try:
        data = json.load(sys.stdin)
    except (json.JSONDecodeError, EOFError):
        return

    tool_name = data.get("tool_name", "")
    tool_input = data.get("tool_input", {})

    if tool_name == "Bash":
        cmd = tool_input.get("command", "")
        if cmd:
            label = _blocked_label(cmd)
            if label:
                _deny(label)

    elif tool_name in ("Write", "Edit", "MultiEdit"):
        file_path = tool_input.get("file_path", "")
        if file_path:
            label = _blocked_label(file_path)
            if label:
                _deny(label)


if __name__ == "__main__":
    main()
