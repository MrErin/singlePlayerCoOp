#!/usr/bin/env python3
"""PreToolUse hook: block agent from running full test suites.

The fish tank environment creates friction with test running — missing
packages, version mismatches, seccomp blocks. Full-suite runs also consume
context and create fix-rerun-fix churn.

New model: user runs tests and pastes results. Agent may run targeted tests
(single file or test class) for mid-fix verification only.

Blocked:
  pytest (no arguments or broad flags like -x, -v, --tb)
  python3 -m pytest (same)
  npm test / npm run test (no file argument)
  npx vitest / npx jest (no file argument)

Allowed:
  pytest path/to/test_file.py
  pytest path/to/test_file.py::TestClass
  pytest path/to/test_file.py::TestClass::test_method
  pytest --collect-only (collection check, no execution)
  npm test -- path/to/file
  npx vitest path/to/file
"""
import json
import re
import sys


def _is_targeted(args: str) -> bool:
    """Return True if the test command targets a specific file or class."""
    # Strip common flags to find positional args
    # Remove flags like -v, -x, -s, --tb=short, --no-header, -q, etc.
    stripped = re.sub(r"--?\w[\w-]*(?:=\S+)?", "", args).strip()
    # If anything remains after stripping flags, it's a file/class target
    return bool(stripped)


def _check_pytest(cmd: str) -> str | None:
    """Check pytest commands. Returns block reason or None."""
    # Match pytest or python3 -m pytest
    match = re.match(r"(?:python3?\s+-m\s+)?pytest\b(.*)", cmd)
    if not match:
        return None

    args = match.group(1).strip()

    # Always allow collection-only (environment check, no test execution)
    if "--collect-only" in args:
        return None

    # Allow targeted runs (file, class, or method specified)
    if _is_targeted(args):
        return None

    return (
        "Blocked: full test suite run. The user runs the full test suite and "
        "reports results. You may run targeted tests on a specific file or "
        "test class (e.g., `pytest path/to/test_file.py::TestClass`). "
        "Ask the user to run the full suite and paste failures."
    )


def _check_npm(cmd: str) -> str | None:
    """Check npm test commands. Returns block reason or None."""
    match = re.match(r"npm\s+(?:test|run\s+test)\b(.*)", cmd)
    if not match:
        return None

    args = match.group(1).strip()

    # Allow if -- separator with file arguments
    if "--" in args and _is_targeted(args.split("--", 1)[1]):
        return None

    # Allow if file argument directly follows
    if _is_targeted(args):
        return None

    return (
        "Blocked: full test suite run. Ask the user to run `npm test` and "
        "paste the results. You may run targeted tests with a file argument."
    )


def _check_vitest_jest(cmd: str) -> str | None:
    """Check npx vitest/jest commands. Returns block reason or None."""
    match = re.match(r"npx\s+(?:vitest|jest)\b(.*)", cmd)
    if not match:
        return None

    args = match.group(1).strip()

    if _is_targeted(args):
        return None

    return (
        "Blocked: full test suite run. Ask the user to run the test suite and "
        "paste the results. You may run targeted tests with a file argument."
    )


def _check_wrapper(cmd: str) -> str | None:
    """Check coverage-wrapper and mutmut-wrapper commands. Returns block reason or None."""
    if re.match(r"(?:coverage-wrapper|mutmut-wrapper)\b", cmd):
        return (
            "Blocked: test suite wrapper. The user runs test suites and "
            "reports results. Ask the user to run this command and paste "
            "the output."
        )
    return None


def main() -> None:
    try:
        data = json.load(sys.stdin)
    except (json.JSONDecodeError, EOFError):
        return

    if data.get("tool_name") != "Bash":
        return

    cmd = data.get("tool_input", {}).get("command", "").strip()
    if not cmd:
        return

    reason = (
        _check_pytest(cmd)
        or _check_npm(cmd)
        or _check_vitest_jest(cmd)
        or _check_wrapper(cmd)
    )

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
