#!/usr/bin/env python3
"""PreToolUse hook: suggest /compact when context pressure is high.

Tracks tool invocations per session using a temp file keyed by
CLAUDE_SESSION_ID. At 50 calls, suggests running /compact. Every 25
calls after that, repeats the suggestion.

Uses CLAUDE_SESSION_ID env var to scope state to the current session.
Temp files are cleaned up when the session ends (container --rm handles
this automatically).
"""
import json
import os
import sys
import tempfile

# Thresholds
FIRST_NUDGE = 50
REPEAT_INTERVAL = 25

COMPACT_DECISION_TABLE = """\
## When to /compact

| Situation | Compact? |
|-----------|----------|
| After research phase, before implementation | Yes |
| Mid-implementation with interdependent files | No |
| After completing a self-contained task | Yes |
| When context includes stale file reads | Yes |
| During debugging with error context needed | No |

**What survives compaction:** CLAUDE.md, TodoWrite, memory, git state, files on disk.
**What's lost:** intermediate reasoning, file contents previously read, conversation history, verbal preferences.
"""


def _counter_path(session_id: str) -> str:
    """Return a temp file path for the session's tool call counter."""
    tmp_dir = tempfile.gettempdir()
    return os.path.join(tmp_dir, f"claude-tool-count-{session_id}")


def _read_count(path: str) -> int:
    """Read the current count from the counter file."""
    try:
        with open(path, encoding="utf-8") as f:
            return int(f.read().strip())
    except (FileNotFoundError, ValueError):
        return 0


def _write_count(path: str, count: int) -> None:
    """Write the current count to the counter file."""
    try:
        with open(path, "w", encoding="utf-8") as f:
            f.write(str(count))
    except OSError:
        pass


def main() -> None:
    try:
        data = json.load(sys.stdin)
    except (json.JSONDecodeError, EOFError):
        return

    session_id = os.environ.get("CLAUDE_SESSION_ID", "")
    if not session_id:
        return

    path = _counter_path(session_id)
    count = _read_count(path) + 1
    _write_count(path, count)

    # Check if we should nudge
    if count == FIRST_NUDGE or (
        count > FIRST_NUDGE and (count - FIRST_NUDGE) % REPEAT_INTERVAL == 0
    ):
        print(
            f"\n⚠️  Context pressure: {count} tool calls this session. "
            f"Consider running /compact if you've completed a research "
            f"phase or self-contained task.\n{COMPACT_DECISION_TABLE}",
            file=sys.stderr,
        )


if __name__ == "__main__":
    main()
