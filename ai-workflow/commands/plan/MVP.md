---
description: Conduct a full requirements interview for a new project. Produces _planning/requirements.md through conversation. Run before /plan:init. Use for greenfield projects only — for features on an existing codebase, use /plan:feature instead.
allowed-tools: Read, Write, Glob
---

# MVP Requirements Interview

## Purpose

Produce `_planning/requirements.md` through conversation — not a template. Challenge vague answers, name tradeoffs, synthesize into a running draft.

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

## Product Brief Integration

Check for `[slug]-product-brief.md` in the current or parent directory. If found:

1. Read it. Treat business-layer decisions (customer, monetization, positioning) as settled ground — don't re-ask.
2. Note in the running draft: `**Product brief:** [filename] incorporated`
3. Focus the interview on technical decisions the brief doesn't cover.

## Backlog Integration

Check if `_planning/backlog/` exists. If it does:

1. Ask: "Do you have backlog items to incorporate? Reference them by ID (e.g., F-008, B-003) or say 'no' to skip."
2. If yes: read the referenced entries and any linked specs. Use their descriptions as seed context — the user shouldn't have to re-explain ideas already captured.
3. At the end of the interrogation: update each referenced item's status from `open` to `planned`, and add `**Incorporates:** F-008, B-003` to the requirements doc.

## Running Draft

Create `_planning/requirements.md` before the first question. Update after each section. User can stop anytime and have useful output.

## Interview Sequence

Load `commands/plan/references/requirements-guide.md` for detailed probing questions.

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
