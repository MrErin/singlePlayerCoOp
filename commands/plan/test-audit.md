---
description: Audit the test suite for quality, effectiveness, and coverage gaps. Generates investigation cards — small, self-contained tasks for manually verifying and improving tests. Does NOT rewrite code. 
allowed-tools: Bash, Read, Write, Grep, Glob
---

# Audit Test Suite

**Skill:** Load `my-style`
**No git commits.**

## Steps

1. **Read**: all documents in the `_planning` directory to understand the project requirements, codebase, and architecture
    1. If the `_planning` directory does not exist, STOP. Instruct the user to run the /plan:init command first
2. **Map the test landscape**: Identify all test files, the test framework(s) in use, and which source modules have corresponding tests
3. **Analyze each test file** against the standards below. For every issue found, create an investigation card (see card templates)
4. **Get coverage results**: Check for an existing `.coverage` file in the project root. If found, run `coverage report` to read it — do not re-run tests. If not found, check for `htmlcov/index.html`. If neither exists and a coverage tool is installed, run `pytest --cov=src --cov-report=html` to generate it. If no coverage tool is installed, note this in the setup section and skip.
5. **Get mutation testing results**: Check for a `.mutmut-cache` file in the project root. If found, run `mutmut results` to read the existing results. If not found, run `mutmut run` to generate them — this may take several minutes depending on project size. Incorporate surviving mutants as cards in step 8.
6. **For any trivial changes, just make the edits**: If there are weak assertions (>= where == should be), untested fields in a return object, or other trivial changes that would improve the test suite, make those changes during the audit rather than handing them back to the user. 
	1. If the collected trivial changes break tests, ask user to handle test adjustments for all trivial fixes as one card in step 8.
7. **Generate**: a file in the `_planning` directory called `test_audit.md` using the template below
8. **Generate cards**: Create investigation cards, then organize them into clusters by source module — all cards covering tests for the same module belong in one cluster. Within each cluster, order cards from hardest to easiest (tackle the deep work while your context is fresh). Assign a BOSS card to any cluster with 3 or more issues.
9. **Classify** each card by difficulty (🟢 Quick 10-15 min, 🟡 Medium 20-30 min, 🔴 Deep Dive 30-45 min)

## Standards to Evaluate Against

### Assertion Quality

- [ ] Every test has at least one meaningful assertion (not just "does not throw")
- [ ] Assertions test behavior/output, not implementation details
- [ ] Assertions have descriptive messages or the test name makes the intent obvious
- [ ] No tautological assertions (always true/always false)
- [ ] Return values from called methods are actually checked

### Test Design

- [ ] Each test verifies one logical concept (not multiple unrelated behaviors)
- [ ] Test names describe the scenario and expected outcome
- [ ] No conditional logic (if/else) inside tests
- [ ] No loops generating dynamic assertions
- [ ] Setup/teardown is proportional to what's being tested (no over-mocking)
- [ ] No two tests exercise the exact same code path with the same assertions

### Coverage Quality (not just quantity)

- [ ] Business logic functions have tests that verify correct AND incorrect inputs
- [ ] Edge cases are covered (nulls, empty collections, boundary values, zero, negative)
- [ ] Error paths are tested, not just happy paths
- [ ] Tests would fail if the core logic changed (not just if an exception is thrown)
- [ ] Pure functions with clear invariants have property-based tests (Hypothesis/fast-check), not just example-based tests
- [ ] Integration boundaries between modules have at least one test exercising the full handoff

### Test Independence

- [ ] Tests don't depend on execution order
- [ ] Tests don't share mutable state
- [ ] No external resource dependencies without mocking (files, network, databases)
- [ ] No sleep/timing-dependent assertions

### AI-Generated Test Red Flags

- [ ] Tests aren't just mirroring the implementation (asserting the same calculation the code does)
- [ ] Tests aren't only checking happy-path with convenient round numbers
- [ ] Test descriptions aren't generic boilerplate ("should work correctly")
- [ ] Mock setups aren't so extensive they've replaced the actual logic being tested

### Obsolete Tests

- [ ] No tests reference functions, classes, or modules that no longer exist
- [ ] No tests cover behavior that has been removed or replaced
- [ ] Tests for renamed functionality have been updated, not left targeting the old name

## Investigation Card Templates

### 🔍 Smell Check Card

```markdown
### 🔍 SMELL-[NNN]: [Smell Name]
- **Difficulty**: [🟢 | 🟡 | 🔴]
- **File**: [test file path]::[test function name]
- **Smell**: [which smell from the standards list]
- **What's suspicious**: [1-2 sentence description of what the agent observed]
- **Your mission**: [specific question to answer or action to take]
- **Done when**: [clear completion criteria]
- **Time box**: [minutes]
```

### 🎯 Coverage Gap Card

```markdown
### 🎯 GAP-[NNN]: [Untested Behavior]
- **Difficulty**: [🟢 | 🟡 | 🔴]
- **Source file**: [production code path]::[function/method name]
- **What's untested**: [specific behavior, branch, or edge case with no test]
- **Why it matters**: [what could go wrong — connect to business logic if possible]
- **Your mission**: Write a test that would catch a bug in this behavior
- **Starter hint**: [suggest what to assert, but not how — per user's graduated approach]
- **Done when**: A new test exists that fails if the described behavior breaks
- **Time box**: [minutes]
```

### 💀 Mutant Hunt Card

> Note: These cards require mutation testing tools to be installed and a mutation run to have been completed. If tools aren't installed yet or haven't been run, this section contains setup instructions instead of cards.

```markdown
### 💀 MUTANT-[NNN]: [Description of the Mutation]
- **Difficulty**: [🟢 | 🟡 | 🔴]
- **Source file**: [production code file]:[line number]
- **Mutation**: [what was changed, e.g., "Changed `>` to `>=`"]
- **Survived?**: Yes — no test caught this
- **Nearest test**: [test file most likely responsible for covering this code]
- **Your mission**: Figure out which test *should* catch this and why it doesn't. Fix the test or write a new one.
- **Done when**: Re-running the mutation on this line results in a killed mutant (test fails)
- **Time box**: [minutes]
```

### 🧪 Upgrade Card

```markdown
### 🧪 UPGRADE-[NNN]: [Function Name]
- **Difficulty**: [🟢 | 🟡 | 🔴]
- **File**: [test file path]::[test function name(s)]
- **Subject**: [production function/class being tested]
- **Why it's a candidate**: [what property or invariant makes this suitable for property-based testing — e.g., "pure calculation", "output always subset of input", "serialization roundtrip"]
- **What's missing**: [the invariant to test — stated as a rule, not an example]
- **Your mission**: Add Hypothesis (Python) or fast-check (TypeScript) tests for the invariant. Keep existing example-based tests — don't replace them.
- **Done when**: At least one property-based test exists that would catch a violation of the stated invariant
- **Time box**: [minutes]
```

### 🔗 Seam Card

```markdown
### 🔗 SEAM-[NNN]: [Module A → Module B]
- **Difficulty**: [🟢 | 🟡 | 🔴]
- **Boundary**: [the call site — function in Module A that calls into Module B]
- **What crosses the boundary**: [the data or behavior being handed off]
- **Why it's untested**: [both sides have unit tests but the handoff itself has no test]
- **What could go wrong**: [specific failure mode that unit tests on each side would miss]
- **Your mission**: Write one integration test that exercises the full path through both modules at this boundary. No mocking of the boundary itself.
- **Done when**: A test exists that would fail if the contract between the two modules broke
- **Time box**: [minutes]
```

### 🔁 Redundancy Card

```markdown
### 🔁 REDUNDANT-[NNN]: [Description]
- **Difficulty**: [🟢 | 🟡 | 🔴]
- **Files**: [test file(s) and function names]
- **What's duplicated**: [the code path or behavior both tests exercise]
- **Why it matters**: [maintenance cost — if the behavior changes, N tests break for one logical change]
- **Your mission**: Confirm these tests are truly redundant (same path, same assertions). If so, delete the weaker one and verify the remaining test still covers the behavior. If they differ in a meaningful way, document what each one adds.
- **Done when**: Either one test is deleted, or you've documented why both are needed
- **Time box**: [minutes]
```

### 👻 Orphan Card

```markdown
### 👻 ORPHAN-[NNN]: [Test Name]
- **Difficulty**: [🟢 | 🟡 | 🔴]
- **File**: [test file path]::[test function name]
- **Subject**: [the function/class/behavior the test appears to target]
- **Why it may be obsolete**: [what changed — function removed, renamed, logic gutted, behavior moved]
- **Your mission**: Confirm whether this test still tests anything real. If the subject no longer exists or has changed enough that the test is a passenger, delete it. If it's salvageable, update it to match current behavior.
- **Done when**: Either the test is deleted, or it's updated and tests a real current behavior
- **Time box**: [minutes]
```

### 👾 Boss Battle Card

```markdown
### 👾 BOSS-[NNN]: [Module Name]
- **Difficulty**: 🔴
- **Module**: [source module or feature area]
- **Issues found**: [count] — references: [list card numbers, e.g., SMELL-003, GAP-007, GAP-008]
- **The situation**: [2-3 sentences describing the overall problem with testing in this area]
- **Your mission**: Review the related cards first, then decide: should these tests be restructured from scratch or fixed incrementally?
- **Done when**: You've completed the referenced cards AND documented your decision in a comment at the top of the test file
- **Time box**: 45 min (or split across sessions)
```

## test_audit.md

```markdown
# Test Suite Audit

**Date**: [today's date]
**Assessed Against**: Test quality standards (assertion quality, test design, coverage quality, test independence, AI-generated test red flags)
**Test Framework(s)**: [e.g., pytest, vitest, jest]
**Codebase**: [languages, frameworks involved]

---

## Scorecard

| Metric | Value | Notes |
|--------|-------|-------|
| Total test files | [n] | |
| Total test functions/methods | [n] | |
| Line coverage (if available) | [n%] | [tool used or "not configured"] |
| Mutation score (if available) | [n%] | [tool used or "not configured"] |
| Tests with no meaningful assertions | [n] | |
| Tests with smell flags | [n] | |
| Source modules with zero test coverage | [n] | list below |
| Investigation cards generated | [n] | 🔍 [n] 🎯 [n] 💀 [n] 👾 [n] 👻 [n] 🧪 [n] 🔗 [n] 🔁 [n] |

### Untested Modules
[List any production code modules/files with no corresponding tests]

---

## Tool Setup

### Coverage
- **Status**: [Configured / Not configured]
- **How to run**: [exact command, e.g., `pytest --cov=src --cov-report=html`]
- **Install if needed**: [e.g., `pip install pytest-cov --break-system-packages`]

### Mutation Testing
- **Status**: [Installed / Not installed]
- **Tool recommended**: [mutmut for Python / Stryker for TypeScript]
- **Install**:
  ```bash
  # Python
  pip install mutmut --break-system-packages

  # TypeScript
  npm install --save-dev @stryker-mutator/core @stryker-mutator/[test-runner]-runner
```

---

## Standards Check

These areas were evaluated:

|Standard|Status|Notes|
|---|---|---|
|Every test has meaningful assertions|[PASS/FAIL/PARTIAL]|[n violations found]|
|Assertions test behavior, not implementation|[PASS/FAIL/PARTIAL]||
|One concept per test|[PASS/FAIL/PARTIAL]||
|No conditional logic in tests|[PASS/FAIL/PARTIAL]||
|Business logic has correct AND incorrect input tests|[PASS/FAIL/PARTIAL]||
|Edge cases covered|[PASS/FAIL/PARTIAL]||
|Error paths tested|[PASS/FAIL/PARTIAL]||
|Tests are order-independent|[PASS/FAIL/PARTIAL]||
|No external resource dependencies|[PASS/FAIL/PARTIAL]||
|No AI-generated test red flags|[PASS/FAIL/PARTIAL]||

---

## 🃏 The Deck

> **How to use**: Work through one cluster at a time — all cards in a cluster cover the same source module, so your context stays focused. Within each cluster, cards run hardest-to-easiest. Boss cards are the entry point for clusters with 3+ issues. Check off cards as you go.
>
> **Card types**: 🔍 Smell Check | 🎯 Coverage Gap | 💀 Mutant Hunt | 👾 Boss Battle | 👻 Orphan | 🧪 Upgrade | 🔗 Seam | 🔁 Redundancy
>
> **Difficulty**: 🟢 Quick (10-15 min) | 🟡 Medium (20-30 min) | 🔴 Deep Dive (30-45 min)

### Cluster: [Module Name]

Source: `[module path]` | Tests: `[test file path]`
Total: [n] cards | Est. effort: [time]

|#|Done|Card|Type|Difficulty|Time|
|---|---|---|---|---|---|
|1|[ ]|[BOSS-001]|👾|🔴|45 min|
|2|[ ]|[GAP-001]|🎯|🔴|30 min|
|3|[ ]|[SMELL-001]|🔍|🟢|15 min|

### Cluster: [Next Module Name]

Source: `[module path]` | Tests: `[test file path]`
Total: [n] cards | Est. effort: [time]

|#|Done|Card|Type|Difficulty|Time|
|---|---|---|---|---|---|
|...|||||

**Total estimated effort**: [hour estimate]

---

## Card Details

[All investigation cards here, in card-number order for reference]

[Cards go here using the templates above]

## Rules

- Do not rewrite code in codebase
- Prefer reading existing `.mutmut-cache` over re-running
- Provide brief corrected examples when fix is obvious
- Explain WHY the test is insufficient — connect to bugs it would miss
- Prioritize business logic tests over utility tests
- Cluster cards by source module
- For large suites, focus on critical modules from `_planning` documents
