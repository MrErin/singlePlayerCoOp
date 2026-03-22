# Project Roadmap

## Project: [Name]

Requirements: [path to requirements file] Created: [date]

## Phases

[Generated dynamically based on project scope. Phase names describe the actual work.] [Example:]

- [ ] Phase 1: Project setup
- [ ] Phase 2: Schema and models
- [ ] Phase 3: Exercise read operations
- [ ] Phase 4: User CRUD
- [ ] Phase 5: Exercise logging and validation
- [ ] Phase 6: Tests for phases 3-5
- [ ] Phase 7: XP calculation engine
- [ ] Phase 8: Tests for phase 7
- [ ] Phase 9: Dashboard and stats display
- [ ] Phase 10: Styling and accessibility

[Delete the example above and replace with actual phases for this project.]

## Phase intent notes (written at init)

[2-3 sentences per phase capturing scope boundary and key deliverables. Written once at init and updated when phases are inserted. Not updated during builds — this is planning context, not a changelog.]

**Phase 1 (Project setup):** [example]
**Phase 2 (Schema and models):** [example]

## Notes

[Any scope adjustments, phase splits, or other context]

## Audit Checkpoints

> **User-initiated audits** — run `/plan:audit` at these optimal points. Not automated, just guidance.

| Checkpoint | Trigger | Why |
|------------|---------|-----|
| **First Logic** | After first read/write/logic phase group, before its test phase | Early drift caught; basic tests exist for validation |
| **Pre-Architecture** | Before adding a major subsystem (auth, notifications, etc.) | Validate foundation before building on it |
| **Mid-Project** | ~50% through implementation phases | Prevent late-game debt avalanche |
| **Pre-Polish** | Before final polish/cleanup phase | Clean slate for finish work |

**How to use:** When you reach a checkpoint, run `/plan:audit` if you've made manual fixes outside the workflow or feel uncertainty about accumulated drift. Skip if the last audit was recent or phases have been clean.