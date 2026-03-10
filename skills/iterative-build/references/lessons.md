# Lessons Learned

This file captures issues discovered during builds so future planning can avoid repeating known pitfalls.

## Format

Each entry follows this structure:

```
## [YYYY-MM-DD] [Phase] - [Brief Title]

**What happened:** [Description of the issue caught during verification]

**Root cause:** [Why it occurred]

**Fix applied:** [How it was resolved]

**Prevention:** [What to check/avoid in future phases]
```

## Entries

[Lessons will be appended here as issues are discovered during builds]

---

## Example Entry: Environment Mismatch

```
## [2026-03-10] [Phase 8] - Environment mismatch: Python version

**What happened:** All third-party imports failed with ModuleNotFoundError. Agent created MagicMock workarounds in production code instead of diagnosing the environment.

**Root cause:** Docker container runs Python 3.11 but venv was created with Python 3.10. Packages exist in `.venv/lib/python3.10/site-packages/` but Python 3.11 looks for `python3.11/site-packages/`.

**Fix applied:** User fixed Docker image to use matching Python version. Reverted mock workarounds from production code.

**Prevention:** Run environment preflight check before each phase. When imports fail, check if package files exist on disk before concluding they're missing. Never add mocks to production code to work around environment issues.
```
