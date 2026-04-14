#!/usr/bin/env python3
"""Stop hook: write a notification file when Claude finishes responding.

Since the fish tank is a headless container, this writes a notification
file to the mounted volume at /project/.claude/notification. The host
machine can watch for changes to this file (e.g., with fswatch, inotify,
or a polling script) and surface a native OS notification.

The notification file is a single JSON line with timestamp, session ID,
and the first 100 characters of the last assistant message.
"""
import json
import os
import sys
from datetime import datetime, timezone

NOTIFICATION_DIR = "/project/.claude"
NOTIFICATION_FILE = os.path.join(NOTIFICATION_DIR, "notification")
MESSAGE_TRUNCATE = 100


def main() -> None:
    try:
        data = json.load(sys.stdin)
    except (json.JSONDecodeError, EOFError):
        return

    session_id = data.get("session_id", "unknown")
    last_message = data.get("last_assistant_message", "")

    # Truncate message for notification body
    if last_message and len(last_message) > MESSAGE_TRUNCATE:
        body = last_message[:MESSAGE_TRUNCATE].rstrip() + "…"
    else:
        body = last_message.strip()

    notification = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "session_id": session_id,
        "type": "claude-completion",
        "body": body,
    }

    os.makedirs(NOTIFICATION_DIR, exist_ok=True)
    with open(NOTIFICATION_FILE, "w", encoding="utf-8") as f:
        f.write(json.dumps(notification) + "\n")


if __name__ == "__main__":
    main()
