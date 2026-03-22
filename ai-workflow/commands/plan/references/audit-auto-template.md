# Auto-Fix List Templates

Load this file when ready to generate `audit-auto.md` output.

---

## Purpose

`audit-auto.md` is designed to be handed to an agent (e.g., GLM) for autonomous execution.

It contains only items that require no human judgment — no architectural decisions, no tradeoffs, no ambiguity. The agent should work through items in order and escalate anything that turns out to be more complex than described.

**Format principles:**
- Each item: unique ID, location, imperative action, one-line why, done criteria
- No emojis in item bodies, no lengthy context, no options — just what the agent needs to reason about edge cases
- Grouped by module so the agent works file-by-file
- Escalations section at the bottom for items the agent flags after starting work

---

## Item Format

```
- [ ] AUTO-NNN `path/to/file.py:line` — [imperative action]
  Why: [one sentence — enough to reason about edge cases, not enough to debate tradeoffs]
  Done: [one sentence — observable completion criteria]
```

---

## audit-auto.md Document Template

```markdown
# Audit Auto-Fix List — [Project Name]

**Date**: [today's date]
**Total items**: [n] across [n] modules
**Source audit**: `_planning/audit-review.md`

> **Instructions for executing agent**: Work through items in order within each module.
> If an item is more complex than described — requires architectural judgment, touches shared interfaces,
> or has ambiguous callers — add it to the Escalations section at the bottom and skip it.
> Do NOT attempt fixes that require tradeoffs or could affect other modules unexpectedly.
>
> **Renames require a mandatory protocol:**
> 1. Grep for the symbol across the entire codebase first
> 2. Enumerate ALL matches: imports, usages, tests, docstrings, comments, string literals
> 3. Verify each match is the same symbol (not a homonym)
> 4. Update ALL matches in a single pass
>
> **Escalate renames if:** >20 matches, spans config/migrations, or symbol name has false-positive risk (e.g., `process`, `handle`).
> **Safe to auto-fix if:** <10 matches, confined to source/test files, no ambiguity.

---

## [Module Name]

`[module path]`

- [ ] AUTO-001 `path/to/file.py:12` — Remove unused import `os`
  Why: Never referenced in this file; leftover from a previous refactor
  Done: Import removed; no remaining references to `os` in file

- [ ] AUTO-002 `path/to/file.py:34` — Add type hint `-> int` to `calculate_total`
  Why: Missing return type annotation; return value is always an integer
  Done: Type hint added; function signature is `def calculate_total(...) -> int:`

---

## [Next Module Name]

`[module path]`

...

---

## ⚠️ Escalations

> Add entries here for items that turned out to require human judgment after you started.
> Do NOT attempt these — flag them and move on. The human will review this section.

| ID | Reason |
|----|--------|
| | |
```
