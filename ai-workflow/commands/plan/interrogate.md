---
description: Conduct a structured requirements interview to produce a completed requirements.md. Adapts to four contexts - new project (full interview), new feature (scoped interview), clarify existing (targeted gaps), or phase shift (insert phases mid-build). Ask one topic at a time, push back on vague answers, discuss tradeoffs critically. Synthesize responses into a running draft that updates after each section. Use before /plan:init on any new project or feature.
allowed-tools: Read, Write, Glob
---

# Requirements Interrogation

## Purpose

Produce `requirements.md` through conversation — not a template. Challenge vague answers, name tradeoffs, synthesize into a running draft.

## Critical Dialogue Principle

**You are not a yes-machine.** The user wants constructive pushback, not passive agreement. Your role is to:

- **Challenge flawed assumptions** — if an approach has hidden costs, name them
- **Propose alternatives** — if there's a better way, explain why it's better
- **Check feasibility** — before committing to a third-party package, verify its capabilities via Context7 or documentation. Never assume "there's probably a library for that"

The user makes final decisions, but expects you to surface tradeoffs, especially in:

| Domain | What to probe |
|--------|---------------|
| **UX Design** | Cognitive load, information hierarchy, discoverability, feedback loops |
| **Gamification** | Intrinsic vs extrinsic motivation, reward schedules, avoidance of dark patterns |
| **Architecture** | Separation of concerns, extensibility, coupling points, state management |
| **Performance** | Query patterns, caching needs, bundle size, render cycles |

If the user suggests something hacky or suboptimal, say so. They're learning too.

## Mode Detection

Read project directory first:

| Mode | Signals | Action |
|------|---------|--------|
| **A: New Project** | No `_planning/` or empty requirements | Full interview |
| **B: New Feature** | `_planning/` exists, codebase exists | Scoped interview |
| **C: Clarify** | requirements.md has content, user wants gaps filled | Targeted interview |
| **D: Phase Shift** | User mentions requirements change, refactoring needed, or unexpected work mid-build | Phase insertion interview |

**Mode B:** Read `roadmap.md`, `decisions.md`, `codebase.md`, phase summaries, `project-requirements/index.md` first. Don't ask what you can learn from context.

**Mode C:** Read `requirements.md` and `decisions.md`. Identify gaps, vague criteria, contradictions. Interview only those areas.

**Mode D:** Read `roadmap.md`, `state.md`, current phase plan, and any relevant phase summaries. Understand what's been built and what's blocked or needs rework.

## Backlog Integration

Before starting the interview (Modes A, B, and C), check if `_planning/backlog/` exists. If it does:

1. Ask: "Do you have backlog items to incorporate? Reference them by ID (e.g., F-008, B-003) or say 'no' to skip."
2. If yes: read the referenced entries from the catalog files, plus any linked specs in `_planning/backlog/specs/`. Use their descriptions as **seed context** — the user shouldn't have to re-explain ideas already captured in the backlog.
3. At the **end** of the interrogation (after the final requirements draft is written):
   - Update each referenced backlog item's status from `open` to `planned`
   - Add an `Incorporates:` line to the requirements doc listing the IDs: `**Incorporates:** F-008, B-003, Q-003`

If `_planning/backlog/` doesn't exist, skip this step silently.

## Running Draft

Create/open `requirements.md` before interviewing. Update after each section. User can stop anytime and have useful output.

## Interview Sequence (Mode A)

Load `commands/plan/references/interrogate-guide.md` for detailed probing questions.

```
[ ] 1. Problem & Purpose
[ ] 2. User Stories
[ ] 3. Tech Stack
[ ] 4. Data Model
[ ] 5. Future Features
[ ] 6. Business Rules
[ ] 7. UI/UX
[ ] 8. Non-Functional Requirements
[ ] 9. Out of Scope
[ ] 10. Coverage Confirmation
```

## Interview Sequence (Mode B)

```
[ ] 1. Read existing context
[ ] 2. Feature definition & user stories
[ ] 3. Integration points
[ ] 4. Data model changes
[ ] 5. Feature-specific business rules
[ ] 6. Feature UI/UX
[ ] 7. Out of scope
[ ] 8. Coverage confirmation
```

## Interview Sequence (Mode D: Phase Shift)

**Trigger:** User indicates requirements have changed, something needs refactoring, or unexpected work is needed mid-build.

```
[ ] 1. Understand the shift
    - What triggered this? (requirements change, discovered technical debt, integration issue)
    - What's blocked or broken without this work?
    - Is this urgent or can it wait until after current phases?
[ ] 2. Scope the new work
    - What specifically needs to be built/changed?
    - Does this affect already-built phases? (may need retroactive fixes)
    - Does this change the data model? (cascading effects)
[ ] 3. Determine phase count
    - Implementation phase needed? (usually yes)
    - Test phase needed? (yes if implementation phase)
    - Total phases to insert: 1-2 typically
[ ] 4. Insertion point
    - After which phase should this be inserted?
    - Confirm: all subsequent phases will be renumbered
[ ] 5. Create phase shift document
    - Write `_planning/phase_shift_requirements_phase[N].md` where N is the NEW phase number after insertion
    - Include: trigger, scope, affected phases, implementation approach
[ ] 6. Update roadmap
    - Insert new phase(s) at the correct position
    - Renumber all subsequent phases (no decimals)
    - Update phase names to reflect new numbering
    - Add note explaining the shift
    - In the **Phase intent notes** section: renumber all shifted entries to match their new phase numbers, then add a new entry for each inserted phase (2-3 sentences: what is built, what is excluded, what done looks like)
```

**After Mode D:** The user can proceed with `/plan:phase [N]` to plan the new phase using the shift requirements document.

## Interview Behavior

- **One topic at a time.** No numbered question lists.
- **Follow up on vague answers.** "Later" is OK for soft decisions, not load-bearing ones.
- **Name tradeoffs honestly.** User can override with information.
- **Park undecided items.** Add to Open Questions, move on.

### Load-Bearing vs Soft

- **Load-bearing (push hard):** data model structure, auth, multi-user, state management
- **Soft (let slide):** field names, UI copy, minor rules

## Rules

- Do NOT run `/plan:init` automatically
- Do NOT ask all questions at once
- DO update draft after each section
- DO use existing context to avoid re-asking

$ARGUMENTS
