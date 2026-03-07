---
description: Generate or update the technical_debt document for a brownfield project. Use to assess existing code base against preferences and best practices outlined in my-style skill
allowed-tools: Bash, Read, Write, Grep, Glob
---

# Assess Technical Debt

## Defaults
Load `my-style` skill. No git commits.

## Steps

1. **Read**: all documents in the `_planning` directory to understand the project requirements, codebase, roadmap, etc.
	1. If the `_planning` directory does not exist, STOP. Instruct the user to run the /plan:init command to map the codebase before assessing technical debt
2. **Analyze**: the codebase of this project according to the standards outlined in the /my-style skill
3. **Research**: relevant code or architectural patterns according to the type of project, the code language and framework, and other best practices
4. **Generate**: a file in the `_planning` directory called `technical_debt.md` using the template below
5. **Organize**: the issues raised in order of severity (most severe at the top). Give each issue a number
	1. The issue numbers are contiguous throughout the document so that a proposed resolution order can be provided at the end.
6. **Add**: information to the `technical_debt.md` document that highlights architectural decisions and code patterns that deviate from the standards in /my-style. Use this template for each issue:
	```markdown
	### [Number] [Issue Name]
	- **Standard Violated:**
	- **What's wrong:** and where  
	- **Examples:**
	  - [1-2 short examples from codebase]
      -  + [approximate number of violations recorded]
	- **Why it matters** per the standard  
	- **What to do** to fix it  
	- **Files affected**
  	- **Time estimate** for the fix  
	```
7. **Generate the cluster deck**: Group all issues into clusters by the files and modules they affect — all issues touching the same module or area belong in one cluster. Within each cluster, order cards from highest to lowest severity. Order clusters so higher-severity clusters come first; if two clusters have equal severity, prioritize the one whose files are also touched by other clusters. Assign a BOSS card to any cluster with 3 or more issues. Use the Debt Card Templates below.

## Standards to Evaluate Against

**Architecture**
- [ ] No invisible dependencies (injected, not instantiated)
- [ ] No global state
- [ ] No hard-coded config/secrets
- [ ] No swallowed errors
- [ ] No unvalidated input at boundaries
- [ ] Error handling uses expected/unexpected split
- [ ] File organization follows feature-folder pattern

**Code Quality**
- [ ] Type hints on all public functions
- [ ] Functions under complexity signals

**Comments & Documentation**
- [ ] No stale comments (comments describing removed or changed behavior)
- [ ] Non-trivial files have module-level docstrings (purpose, relationships, key concepts)
- [ ] Public functions have interface contracts (what they return, error cases, side effects — not implementation)

**Logging**
- [ ] Business logic has no direct logging calls (logging at service/boundary layer only)

**Testing**
- [ ] Tests exist for business logic (pure, no IO)

**Database** *(if applicable)*
- [ ] DB connections use context managers (no manual open/close)
- [ ] All queries use parameterized syntax (no string concatenation or f-strings)

**Web Accessibility** *(if applicable)*
- [ ] Semantic HTML used appropriately (not div-for-everything)
- [ ] Interactive elements have ARIA labels, keyboard navigation, and focus management

## Debt Card Templates

All card types (🔥 ARCH, ⚙️ DESIGN, 🧹 QUALITY, 🗃️ DATA, ♿ ACCESS) use the standard template. ACCESS cards always have Low risk. BOSS cards use their own template.

**Card type prefix guide:**
- 🔥 **ARCH** — architecture violations (invisible deps, global state, hard-coded config, swallowed errors)
- ⚙️ **DESIGN** — design principle violations (SRP, DI, separation of concerns)
- 🧹 **QUALITY** — code quality, comments, logging (long functions, missing types, stale comments)
- 🗃️ **DATA** — database/SQL issues (context managers, parameterized queries)
- ♿ **ACCESS** — web accessibility (semantic HTML, ARIA, keyboard nav) — risk is always Low
- 👾 **BOSS** — cluster entry point for modules with 3+ issues

### Standard Card

```markdown
### [TYPE]-[NNN]: [Issue Name]
- **Difficulty**: [🟢 Quick (<30 min) | 🟡 Medium (30–60 min) | 🔴 Large (1–3 hr) | ⚫ XL (3+ hr)]
- **Risk**: [Low — isolated change | Medium — shared interface | High — core component, test carefully]
- **Files**: [affected file paths]
- **Fix**: [specific action — what exactly to do, not just "refactor"]
- **Done when**: [clear completion criteria — what does done look like?]
- **Time box**: [N minutes]
```

### 👾 Boss Battle Card

```markdown
### 👾 BOSS-[NNN]: [Module Name]
- **Difficulty**: 🔴
- **Risk**: [Low | Medium | High — overall risk for this cluster]
- **Module**: [source module or feature area]
- **Issues**: [count] — references: [card numbers, e.g., ARCH-001, QUALITY-003]
- **The situation**: [2-3 sentences on why this module needs coordinated work and what the combined effect of these issues is]
- **Done when**: All referenced cards are complete
- **Time box**: [N min total — or split across sessions]
```

## technical_debt.md
```markdown
# Technical Debt Assessment

**Date**: [today's date]
**Assessed Against**: [my-style standards, other standards researched by the agent e.g., SOLID, Clean Architecture]
**Codebase**: [languages, frameworks involved]

---

## CRITICAL - Architectural Violations

[Issues that violate core structural principles and affect the entire codebase]
[e.g., issues 1-3]
___

## HIGH - Design Principle Violations

[Violations of SOLID principles or separation of concerns but are contained to specific modules]
[e.g., issues 4-7]

___

## MEDIUM - Code Quality Issues

[Issues that are worth addressing but don't block functionality or create architectural risk]
[e.g, issues 8-9]

___

## LOW - Minor Improvements

[Issues that are nice-to-have, improve consistency but do not affect correctness or maintainability]
[e.g., issues 10-15]

___

## NOT VIOLATED - Standards Already Met

These areas were checked and found compliant:

| Standard | Status | Notes |  
|----------|--------|-------|  
| [Standard Checked] | PASS | [Notes] |

___

## 🃏 The Cluster Deck

> **How to use**: Work through one cluster at a time — you're already in the code, fix everything in the area before moving on. Within each cluster, cards run highest-to-lowest severity. Boss cards are the entry point for clusters with 3+ issues. Check off cards as you go.
>
> **Card types**: 🔥 Arch | ⚙️ Design | 🧹 Quality | 🗃️ Data | ♿ Access | 👾 Boss
>
> **Difficulty**: 🟢 Quick (<30 min) | 🟡 Medium (30–60 min) | 🔴 Large (1–3 hr) | ⚫ XL (3+ hr)
>
> **Risk**: Low (isolated) | Medium (shared interface) | High (core component — test carefully)

### Cluster: [Module / File Area]

Files: `[file paths]`
Total: [n] cards | Est. effort: [time] | Risk ceiling: [highest risk level in cluster]

| # | Done | Card | Type | Difficulty | Risk | Time |
|---|------|------|------|------------|------|------|
| 1 | [ ] | [BOSS-001] | 👾 | 🔴 | High | 90 min |
| 2 | [ ] | [ARCH-001] | 🔥 | 🔴 | High | 45 min |
| 3 | [ ] | [QUALITY-002] | 🧹 | 🟡 | Low | 20 min |

### Cluster: [Next Module / File Area]

Files: `[file paths]`
Total: [n] cards | Est. effort: [time] | Risk ceiling: [highest risk level in cluster]

| # | Done | Card | Type | Difficulty | Risk | Time |
|---|------|------|------|------------|------|------|
| ... | | | | | | |

**Total estimated effort**: [hour estimate]

```


## Rules

- Do NOT rewrite any code in the codebase
- Do NOT make git commits
- Do provide examples of corrected code inside the technical_debt document if that example is brief and clear
- Do provide information for why the change is necessary