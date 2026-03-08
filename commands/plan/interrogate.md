---
description: Conduct a structured requirements interview to produce a completed requirements.md. Adapts to three contexts - new project (full interview from scratch), new feature (scoped to the feature and its integration points), or clarify existing (targeted gap analysis). Ask one topic at a time, push back on vague answers, discuss tradeoffs critically. Synthesize responses into a running draft that updates after each section. Use before /plan:init on any new project or feature.
allowed-tools: Read, Write
---

# Requirements Interrogation

## Purpose

Produce `requirements.md` through conversation — not a template. Challenge vague answers, name tradeoffs, synthesize into a running draft.

**You are not a yes-machine.** If an approach has costs, name them. If a criterion is untestable, say so.

## Mode Detection

Read project directory first:

| Mode | Signals | Action |
|------|---------|--------|
| **A: New Project** | No `_planning/` or empty requirements | Full interview |
| **B: New Feature** | `_planning/` exists, codebase exists | Scoped interview |
| **C: Clarify** | requirements.md has content, user wants gaps filled | Targeted interview |

**Mode B:** Read `roadmap.md`, `decisions.md`, `codebase.md`, phase summaries, `project-requirements/index.md` first. Don't ask what you can learn from context.

**Mode C:** Read `requirements.md` and `decisions.md`. Identify gaps, vague criteria, contradictions. Interview only those areas.

## Running Draft

Create/open `requirements.md` before interviewing. Update after each section. User can stop anytime and have useful output.

## Interview Sequence (Mode A)

Load `references/interrogate-guide.md` for detailed probing questions.

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
- Do NOT make git commits
- Do NOT ask all questions at once
- DO update draft after each section
- DO use existing context to avoid re-asking

$ARGUMENTS
