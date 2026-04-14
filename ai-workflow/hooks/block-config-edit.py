#!/usr/bin/env python3
"""PreToolUse hook: block edits to linter and formatter config files.

Prevents the agent from weakening linting rules instead of fixing code.
This is a known LLM failure mode — agents "fix" lint errors by loosening
the linter rather than addressing the underlying issue.

For pyproject.toml, only blocks edits that touch tool sections that
contain linting/testing configuration. Edits to [project], [build-system],
dependencies, and other non-linting sections are allowed.
"""
import json
import sys

# Files to block entirely (no parsing needed — all content is config)
BLOCKED_FILES = {
    "ruff.toml",
    ".ruff.toml",
    "eslint.config.js",
    "eslint.config.mjs",
    "eslint.config.cjs",
    ".eslintrc",
    ".eslintrc.js",
    ".eslintrc.json",
    ".eslintrc.yml",
    ".eslintrc.yaml",
    ".eslintrc.cjs",
    ".prettierrc",
    ".prettierrc.js",
    ".prettierrc.json",
    ".prettierrc.yml",
    ".prettierrc.yaml",
    ".prettierrc.cjs",
    ".prettierrc.toml",
    "biome.json",
    "biome.jsonc",
    "tslint.json",
    ".stylelintrc",
    ".stylelintrc.js",
    ".stylelintrc.json",
    ".stylelintrc.yml",
    ".stylelintrc.yaml",
    ".stylelintrc.cjs",
}

# pyproject.toml sections that contain linting/testing config.
# Edits touching these sections are blocked.
BLOCKED_TOML_SECTIONS = [
    "[tool.ruff",
    "[tool.mypy",
    "[tool.pytest",
    "[tool.coverage",
    "[tool.mutmut",
    "[tool.hypothesis",
    "[tool.pylint",
    "[tool.flake8",
    "[tool.isort",
    "[tool.black",
    "[tool.bandit",
]

_GUIDANCE = (
    "Fix the code to satisfy the linter rule rather than weakening the rule. "
    "If a rule is genuinely wrong, ask the user to modify the config manually."
)


def _filename_matches(file_path: str) -> bool:
    """Check if the file_path matches a fully-blocked config filename."""
    filename = file_path.rsplit("/", 1)[-1] if "/" in file_path else file_path
    return filename in BLOCKED_FILES


def _toml_section_touched(content: str) -> bool:
    """Check if content modifies a blocked pyproject.toml section.

    Looks for section headers (e.g., '[tool.ruff') and key assignments
    within those sections. Only flags edits that clearly target a blocked
    section — not edits to unrelated parts of the file.
    """
    if not content:
        return False

    for section in BLOCKED_TOML_SECTIONS:
        if section in content:
            return True

    return False


def main() -> None:
    try:
        data = json.load(sys.stdin)
    except (json.JSONDecodeError, EOFError):
        return

    tool_name = data.get("tool_name", "")
    if tool_name not in ("Write", "Edit", "MultiEdit"):
        return

    file_path = data.get("tool_input", {}).get("file_path", "")
    if not file_path:
        return

    # Check fully-blocked filenames
    if _filename_matches(file_path):
        filename = file_path.rsplit("/", 1)[-1] if "/" in file_path else file_path
        _deny(f"'{filename}' is a linter/formatter config file")

    # Special handling for pyproject.toml — section-aware
    if file_path.endswith("pyproject.toml"):
        tool_input = data.get("tool_input", {})
        content = tool_input.get("content", "") or tool_input.get(
            "new_string", ""
        )
        if _toml_section_touched(content):
            _deny("pyproject.toml linting/testing tool section")


def _deny(label: str) -> None:
    result = {
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": (
                f"Blocked: {label}. {_GUIDANCE}"
            ),
        }
    }
    json.dump(result, sys.stdout)
    sys.exit(0)


if __name__ == "__main__":
    main()
