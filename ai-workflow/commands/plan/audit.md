---
description: Full codebase sweep producing two outputs — an agent-executable auto-fix list (audit-auto.md) covering everything with an unambiguous fix, and a slim review deck (audit-review.md) containing only items that require a human decision between valid alternatives. Covers debt analysis, test analysis, and documentation drift.
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Agent
---

# Code Audit

**Skill:** Load `my-style`

## Resume Detection

Before starting, check if `_planning/audit-review.md` exists:

- `<!-- STATUS: COMPLETE -->` → tell the user the audit is current. Suggest re-running only if significant code has changed since the audit date.
- `<!-- STATUS: DRAFT -->` + `<!-- TEST PASS: COMPLETE -->` → skip to Finalize.
- `<!-- STATUS: DRAFT -->` + `<!-- DEBT PASS: COMPLETE -->` → skip to Pass 2 (Test Analysis).
- `<!-- STATUS: DRAFT -->` + `<!-- DOC PASS: COMPLETE -->` → skip to Pass 1 (Debt Analysis).
- `<!-- STATUS: DRAFT -->` + no pass markers → start with Pass 0 (Documentation Drift).

---

## Setup — Run Once

1. **Read**: `_planning/codebase.md`, `_planning/requirements.md`, `_planning/decisions.md`
   - If `_planning/` does not exist: STOP. Tell user to run `/plan:init` first.
   - If `_planning/backlog/bugs.md` exists, read it and keep the list of known bugs in context. Any finding that matches an already-tracked bug must be skipped — do not create a duplicate card or AUTO item for it.

2. **Check for tests**: Use Glob to find test files. If no test files exist, skip Pass 2 (Test Analysis) entirely — note this in both document headers.

3. **Map module structure**: Use Glob to enumerate source files and directories to see the full module structure.

4. **Triage modules**: From `codebase.md`, identify all source modules and rank by importance:
   business logic > data layer > API/routes > utilities > config

5. **Scaffold both documents**:
   - Read `commands/plan/references/audit-template.md` for review card formats.
   - Read `commands/plan/references/audit-auto-template.md` for the auto-fix list format.
   - Write `_planning/audit-review.md` with `<!-- STATUS: DRAFT -->`, `<!-- DOC PASS: PENDING -->`, `<!-- DEBT PASS: PENDING -->`, `<!-- TEST PASS: PENDING -->`, document header, scorecard placeholder, and three sections (Documentation Drift, Debt, Tests).
   - Write `_planning/audit-auto.md` with document header and empty module sections.

---

## Classification Rules

Every finding is routed to one of two tiers. The deciding question is: **"Is there a decision to make — a choice between valid alternatives or a tradeoff to accept?"** If the fix has one correct answer, it's AUTO regardless of how many files it touches or how risky it feels. Risk determines whether the agent should be *careful*, not whether a human needs to *decide*.

**Backlog deduplication** — before writing any item, check it against `_planning/backlog/bugs.md` (loaded in Setup). If the finding describes the same issue as an existing bug entry, skip it entirely.

**AUTO tier** (default) — the fix is unambiguous, even if large:
- Everything with one correct fix: dead code, unused imports, missing types, naming violations, stale comments, long functions with obvious split points, missing tests where the behavior is clear, orphan tests, redundant tests, trivial assertion fixes, linter violations, doc sync mismatches
- Coverage gaps where what to test is obvious (pure functions, clear branches, error paths)
- Survived mutants where the missing assertion is clear
- Test smells with a mechanical fix (rename, remove conditional, add assertion)
- Code quality issues with one right answer (extract function, add context manager, parameterize query)

**Renames require a mandatory protocol** (but are still AUTO):

Before any rename, the agent MUST:
1. Grep for the symbol across the entire codebase (not just the current file)
2. Enumerate all matches: imports, usages, tests, docstrings, comments, string literals
3. Verify each match is the same symbol (not a homonym in different scope)
4. Update ALL matches in a single pass

**Escalate (move to REVIEW) if:** >20 matches, spans config/migrations, or symbol name has false-positive risk.

**REVIEW tier** — there is a genuine decision with multiple valid approaches:
- Architectural changes where there are multiple valid restructurings
- Security concerns (tradeoff between security and usability/complexity)
- Design principle violations where the fix could go several ways (how to split responsibilities, where to draw module boundaries)
- Dead code where usage is ambiguous (dynamic dispatch, plugin systems)
- Behavior changes — the "fix" would change what users see
- Refactors touching shared interfaces where downstream impact is unclear
- Any item where you can articulate two or more reasonable approaches

**When uncertain**: default to AUTO with an escalation note. The auto-fix doc has an Escalations section — an item that turns out harder than expected gets flagged there. A wrongly-escalated AUTO wastes agent time on one item; a wrongly-classified REVIEW wastes human time on a non-decision.

---

## Pass 0 — Documentation Drift

Update the draft marker to `<!-- DOC PASS: IN_PROGRESS -->`.

**Purpose:** Catch inconsistencies between planning docs and actual codebase state before analyzing code. This surfaces manual fixes the user made that weren't reflected back into planning docs.

**Delegate to a `general-purpose` subagent** with the following task:

The subagent reads all active planning files (exclude `_planning/archive/`):
- `_planning/roadmap.md`
- `_planning/state.md`
- `_planning/codebase.md`
- `_planning/decisions.md`
- `_planning/requirements.md`
- `_planning/deferred.md`
- Current phase `_planning/phase[N]/plan.md` (if any)

The subagent checks for drift and classifies each finding as AUTO or REVIEW:

### AUTO-tier drift (mechanical mismatches)

| Check | AUTO if |
|-------|---------|
| Phase status mismatch | roadmap.md shows phase N "in progress" but state.md shows different status |
| Stale directory listing | codebase.md lists directories that no longer exist (verify with Glob) |
| Stale dependency listing | codebase.md lists dependencies not in requirements.txt / package.json |
| Orphan phase files | plan.md exists for phase but roadmap has no such phase number |
| Deferred item resolved | deferred.md lists an item that appears implemented (grep shows usage in codebase) |

### REVIEW-tier drift (requires judgment)

| Check | REVIEW if |
|-------|-----------|
| Feature drift | Code implements behavior not mentioned in requirements.md (user may have added scope informally) |
| Decision violation | decisions.md says "use X pattern" but code uses Y (may be intentional override or drift) |
| Missing from codebase.md | New directories/modules added but codebase.md not updated |
| Contradictory requirements | requirements.md and decisions.md say different things about same concern |
| Stale phase intent | Roadmap phase intent doesn't match what was actually built (per phase_summary.md or code) |

**Output format:** The subagent returns findings as a list with tier classification. Main agent writes AUTO findings to `audit-auto.md` and REVIEW findings (only those with ambiguous resolution) as 📄 DOC cards to `audit-review.md`.

**The subagent must NOT modify files** — only read and report.

When complete: update marker to `<!-- DOC PASS: COMPLETE -->`.

---

## Pass 1 — Debt Analysis

Update the draft marker to `<!-- DEBT PASS: IN_PROGRESS -->`.

**Linter scan first** — run across the full codebase before any grep or per-module analysis:

- Python: `ruff check --output-format=json <source dirs>`
- JavaScript/TypeScript: `npx eslint --format=json <source dirs>`
- If no linter config found: skip and note in the debt summary.

Parse the output. Route each finding per the classification rules:
- Autofix-capable violations (ruff `fix` field present; eslint `fixable`) → **AUTO tier**: add to `audit-auto.md` as a single grouped item per rule (e.g., "Fix 14 E501 line-length violations across 6 files"). Do not list every line individually.
- Non-autofix violations where the fix is unambiguous and mechanical → **AUTO tier**
- Non-autofix violations requiring judgment (ruff B/C/S rules; complex restructuring) → **AUTO** if the fix is unambiguous; **REVIEW** only if there are multiple valid approaches

Note total linter violation count in the Debt Summary. Skip any grep pattern below that ruff already caught.

**Quick antipattern scan** — use Grep for patterns ruff doesn't cover. Most antipatterns have one correct fix and route to AUTO. Route to REVIEW only if the fix is ambiguous (e.g., a bare `except:` that might be intentional error suppression).

| Pattern | Typical fix | Default tier |
|---------|-------------|-------------|
| `sys.modules[` | Remove monkey-patching | AUTO |
| `except:` or `except.*: pass` | Add specific exception type | AUTO (REVIEW if suppression may be intentional) |
| `=[` or `={}` in function signature | Use `None` default + factory | AUTO |
| `from unittest.mock import` in `src/` | Move to test file | AUTO |
| `+` or f-string in SQL | Parameterize query | AUTO |
| query inside loop over results | Batch query | AUTO (REVIEW if restructuring is non-obvious) |

See `my-style/references/antipatterns.md` for the full detection pattern list and severity mappings.

**Package hallucination check** — verify all imports resolve to real packages. AUTO tier.
1. Collect all `import` / `from X import` statements across source files (exclude stdlib modules).
2. Cross-check each against the project's lock file (requirements.txt, pyproject.toml, package.json, or package-lock.json).
3. Flag any import that doesn't resolve to a listed dependency or stdlib module — these may be hallucinated packages and a potential supply-chain risk (slopsquatting).

**Placeholder credential scan** — grep for known AI-generated placeholder secrets. AUTO tier.
- `password123`, `admin123`, `changeme`, `secret123`, `test1234`, `letmein`
- `your-secret-key`, `supersecretkey`, `change-me`
- `sk_test_`, `sk_live_`, `ghp_`, `glpat_`, `AKIA` (existing)
- Any string literal assigned to a variable named `password`, `secret`, `api_key`, `token`, or `signing_key`

**Scope/visibility check** — during per-module analysis. AUTO tier.
- For each module, identify functions without a `_` prefix that have no callers outside their own file (grep for the function name across the codebase). Flag as over-exposed — fix is to add `_` prefix.

**Per-module analysis** (highest priority first, sequential — one module at a time):

For each module, read its files using Grep and Read, then analyze inline. Apply the classification rules above to label each finding AUTO or REVIEW.

Debt-specific checks per module:
- File organization follows feature-folder pattern
- DB connections use context managers (no manual open/close)
- All queries use parameterized syntax (no string concatenation or f-strings)
- Semantic HTML used appropriately (not div-for-everything)
- Interactive elements have ARIA labels, keyboard navigation, and focus management
- **Dead code**: use Grep to find functions/classes defined but never called outside their own file. Verify before flagging — check for dynamic calls, test fixtures, and API endpoints. Route confirmed dead code per classification rules.
- **Redundant code**: near-identical functions across files, copy-paste artifacts, multiple implementations of the same utility → route per classification rules.

**Architectural assessment** (from `my-style/references/architecture.md`) — evaluate each module for:
- **Coupling:** Does the module import from the wrong layer? Are there circular or inverted dependencies? Can the module be used in isolation?
- **Separation of concerns:** Does the module mix responsibilities? Are models pure data? Are repositories pure CRUD? Is business logic in services, not UI or DB?
- **Data layer:** Are column lists duplicated across methods? Are repositories single-responsibility? Do query results map to typed models? Is there a migration system?
- **External service integration:** Is provider config externalized? Does retry logic distinguish transient from permanent errors? Is adding a provider low-friction (≤3 files)?
- **Configuration:** Are constants centralized or scattered? Are display strings duplicated between constants and views?
- **Code duplication:** Are filter lists, column lists, or input preparation logic duplicated across methods or files?
- **Extensibility:** For each module, estimate the file touch count for adding a new table, provider, screen, or enum value. Flag any scenario that's high friction (7+ files) — route to REVIEW only if there are multiple valid ways to reduce friction.

**After each module**: Write AUTO findings to `audit-auto.md` and REVIEW findings as cards to the appropriate type section in `audit-review.md` before moving to the next module.

When all modules are complete: update marker to `<!-- DEBT PASS: COMPLETE -->`.

---

## Pass 2 — Test Analysis

Update the draft marker to `<!-- TEST PASS: IN_PROGRESS -->`.

**Run tooling first — always coverage before mutation:**

1. Run `coverage-wrapper run` → get branch coverage percentage. Append results to `audit-review.md`.
2. Run `coverage-wrapper gaps` → identify uncovered files. Append results to `audit-review.md`.
3. **Derive coverage gap items** from the `coverage-wrapper gaps` output. Each uncovered file or function becomes an AUTO item if what to test is obvious, or a REVIEW card if the behavior to test is unclear or requires understanding business rules.
4. Assess:
   - **Below 80%**: Skip mutation testing entirely. Add note to document: "Mutation testing deferred — branch coverage must reach 80% first."
   - **80–90%**: Run `mutmut-wrapper run` (no pattern filter). Append results.
   - **Above 90%**: Run `mutmut-wrapper run`, then `mutmut-wrapper show-all`. Read `mutmut_output/survived_all.txt` for diffs. Append results.

**Quick antipattern scan for test files** — use Grep before per-module analysis. Most test antipatterns have a clear fix and route to AUTO. Route to REVIEW only when the test redesign has multiple valid approaches.
- `sys.modules[` in test files → AUTO (remove and use proper imports)
- `MagicMock` in `src/` → AUTO (move to test file)
- `assert True` or assertion-free tests → AUTO (add real assertion or delete)
- **Phantom mocks:** `grep -r 'patch("' tests/` — for each unique patch path, attempt to resolve the import. Paths that don't exist are phantom mocks → AUTO (fix patch path or delete test)
- **Dead mock smell:** Files where `patch(` count ≥ 3× the `def test_` count → REVIEW (likely needs test redesign — multiple valid approaches)

**Quantitative metrics scan** — run before per-module analysis. Adjust path from `codebase.md`. Write results directly into the Test Quality section of `audit-review.md`.

| Metric | Command | Note |
|--------|---------|------|
| Total tests | `grep -r "def test_" tests/ \| wc -l` | |
| Total assertions | `grep -r "^\s*assert " tests/ \| wc -l` | |
| Assertion ratio | assertions ÷ tests | Healthy: 1.5–3.0 |
| Skipped tests | `grep -r "@pytest.mark.skip\|pytest.skip" tests/ \| wc -l` | Each needs a documented reason |
| Empty tests | `grep -rn "def test_" tests/ \| grep -A1 "def test_" \| grep -cE "^\s*pass$"` | Should be 0 |
| Largest file assertion share | `grep -c "assert" tests/test_*.py \| sort -t: -k2 -n` | Flag if one file >30% of total |

Route findings:
- Undocumented skipped tests → AUTO (add skip reason or remove skip)
- Empty tests (pass/no assertions) → AUTO (add assertion or delete)
- Assertion ratio <1.5 or >5 → note in Warning Signs checklist, not a card unless systemic

**Per-module test analysis** (same priority order as Pass 1):

For each module's test file(s), use Grep for test function definitions to see all test functions. Evaluate against these standards:

| Category | What to check |
|----------|---------------|
| **Naming** | `Test[Feature]` class names; `test_[action]_[condition]_[result]` method names; no vague names like `TestUser` |
| **Design** | One concept per test; no conditionals; proportional setup; no section dividers |
| **Independence** | Order-independent; no shared mutable state; no timing dependencies |
| **Assertions** | All return fields asserted; exact counts (not `>=`); no tautologies; no mirror tests |
| **Edge cases** | Error paths tested; minimum 1:2 negative:happy-path ratio |
| **Seams** | Module boundaries have integration tests, not just mocked units |
| **Redundancy** | No duplicate tests covering same path with same assertions |
| **Obsolete** | Tests for renamed or deleted functions |
| **Parallel coverage** | Similar modules (same pattern) have similar test coverage |
| **Mock integrity** | No phantom mocks (patch paths that don't resolve); no dead mock smell (3+ patches, assertions only on mock calls) |
| **Name-assertion alignment** | Test names match what's asserted — not just a mock call count |
| **Test organization** | No `*Integration*`/`*Misc*`/`*Other*` catch-all classes with >3 tests across different categories |

**After each module**: Write AUTO findings to `audit-auto.md` and REVIEW findings as cards to `audit-review.md`.

When all modules are complete: update marker to `<!-- TEST PASS: COMPLETE -->`.

---

## Finalize

### Trend Data

Before finalizing either document, check for `_planning/audit-scorecard.md`:

1. If it exists: read the most recent entry (newest at top). Extract Previous values from its Coverage & Mutation, Test Quality, and Summary sections.
2. Populate the **Previous** and **Δ** columns in the current `audit-review.md` scorecard. Δ = Current − Previous. For card/item counts and zero-coverage modules, negative Δ is improvement (↓ is good). For coverage, mutation score, and assertion ratio, positive Δ is improvement (↑ is good).
3. If `audit-scorecard.md` does not exist: leave Previous and Δ blank. Note "First audit — no baseline yet" in the scorecard header.

After both documents are finalized, prepend a new snapshot entry to `_planning/audit-scorecard.md` (create if it doesn't exist). Load `commands/plan/references/audit-scorecard-template.md` for the entry format.

### Finalize audit-auto.md

1. Review all AUTO items written across all three passes (Doc, Debt, Test).
2. Within each module section, order by safety: doc sync first, then dead code and unused imports, then style/naming, then test fixes.
3. Assign sequential IDs: `AUTO-001`, `AUTO-002`, etc. across the entire document.
4. Ensure the Escalations section is present at the bottom.
5. Write the header summary: total items, modules affected.

### Finalize audit-review.md

1. **Generate the scorecard** — count cards by type across all sections. Cards are already organized by type from Passes 0–2; no re-ordering needed.
2. Replace `<!-- STATUS: DRAFT -->` with `<!-- STATUS: COMPLETE -->`.

---

## Rules

- **Emojis are required — not optional.** Every review card heading must open with its type emoji. These are functional visual cues — never omit them.
- Auto-fix items use the terse format from `audit-auto-template.md`.
- Do not rewrite production code during analysis. Trivial test assertion fixes are allowed.
- Analyze each module sequentially — read files, review, write findings, then move to the next module. No parallel subagents.
- Always run `coverage-wrapper` before `mutmut-wrapper` — never skip the order of operations.
- Use `coverage-wrapper` and `mutmut-wrapper` — never raw `coverage` or `mutmut` commands.
- Write findings to disk after each module — do not batch all writes to the end.
- **When uncertain about tier**: default to AUTO with an escalation note. The agent can always escalate; the human shouldn't have to triage non-decisions.


$ARGUMENTS
