---
description: Audit the test suite for quality, effectiveness, and coverage gaps. Generates investigation cards — small, self-contained tasks for manually verifying and improving tests. Does NOT rewrite code.
allowed-tools: Bash, Read, Write, Edit, Grep, Glob
---

# Audit Test Suite

**Skill:** Load `my-style`

## Resume Detection

Before starting, check if `_planning/test_audit.md` exists with `<!-- STATUS: DRAFT -->`. If so, read it to identify which clusters/modules are already written. Continue from the next unwritten section — do not redo completed analysis.

## Steps

1. **Read**: `_planning/codebase.md` to understand project structure. Read `_planning/requirements.md` for business context.
	1. If the `_planning` directory does not exist, STOP. Instruct the user to run /plan:init first.
2. **Index with jcodemunch**: If not already indexed, run `index_folder` on the source directory. Use `search_symbols` to find test files and `get_file_outline` to see test structure.
3. **Map the test landscape**: Identify all test files, test framework(s), and which source modules have corresponding tests. Use jcodemunch `search_text` to find test file patterns.
4. **Triage**: From `codebase.md`, identify business logic and core modules. Prioritize analysis: business logic > data layer > API/routes > utilities. For large suites, focus on critical modules first.
5. **Scaffold the document**: Read `commands/plan/references/test-audit-templates.md` for templates. Write `_planning/test_audit.md` with `<!-- STATUS: DRAFT -->`, the document header, and the module priority list. This file is now the working output — all subsequent findings are appended here.
6. **Get coverage results**: Check for `.coverage` file — if found, run `coverage report` (don't re-run tests). If not found, check `htmlcov/index.html`. If neither exists and a coverage tool is installed, run `pytest --cov=src --cov-report=html` in the background. If no coverage tool is installed, note in setup section and skip. **Append results to the document.**
7. **Get mutation testing results**: Check for `.mutmut-cache` — if found, run `mutmut results`. If not found, run `mutmut run` in the background. **Append results to the document.**
8. **Analyze by module** (highest priority first): For each module, analyze its test files against the standards below. Use jcodemunch `get_file_outline` to see all test functions in each file. Create investigation cards for every issue. Classify each card: Quick (10-15 min), Medium (20-30 min), Deep Dive (30-45 min). **Write the completed cluster to the document before moving to the next module.** Within each cluster, order hardest-to-easiest. Assign a BOSS card to any cluster with 3+ issues.
9. **Trivial fixes**: Weak assertions (>= where == should be), untested fields in a return object, or other obvious improvements — fix them during the audit. If collected trivial fixes break tests, hand back to user as one card.
10. **Finalize**: Generate the scorecard and standards check summary at the top of the document (now that all clusters are written). Replace `<!-- STATUS: DRAFT -->` with `<!-- STATUS: COMPLETE -->`.
11. **Progressive output**: If >10 cards generated, only expand full card details for the top 2 clusters. Add a note: "Run `/plan:test-audit [cluster-name]` to expand remaining clusters."

## Standards to Evaluate Against

All tests evaluated against `my-style/testing.md`. Quick reference for what to flag:

| Category | What to Check For |
|----------|-------------------|
| **Test Class Naming** | `Test[Feature]` or `Test[Feature][Category]`; `CRUD` classes must test all four operations; no vague names like `TestUser` |
| **Test Method Naming** | Behavior-focused: `test_[action]_[condition]_[result]`; no method-coupled names like `test_login` |
| **Test Design** | One concept per test, descriptive names, no conditionals, proportional setup, no section dividers |
| **Test Independence** | Order-independent, no shared mutable state, no timing dependencies |
| **Assertion Quality** | All fields asserted, exact counts (not `>=`), no tautologies or mirror tests |
| **Coverage** | Edge cases, error paths, negative tests (minimum 1:2 ratio with happy path) |
| **Suite Structure** | Repos have CRUD tests; services have happy/validation/business-rule tests; APIs have auth/success/error tests |
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
