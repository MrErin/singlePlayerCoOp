---
description: Full codebase sweep producing two outputs — an agent-executable auto-fix list (audit-auto.md) for delegation to a cheap model, and a gamified human review deck (audit-review.md) for decisions that require judgment. Replaces /plan:debt and /plan:test-audit.
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Agent
---

# Code Audit

**Skill:** Load `my-style`

## Resume Detection

Before starting, check if `_planning/audit-review.md` exists:

- `<!-- STATUS: COMPLETE -->` → tell the user the audit is current. Suggest re-running only if significant code has changed since the audit date.
- `<!-- STATUS: DRAFT -->` + `<!-- TEST PASS: COMPLETE -->` → skip to Pass 3 (Dual Output).
- `<!-- STATUS: DRAFT -->` + `<!-- DEBT PASS: COMPLETE -->` → skip to Pass 2 (Test Analysis).
- `<!-- STATUS: DRAFT -->` + `<!-- DOC PASS: COMPLETE -->` → skip to Pass 1 (Debt Analysis).
- `<!-- STATUS: DRAFT -->` + no pass markers → start with Pass 0 (Documentation Drift).

---

## Setup — Run Once

1. **Read**: `_planning/codebase.md`, `_planning/requirements.md`, `_planning/decisions.md`
   - If `_planning/` does not exist: STOP. Tell user to run `/plan:init` first.

2. **Check for tests**: Use Glob to find test files. If no test files exist, skip Pass 2 (Test Analysis) entirely — note this in both document headers.

3. **Map module structure**: Use Glob to enumerate source files and directories to see the full module structure.

4. **Triage modules**: From `codebase.md`, identify all source modules and rank by importance:
   business logic > data layer > API/routes > utilities > config

5. **Scaffold both documents**:
   - Read `commands/plan/references/audit-template.md` for review card formats.
   - Read `commands/plan/references/audit-auto-template.md` for the auto-fix list format.
   - Write `_planning/audit-review.md` with `<!-- STATUS: DRAFT -->`, `<!-- DOC PASS: PENDING -->`, `<!-- DEBT PASS: PENDING -->`, `<!-- TEST PASS: PENDING -->`, document header, and ranked module list.
   - Write `_planning/audit-auto.md` with document header and empty module sections.

---

## Classification Rules

Every finding is routed to one of two tiers. Apply these rules before writing any item.

**AUTO tier** — executable by an agent without human judgment:
- Unused imports (confirmed not dynamically referenced)
- Confirmed dead code (no callers, no dynamic dispatch, not a test fixture or API endpoint)
- Missing type annotations on simple functions (no complex generics or protocol types involved)
- Style/naming violations that are purely mechanical (casing, underscore consistency)
- Redundant/duplicate tests confirmed identical (same code path, same assertions)
- Orphan tests for confirmed-deleted or confirmed-renamed production code
- Trivial assertion fixes (`>=` where `==` is clearly correct; untested field in return object)
- Missing trivial tests for pure functions with deterministic, obvious behavior
- Unused variables, dead branches, unreachable code

**Renames require a mandatory protocol:**

Before any rename, the agent MUST:
1. Grep for the symbol across the entire codebase (not just the current file)
2. Enumerate all matches: imports, usages, tests, docstrings, comments, string literals
3. Verify each match is the same symbol (not a homonym in different scope)
4. Update ALL matches in a single pass

**Escalate if:**
- Symbol has >20 matches (too many to verify safely)
- Matches span config files, migrations, or external references
- Symbol name is common enough to have false positives (e.g., `process`, `handle`, `run`)

**Safe to auto-fix if:**
- <10 matches, all clearly the same symbol
- Matches are confined to source and test files
- No ambiguous usages found

**REVIEW tier** — requires human judgment:
- Architectural pattern changes (any structural redesign)
- Design principle violations (SRP, DI, separation of concerns)
- Security concerns of any kind
- Dead code where usage is ambiguous (dynamic dispatch, monkey patching, plugin systems)
- Refactors touching shared interfaces
- Mutant analysis (determining which test should catch what and why it doesn't)
- Coverage gaps requiring new test logic or understanding of business rules
- Test smells requiring test redesign (not just a trivial assertion fix)
- Seam/integration test needs
- Any fix with Medium or High risk
- Any item where the correct answer depends on context or tradeoffs

**When uncertain**: default to REVIEW. An over-cautious review deck is better than an agent making architectural decisions.

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

**Output format:** The subagent returns findings as a list with tier classification. Main agent writes AUTO findings to `audit-auto.md` and REVIEW findings as 📄 DOC cards to `audit-review.md`.

**The subagent must NOT modify files** — only read and report.

When complete: update marker to `<!-- DOC PASS: COMPLETE -->`.

---

## Pass 1 — Debt Analysis

Update the draft marker to `<!-- DEBT PASS: IN_PROGRESS -->`.

**Quick antipattern scan first** — before per-module analysis, use Grep to find critical patterns across the whole codebase. Route each match per the classification rules above (all patterns below are REVIEW tier):

| Pattern | Card type | Severity |
|---------|-----------|----------|
| `sys.modules[` | 🔥 ARCH | Critical |
| `except:` or `except.*: pass` | 🔥 ARCH | Critical |
| `=[` or `={}` in function signature | 🔥 ARCH | Critical |
| `from unittest.mock import` in `src/` | 🔥 ARCH | High |
| `+` or f-string in SQL | 🗃️ DATA | High |
| query inside loop over results | 🗃️ DATA | High |

See `my-style/references/antipatterns.md` for the full detection pattern list and severity mappings.

**Per-module analysis** (highest priority first):

For each module, delegate to a `code-reviewer` subagent. The subagent receives:
- The module's files (use Grep and Read to gather them)
- `my-style` standards
- The debt-specific checks listed below
- The classification rules above — the subagent must label each finding AUTO or REVIEW

Debt-specific checks per module:
- File organization follows feature-folder pattern
- DB connections use context managers (no manual open/close)
- All queries use parameterized syntax (no string concatenation or f-strings)
- Semantic HTML used appropriately (not div-for-everything)
- Interactive elements have ARIA labels, keyboard navigation, and focus management
- **Dead code**: use Grep to find functions/classes defined but never called outside their own file. Verify before flagging — check for dynamic calls, test fixtures, and API endpoints. Route confirmed dead code per classification rules.
- **Redundant code**: near-identical functions across files, copy-paste artifacts, multiple implementations of the same utility → route per classification rules.

**After each module**: Write AUTO findings to `audit-auto.md` and REVIEW findings as cards to `audit-review.md` before moving to the next module.

When all modules are complete: update marker to `<!-- DEBT PASS: COMPLETE -->`.

---

## Pass 2 — Test Analysis

Update the draft marker to `<!-- TEST PASS: IN_PROGRESS -->`.

**Run tooling first — always coverage before mutation:**

1. Run `coverage-wrapper run` → get branch coverage percentage. Append results to `audit-review.md`.
2. Run `coverage-wrapper gaps` → identify uncovered files. Append results to `audit-review.md`.
3. Assess:
   - **Below 80%**: Skip mutation testing entirely. Focus all test cards on 🎯 GAP cards. Add note to document: "Mutation testing deferred — branch coverage must reach 80% first."
   - **80–90%**: Run `mutmut-wrapper run` (no pattern filter). Append results.
   - **Above 90%**: Run `mutmut-wrapper run`, then `mutmut-wrapper show-all`. Read `mutmut_output/survived_all.txt` for diffs. Append results.

**Quick antipattern scan for test files** — use Grep before per-module analysis:
- `sys.modules[` in test files → 🔍 SMELL card (REVIEW)
- `MagicMock` in `src/` → 🔍 SMELL card (REVIEW)
- `assert True` or assertion-free tests → route per classification rules

**Per-module test analysis** (same priority order as Pass 1):

For each module's test file(s), use Grep for test function definitions to see all test functions. Evaluate against these standards:

| Category | What to check |
|----------|---------------|
| **Naming** | `Test[Feature]` class names; `test_[action]_[condition]_[result]` method names; no vague names like `TestUser` |
| **Design** | One concept per test; no conditionals; proportional setup; no section dividers |
| **Independence** | Order-independent; no shared mutable state; no timing dependencies |
| **Assertions** | All return fields asserted; exact counts (not `>=`); no tautologies; no mirror tests |
| **Coverage** | Edge cases; error paths; minimum 1:2 negative:happy-path ratio |
| **Seams** | Module boundaries have integration tests, not just mocked units |
| **Redundancy** | No duplicate tests covering same path with same assertions |
| **Obsolete** | Tests for renamed or deleted functions |
| **Parallel coverage** | Similar modules (same pattern) have similar test coverage |

**After each module**: Write AUTO findings to `audit-auto.md` and REVIEW findings as cards to `audit-review.md`.

When all modules are complete: update marker to `<!-- TEST PASS: COMPLETE -->`.

---

## Pass 3 — Dual Output

### Finalize audit-auto.md

1. Review all AUTO items written across all three passes (Doc, Debt, Test).
2. Within each module section, order by safety: doc sync first, then dead code and unused imports, then style/naming, then test fixes.
3. Assign sequential IDs: `AUTO-001`, `AUTO-002`, etc. across the entire document.
4. Ensure the Escalations section is present at the bottom.
5. Write the header summary: total items, modules affected.

### Finalize audit-review.md

1. Read all REVIEW cards from Passes 0, 1, and 2.

2. **Group into module clusters**: Every card touching the same source module belongs in one cluster — doc, debt, and test cards together. A card spanning multiple files may appear in multiple clusters; add a cross-reference note. Doc-only cards (no module) go in a "Planning Docs" cluster at the start.

3. **Within each cluster**:
   - Assign a 👾 BOSS card if the cluster has 3 or more cards total (debt + test combined).
   - Order: BOSS card first, then remaining cards by severity/difficulty descending.
   - Add a note: "N auto-fix item(s) for this module → see audit-auto.md" (omit if zero).

4. **Order clusters**: Higher-severity clusters first. Tiebreak: clusters whose files are touched by other clusters come first (fixing them unblocks others).

5. **Write the cluster deck** using the template from `audit-template.md`. Each row in the cluster table must include the type emoji in the Type column.

6. **Generate the scorecard** now that all cards are counted.

7. Replace `<!-- STATUS: DRAFT -->` with `<!-- STATUS: COMPLETE -->`.

---

## Rules

- **Emojis are required — not optional.** Every review card heading must open with its type emoji (📄 🔥 ⚙️ 🧹 🗃️ ♿ 🔍 🎯 💀 🧪 🔗 🔁 👻 👾). Every Difficulty field must include a colored circle (🟢 🟡 🔴 ⚫). Every Type column in cluster tables must show the emoji. These are functional visual cues — never omit them.
- Auto-fix items do not use card emojis. They use the terse format from `audit-auto-template.md`.
- Do not rewrite production code during analysis. Trivial test assertion fixes are allowed.
- Delegate per-module debt analysis to `code-reviewer` subagents — do not analyze debt inline.
- Always run `coverage-wrapper` before `mutmut-wrapper` — never skip the order of operations.
- Use `coverage-wrapper` and `mutmut-wrapper` — never raw `coverage` or `mutmut` commands.
- Write findings to disk after each module — do not batch all writes to the end.
- **When uncertain about tier**: default to REVIEW.
- Review cards: provide a brief corrected example when the fix is obvious. Explain why the issue matters.
- Auto items: no examples, no explanation beyond the one-line why.


$ARGUMENTS
