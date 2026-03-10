---
description: Audit the test suite for quality, effectiveness, and coverage gaps. Generates investigation cards — small, self-contained tasks for manually verifying and improving tests. Does NOT rewrite code.
allowed-tools: Bash, Read, Write, Edit, Grep, Glob
---

# Audit Test Suite

**Skill:** Load `my-style`
**No git commits.**

## Steps

1. **Read**: `_planning/codebase.md` to understand project structure. Read `_planning/requirements.md` for business context.
	1. If the `_planning` directory does not exist, STOP. Instruct the user to run /plan:init first.
2. **Index with jcodemunch**: If not already indexed, run `index_folder` on the source directory. Use `search_symbols` to find test files and `get_file_outline` to see test structure.
3. **Map the test landscape**: Identify all test files, test framework(s), and which source modules have corresponding tests. Use jcodemunch `search_text` to find test file patterns.
4. **Triage**: From `codebase.md`, identify business logic and core modules. Prioritize analysis: business logic > data layer > API/routes > utilities. For large suites, focus on critical modules first.
5. **Analyze by module**: For each module (highest priority first), analyze its test files against the standards below. For every issue found, create an investigation card (templates loaded in step 7). Use jcodemunch `get_file_outline` to see all test functions in each file.
6. **Get coverage results**: Check for `.coverage` file — if found, run `coverage report` (don't re-run tests). If not found, check `htmlcov/index.html`. If neither exists and a coverage tool is installed, run `pytest --cov=src --cov-report=html` in the background. If no coverage tool is installed, note in setup section and skip.
7. **Get mutation testing results**: Check for `.mutmut-cache` — if found, run `mutmut results`. If not found, run `mutmut run` in the background. Incorporate surviving mutants as cards in step 8.
8. **For trivial fixes, just make the edits**: Weak assertions (>= where == should be), untested fields in a return object, or other obvious improvements — fix them during the audit. If collected trivial fixes break tests, hand back to user as one card.
9. **Generate output**: Read `commands/plan/references/test-audit-templates.md` for card and document templates. Generate `_planning/test_audit.md`.
10. **Generate cards**: Create investigation cards, organize into clusters by source module. Within each cluster, order hardest-to-easiest. Assign a BOSS card to any cluster with 3+ issues.
11. **Classify** each card: Quick (10-15 min), Medium (20-30 min), Deep Dive (30-45 min).
12. **Progressive output**: If >10 cards generated, produce the full scorecard, standards check, and cluster summary tables, but only expand full card details for the top 2 clusters. Add a note: "Run `/plan:test-audit [cluster-name]` to expand remaining clusters."

## Standards to Evaluate Against

All tests evaluated against `my-style/testing.md`. Quick reference for what to flag:

| Category | What to Check For |
|----------|-------------------|
| **Test Design** | One concept per test, descriptive names, no conditionals, proportional setup, no section dividers |
| **Test Independence** | Order-independent, no shared mutable state, no timing dependencies |
| **Assertion Quality** | All fields asserted, exact counts (not `>=`), no tautologies or mirror tests |
| **Coverage** | Edge cases, error paths, negative tests (minimum 1:2 ratio with happy path) |
| **Seam Tests** | Module boundaries have integration tests, not just mocked unit tests |
| **Redundancy** | No duplicate tests exercising same code path with same assertions |
| **Obsolete Tests** | Tests track renamed/removed code, no orphan tests for deleted functions |
| **Parallel Coverage** | Similar modules (same pattern) have similar test coverage |
| **AI Anti-Patterns** | See `my-style/references/antipatterns.md` Testing section: mirror tests, no assertions, over-mocked, tautological assertions |

When multiple modules share architecture (e.g., all repos have `create_many()`), check that edge case tests in one module exist in siblings. A bug fix without parallel tests invites regression.

## Rules

- Do not rewrite production code. Trivial test fixes (step 8) are allowed.
- Prefer reading existing `.mutmut-cache` over re-running
- Provide brief corrected examples when fix is obvious
- Explain WHY the test is insufficient — connect to bugs it would miss
- Cluster cards by source module

$ARGUMENTS
