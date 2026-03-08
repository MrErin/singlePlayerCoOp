# Phase Workflow

Load this file when executing phases. Contains before/after phase procedures.

## Before Each Phase

Automatically and silently:

1. Read `state.md` → current progress
2. Read `roadmap.md` → phase context
3. Read `codebase.md` → structure and stack
4. Read previous phase artifacts (plan.md, phase_summary.md)
5. Check for user code modifications since last phase
6. Read `decisions.md` → constraints
7. Read `deferred.md` → items targeting this phase
8. If integrating with existing functionality: read `project-requirements/index.md`
9. Adapt plan to incorporate changes

## After Each Phase

1. Create `ua_testing.md` in phase directory
2. Create `user_feedback.md` in phase directory
3. Update `state.md` with completion status and session log
4. Update `roadmap.md` checkbox
5. Update `deferred.md` — add/remove items
6. If structure changed: update `codebase.md`
7. Output completion message with testing checklist
8. **STOP. Wait for approval.**

All three artifacts (ua_testing.md, user_feedback.md, phase_summary.md) required for every phase.
