---
name: iterative-build
description: Build applications in digestible phases with persistent planning state. Use for new apps, features, or multi-step development tasks. Works with /plan: commands.
allowed-tools: Bash, Read, Write, Edit, Grep, Glob
---

# Core Principle

Build in digestible phases. Maintain persistent planning state. Never build everything at once. Always stop after each phase for human review.

**CRITICAL:** Load `my-style` skill when using this one.

# Slash Commands

| Command | Purpose |
|---------|---------|
| `/plan:interrogate` | Requirements interview |
| `/plan:init` | Initialize `_planning/` directory |
| `/plan:phase` | Plan next/specified phase |
| `/plan:build` | Execute current phase |
| `/plan:status` | Show progress, suggest next |
| `/plan:review` | Generate testing doc |
| `/plan:debt` | Technical debt assessment |
| `/plan:test-audit` | Test suite audit |
| `/plan:archive` | Archive completed feature |

If command invoked, follow its instructions. Otherwise, determine appropriate phase.

# The `_planning/` Directory

Single source of truth. Any session can read it and know exactly where things stand.

```
_planning/
├── roadmap.md              # Phase breakdown with status
├── state.md                # Current progress, session log, blockers
├── decisions.md            # Architectural decisions (append-only)
├── deferred.md             # Cross-phase flags
├── lessons.md              # Issues caught during builds (append-only)
├── codebase.md             # Stack, structure, architecture
├── requirements.md         # Current active scope
├── technical_debt.md       # Existing codebase problems
├── test_audit.md           # Test suite analysis
├── project-requirements/   # Accumulated permanent requirements
│   ├── index.md            # Dense summaries + file refs
│   ├── core.md             # Non-feature requirements
│   └── [feature].md        # Per-feature permanent requirements
├── archive/                # Frozen snapshots
└── phases/
    └── [NN-name]/
        ├── plan.md
        ├── phase_summary.md
        ├── ua_testing.md
        └── user_feedback.md
```

## Requirements Tiers

**`requirements.md`** — current active scope. Short, focused. Cleared at archive.

**`project-requirements/`** — accumulated project truth. Load `index.md` for full context. Load specific feature file only when phase touches that area.

**If `project-requirements/` doesn't exist:** work from `requirements.md` only.

# Phase System

## Ordering

1. Setup (greenfield only)
2. Data layer
3. Read operations
4. Write operations
5. Business logic
6. Polish

Each phase: 10-20 min review, <15 min test. If >10 tasks, split into multiple phases.

## Test Phases

**Separate phases, not tasks within implementation.**

Why: Agent that wrote implementation has same blind spots when testing.

Rules:
- Test phases receive: interface contracts, function signatures, `my-style/testing.md`
- Test phases do NOT receive: implementation conversation context (enforced by new session)
- Test phases can batch multiple implementation phases
- Business logic test phases require property-based tests

## Context Detection

- **Greenfield:** No code → setup phase
- **Feature Addition:** Code exists → skip setup, generate `codebase.md` if missing
- **Resuming:** `_planning/` exists → read `state.md`, continue

If unclear: "I see existing code and `_planning/`. Continue previous work, add feature, or start fresh?"

# Critical Rules

- Never proceed without permission. STOP after each phase.
- Phase boundaries are strict.
- Keep phases reviewable.
- One plan per phase.
- **Incremental writes:** When generating documents (plans, audits, reviews), write to disk after each major section — not at the end. If the session ends mid-task, partial work survives. Mark documents `<!-- STATUS: DRAFT -->` at the top while in progress, replace with `<!-- STATUS: COMPLETE -->` when done. On resume, check for DRAFT files and continue from the last written section.

# Reference Files (Lazy Load)

| File | Load When |
|------|-----------|
| `references/roadmap.md` | Creating/updating roadmap |
| `references/state.md` | Creating/updating state |
| `references/decisions.md` | Creating decisions file |
| `references/lessons.md` | Creating lessons file |
| `references/phase_plan.md` | Writing a phase plan |
| `references/phase_summary.md` | Writing phase summary |
| `references/ua_testing.md` | Writing testing doc |
| `references/codebase.md` | Documenting codebase structure |

**Do NOT preload references.**

# Integration

- **my-style**: Coding standards (always)
- **post-build-review**: Final review (project end)
- **Domain skills**: Project-specific requirements

# Notes

- User has ADHD — clear structure and STOP points prevent overwhelm
- `_planning/` is memory across sessions
- Always read state.md before starting
- Always update state.md after completing
