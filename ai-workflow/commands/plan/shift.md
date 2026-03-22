---
description: Handle mid-build requirements changes, phase insertions, or requirements gaps. Use when something unexpected comes up during a build — new work is discovered, a requirement needs clarification, or phases need to be inserted.
allowed-tools: Read, Write, Glob
---

# Phase Shift

## Purpose

Handle anything that comes up mid-build that can't wait for the next feature cycle: a requirements gap, a discovered need for new work, or a change in direction. Determines through conversation whether the situation needs a requirements update, new phase(s), or both.

## Load Current State

Before the first question, read:

- `_planning/roadmap.md` — what's planned and what's been built
- `_planning/state.md` — current phase and status
- The current phase's `plan.md` (if it exists) — what's in flight
- Recent phase summaries — what's already been built
- `_planning/requirements.md` — current active scope
- `_planning/decisions.md` — settled architectural decisions

Don't ask what you can learn from context.

## Understand the Shift

Start here:

1. **What triggered this?** (Requirements change, discovered technical debt, integration issue, scope gap)
2. **What's blocked or at risk without addressing it?**
3. **Is this urgent, or can it wait until after the current phase?**

If it can wait, say so and suggest adding it to `_planning/deferred.md` instead.

## Determine the Output

Based on the conversation, determine what's actually needed:

| Situation | Output |
|-----------|--------|
| Gap in existing requirements — no new phases needed | Update `_planning/requirements.md` directly |
| New work required — current phases can't absorb it | Phase shift: new `phase_shift_requirements_phase[N].md` + roadmap update |
| Both — gap in requirements AND new phases needed | Both outputs |

Don't decide this before the conversation. Let the scope reveal itself.

## Requirements Gap (no new phases)

If the issue is a clarification or gap in existing requirements:

- Update `_planning/requirements.md` with the missing or corrected content
- Note the change at the bottom of the file: `**Updated [date]:** [one-line summary of what changed and why]`
- No new phases, no roadmap change

## Phase Insertion

If new phases are needed:

```
[ ] 1. Scope the new work
    - What specifically needs to be built or changed?
    - Does this affect already-built phases? (may need retroactive fixes)
    - Does this change the data model? (cascading effects)
[ ] 2. Determine phase count
    - Implementation phase needed? (usually yes)
    - Test phase needed? (yes if implementation phase)
    - Total phases to insert: typically 1–2
[ ] 3. Insertion point
    - After which existing phase should this be inserted?
    - Confirm: all subsequent phases will be renumbered
[ ] 4. Create shift document
    - Write `_planning/phase_shift_requirements_phase[N].md` where N is the new phase number
    - Include: trigger, scope, affected phases, implementation approach
[ ] 5. Update roadmap
    - Insert new phase(s) at the correct position
    - Renumber all subsequent phases (no decimals)
    - Add note explaining the shift
    - In the Phase intent notes section: renumber shifted entries, add entries for inserted phases
```

## After Phase Shift

Tell the user: "Run `/plan:phase [N]` to plan the new phase using the shift requirements document."

## Interview Behavior

- **One topic at a time.**
- **Treat existing decisions as settled.** Don't re-open closed questions from `decisions.md`.
- **Determine urgency first.** If it can be deferred, say so.
- **Be concrete about impact.** Name which phases are affected and how.

## Rules

- Do NOT suggest deferring something the user says is blocking
- Do NOT open new phases speculatively — scope must justify it
- DO update `requirements.md` even for small gaps — don't leave undocumented changes
- DO renumber roadmap phases correctly — no decimals, no gaps

$ARGUMENTS
