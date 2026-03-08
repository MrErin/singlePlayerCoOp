---
description: Audit the test suite for quality, effectiveness, and coverage gaps. Generates investigation cards — small, self-contained tasks for manually verifying and improving tests. Does NOT rewrite code.
allowed-tools: Bash, Read, Write, Grep, Glob
---

# Audit Test Suite

**Skill:** Load `my-style`
**No git commits.**

## Steps

1. **Read**: `_planning/codebase.md` to understand project structure. Read `_planning/requirements.md` for business context.
	1. If the `_planning` directory does not exist, STOP. Instruct the user to run /plan:init first.
2. **Map the test landscape**: Identify all test files, test framework(s), and which source modules have corresponding tests.
3. **Triage**: From `codebase.md`, identify business logic and core modules. Prioritize analysis: business logic > data layer > API/routes > utilities. For large suites, focus on critical modules first.
4. **Analyze by module**: For each module (highest priority first), analyze its test files against the standards below. For every issue found, create an investigation card (templates loaded in step 7).
5. **Get coverage results**: Check for `.coverage` file — if found, run `coverage report` (don't re-run tests). If not found, check `htmlcov/index.html`. If neither exists and a coverage tool is installed, run `pytest --cov=src --cov-report=html` in the background. If no coverage tool is installed, note in setup section and skip.
6. **Get mutation testing results**: Check for `.mutmut-cache` — if found, run `mutmut results`. If not found, run `mutmut run` in the background. Incorporate surviving mutants as cards in step 8.
7. **For trivial fixes, just make the edits**: Weak assertions (>= where == should be), untested fields in a return object, or other obvious improvements — fix them during the audit. If collected trivial fixes break tests, hand back to user as one card.
8. **Generate output**: Read `commands/plan/references/test-audit-templates.md` for card and document templates. Generate `_planning/test_audit.md`.
9. **Generate cards**: Create investigation cards, organize into clusters by source module. Within each cluster, order hardest-to-easiest. Assign a BOSS card to any cluster with 3+ issues.
10. **Classify** each card: Quick (10-15 min), Medium (20-30 min), Deep Dive (30-45 min).
11. **Progressive output**: If >10 cards generated, produce the full scorecard, standards check, and cluster summary tables, but only expand full card details for the top 2 clusters. Add a note: "Run `/plan:test-audit [cluster-name]` to expand remaining clusters."

## Standards to Evaluate Against

Evaluate against `my-style` testing standards (load `references/testing.md`). Additionally check these audit-specific concerns:

### Test Design
- [ ] Each test verifies one logical concept
- [ ] Test names describe scenario and expected outcome
- [ ] No conditional logic (if/else) or assertion-generating loops inside tests
- [ ] Setup/teardown is proportional to what's being tested
- [ ] No two tests exercise the exact same code path with the same assertions

### Test Independence
- [ ] Tests don't depend on execution order
- [ ] Tests don't share mutable state
- [ ] No external resource dependencies without mocking
- [ ] No sleep/timing-dependent assertions

### Obsolete Tests
- [ ] No tests reference functions, classes, or modules that no longer exist
- [ ] No tests cover behavior that has been removed or replaced
- [ ] Tests for renamed functionality have been updated

## Rules

- Do not rewrite code in codebase
- Prefer reading existing `.mutmut-cache` over re-running
- Provide brief corrected examples when fix is obvious
- Explain WHY the test is insufficient — connect to bugs it would miss
- Cluster cards by source module

$ARGUMENTS
