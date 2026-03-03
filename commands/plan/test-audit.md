---
description: Audit the test suite for quality, effectiveness, and coverage gaps. Generates investigation cards — small, self-contained tasks for manually verifying and improving tests. Does NOT rewrite code. 
allowed-tools: bash_tool create_file str_replace view
---

# Audit Test Suite

## Defaults

Load `my-style` skill. No git commits.

## Steps

1. **Read**: all documents in the `_planning` directory to understand the project requirements, codebase, and architecture
    1. If the `_planning` directory does not exist, STOP. Instruct the user to run the /plan:init command first
2. **Map the test landscape**: Identify all test files, the test framework(s) in use, and which source modules have corresponding tests
3. **Analyze each test file** against the standards below. For every issue found, create an investigation card (see card templates)
4. **Run coverage analysis** if a coverage tool is configured (e.g., `pytest --cov`, `vitest --coverage`). If not configured, note this in the setup section and skip
5. **Identify mutation testing readiness**: Check if `mutmut` (Python) or `stryker` (TypeScript) is installed. Record status in the setup section.
	1. If it is installed and has been run, incorporate mutation cards in step 7
	2. If it is not installed, add instructions in the setup section
6. **Generate**: a file in the `_planning` directory called `test_audit.md` using the template below
7. **Generate cards**: Create investigation cards organized by type, then shuffle the final deck into a recommended session order that alternates card types for variety
8. **Classify** each card by difficulty (🟢 Quick 10-15 min, 🟡 Medium 20-30 min, 🔴 Deep Dive 30-45 min)

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

### Coverage Quality (not just quantity)

- [ ] Business logic functions have tests that verify correct AND incorrect inputs
- [ ] Edge cases are covered (nulls, empty collections, boundary values, zero, negative)
- [ ] Error paths are tested, not just happy paths
- [ ] Tests would fail if the core logic changed (not just if an exception is thrown)

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
| Investigation cards generated | [n] | 🔍 [n] 🎯 [n] 💀 [n] 👾 [n] |

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

> **How to use**: Pick a card — any card. Each one is self-contained. Work through them in the order below (shuffled for variety) or pick randomly. Check them off as you go. No need to do them all in one session.
> 
> **Card types**: 🔍 Smell Check | 🎯 Coverage Gap | 💀 Mutant Hunt | 👾 Boss Battle
> 
> **Difficulty**: 🟢 Quick (10-15 min) | 🟡 Medium (20-30 min) | 🔴 Deep Dive (30-45 min)

### Session-Ready Order

[Cards arranged to alternate types and difficulty for sustained engagement]

|#|Done|Card|Type|Difficulty|File|Time|
|---|---|---|---|---|---|---|
|1|[ ]|[SMELL-001]|🔍|🟢|[file]|15 min|
|2|[ ]|[GAP-001]|🎯|🟡|[file]|25 min|
|3|[ ]|[SMELL-002]|🔍|🟢|[file]|10 min|
|...|||||||

**Total estimated effort**: [hour estimate] **Suggested pace**: [n] cards per session, [estimated sessions] sessions total

---

## Card Details

[All investigation cards here, in card-number order for reference]

[Cards go here using the templates above]

## Rules

- Do NOT rewrite any code in the codebase
- Do NOT make git commits
- Do NOT run mutation testing tools (only check if they're installed and provide setup instructions)
- Do provide brief corrected examples inside cards when the fix is obvious (e.g., adding an assertion)
- Do provide information for WHY the test is insufficient — connect to what bug it would miss
- Do prioritize business logic tests over utility/helper tests
- Do alternate card types in the session-ready order to maintain variety
- If the test suite is very large, focus on the modules identified as critical in the `_planning` documents and note which areas were not audited
