---
description: Conduct a scoped requirements interview for the next feature on an existing project. Produces a fresh _planning/requirements.md. Only run after /plan:archive has cleared the workspace — stops if requirements.md already exists.
allowed-tools: Read, Write, Glob
---

# Feature Requirements Interview

## Purpose

Produce a fresh `_planning/requirements.md` for the next feature through conversation. Reads existing project context so settled decisions aren't re-litigated. Scoped to the new feature only.

## Precondition Check

Before anything else, check for `_planning/requirements.md`:

- **File does not exist** → proceed
- **File exists** → stop immediately:

  > `requirements.md` already exists at `_planning/requirements.md`. This means a feature is already in progress, or the previous feature wasn't fully archived.
  >
  > Run `/plan:archive` to close out the current feature and clear the workspace, then run `/plan:feature` again.

Do not proceed past this check if the file exists.

## Load Existing Context

Read the following as settled ground — do not re-ask decisions already made here:

- `_planning/project-requirements/index.md` (and any linked requirement files) — permanent capabilities and constraints
- `_planning/decisions.md` — architectural decisions
- `_planning/codebase.md` — stack, structure, current state
- `_planning/lessons.md` — issues caught in prior builds worth carrying forward

## Critical Dialogue Principle

**You are not a yes-machine.** Challenge flawed assumptions, propose alternatives, check feasibility. The user makes final decisions but expects tradeoffs to be named.

| Domain | What to probe |
|--------|---------------|
| **Integration points** | How does this touch what's already built? What breaks if this changes? |
| **Data model changes** | Are new entities or relationships needed? Cascading effects on existing data? |
| **UX Design** | Cognitive load, consistency with existing flows |
| **Architecture** | Does this fit the established patterns, or is there a reason to diverge? |

## Product Brief Integration

Check for `[slug]-product-brief.md` in the current or parent directory. If found:

1. Read it. Treat business-layer decisions as settled ground.
2. Note in the running draft: `**Product brief:** [filename] incorporated`
3. Focus the interview on technical decisions the brief doesn't cover.

## Backlog Integration

Check if `_planning/backlog/` exists. If it does:

1. Ask: "Do you have backlog items to incorporate? Reference them by ID (e.g., F-008, B-003) or say 'no' to skip."
2. If yes: read the referenced entries and any linked specs. Use their descriptions as seed context.
3. At the end: update each referenced item's status from `open` to `planned`, and add `**Incorporates:** F-008, B-003` to the requirements doc.

## Running Draft

Create `_planning/requirements.md` before the first question. Update after each section.

## Interview Sequence

Load `commands/plan/references/requirements-guide.md` for detailed probing questions, focusing on sections relevant to the new feature.

```
[ ] 1. Feature definition & user stories
[ ] 2. Integration points with existing codebase
[ ] 3. Data model changes (if any)
[ ] 4. Feature-specific business rules
[ ] 5. UI/UX for the feature
[ ] 6. Out of scope
[ ] 7. Coverage confirmation
```

## Interview Behavior

- **One topic at a time.** No numbered question lists.
- **Treat existing decisions as settled.** Don't re-litigate architecture from `decisions.md`.
- **Focus pushback on the new feature's specific risks** — integration points, data model changes, and scope creep.
- **Park undecided items.** Add to Open Questions, move on.

### Load-Bearing vs Soft

- **Load-bearing (push hard):** data model changes, auth implications, multi-user effects, integration points that touch existing logic
- **Soft (let slide):** field names, UI copy, minor rules

## Rules

- Do NOT proceed if `requirements.md` already exists
- Do NOT run `/plan:init` automatically
- Do NOT re-ask questions answered in `decisions.md` or `project-requirements/`
- DO update draft after each section

$ARGUMENTS
