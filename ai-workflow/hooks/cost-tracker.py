#!/usr/bin/env python3
"""Stop hook: track session cost by parsing the conversation transcript.

Reads the JSONL transcript referenced by the Stop event's transcript_path,
extracts token usage and model information, estimates USD cost, and appends
a JSONL row to ~/.claude/metrics/costs.jsonl.

If the transcript lacks usage data (common with non-Anthropic proxies like
GLM), the hook logs a session record with null usage fields rather than
failing silently.
"""
import json
import os
import sys
from datetime import datetime, timezone

# Anthropic pricing per million tokens (input / output).
# https://docs.anthropic.com/en/docs/about-claude/pricing
PRICING: dict[str, tuple[float, float]] = {
    "claude-haiku-4-5-20251001": (0.80, 4.00),
    "claude-sonnet-4-6": (3.00, 15.00),
    "claude-opus-4-6": (15.00, 75.00),
    "claude-3-5-haiku-20241022": (0.80, 4.00),
    "claude-3-5-sonnet-20241022": (3.00, 15.00),
    "claude-3-5-haiku-latest": (0.80, 4.00),
    "claude-3-5-sonnet-latest": (3.00, 15.00),
    "claude-3-opus-20240229": (15.00, 75.00),
}

# GLM proxy pricing — add or update as needed.
# GLM sessions may not report token usage in the transcript.
GLM_PRICING: dict[str, tuple[float, float]] = {
    "glm-5-turbo": (0.00, 0.00),  # placeholder — fill in actual GLM pricing
}

METRICS_DIR = os.path.expanduser("~/.claude/metrics")
COSTS_FILE = os.path.join(METRICS_DIR, "costs.jsonl")


def _estimate_cost(model: str, input_tokens: int, output_tokens: int) -> float:
    """Estimate USD cost for a given model and token counts."""
    rates = PRICING.get(model) or GLM_PRICING.get(model)
    if not rates:
        return 0.0
    input_cost = (input_tokens / 1_000_000) * rates[0]
    output_cost = (output_tokens / 1_000_000) * rates[1]
    return input_cost + output_cost


def _parse_transcript(transcript_path: str) -> dict:
    """Parse the JSONL transcript for usage and model data.

    Returns dict with keys: model, input_tokens, output_tokens,
    cache_read_tokens, cache_creation_tokens, num_turns.
    """
    result = {
        "model": None,
        "input_tokens": 0,
        "output_tokens": 0,
        "cache_read_tokens": 0,
        "cache_creation_tokens": 0,
        "num_turns": 0,
    }

    path = os.path.expanduser(transcript_path)
    if not os.path.isfile(path):
        return result

    try:
        with open(path, encoding="utf-8") as f:
            lines = f.readlines()
    except OSError:
        return result

    for line in lines:
        line = line.strip()
        if not line:
            continue
        try:
            entry = json.loads(line)
        except json.JSONDecodeError:
            continue

        # Count conversation turns (user messages)
        entry_type = entry.get("type", "")
        if entry_type in ("user", "human"):
            result["num_turns"] += 1

        # Extract model name from entries that have it
        if not result["model"]:
            model = entry.get("model")
            if model and isinstance(model, str):
                result["model"] = model

        # Extract usage data from entries that have it
        usage = entry.get("usage")
        if isinstance(usage, dict):
            result["input_tokens"] += usage.get("input_tokens", 0) or 0
            result["output_tokens"] += usage.get("output_tokens", 0) or 0
            result["cache_read_tokens"] += (
                usage.get("cache_read_input_tokens", 0) or 0
            )
            result["cache_creation_tokens"] += (
                usage.get("cache_creation_input_tokens", 0) or 0
            )

    return result


def main() -> None:
    try:
        data = json.load(sys.stdin)
    except (json.JSONDecodeError, EOFError):
        return

    session_id = data.get("session_id", "unknown")
    transcript_path = data.get("transcript_path", "")

    usage = _parse_transcript(transcript_path)

    model = usage["model"] or os.environ.get("ANTHROPIC_MODEL", "unknown")
    input_tokens = usage["input_tokens"]
    output_tokens = usage["output_tokens"]
    cost = _estimate_cost(model, input_tokens, output_tokens)

    record = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "session_id": session_id,
        "model": model,
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "cache_read_tokens": usage["cache_read_tokens"],
        "cache_creation_tokens": usage["cache_creation_tokens"],
        "num_turns": usage["num_turns"],
        "estimated_cost_usd": round(cost, 6),
        "has_usage_data": bool(input_tokens or output_tokens),
    }

    os.makedirs(METRICS_DIR, exist_ok=True)
    with open(COSTS_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(record) + "\n")


if __name__ == "__main__":
    main()
