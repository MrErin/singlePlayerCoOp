# Debt Card & Document Templates

Load this file when ready to generate `technical_debt.md` output.

## Debt Card Templates

All card types (ARCH, DESIGN, QUALITY, DATA, ACCESS) use the standard template. ACCESS cards always have Low risk. BOSS cards use their own template.

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
- **Difficulty**: [🟢 Quick (<30 min) | 🟡 Medium (30-60 min) | 🔴 Large (1-3 hr) | ⚫ XL (3+ hr)]
- **Risk**: [Low — isolated change | Medium — shared interface | High — core component, test carefully]
- **Files**: [affected file paths]
- **Fix**: [specific action — what exactly to do, not just "refactor"]
- **Done when**: [clear completion criteria]
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

## technical_debt.md Template

```markdown
# Technical Debt Assessment

**Date**: [today's date]
**Assessed Against**: [my-style standards, other standards researched e.g., SOLID, Clean Architecture]
**Codebase**: [languages, frameworks involved]

---

## CRITICAL - Architectural Violations

[Issues that violate core structural principles and affect the entire codebase]

___

## HIGH - Design Principle Violations

[Violations of SOLID principles or separation of concerns but contained to specific modules]

___

## MEDIUM - Code Quality Issues

[Issues worth addressing but don't block functionality or create architectural risk]

___

## LOW - Minor Improvements

[Nice-to-have, improve consistency but do not affect correctness or maintainability]

___

## NOT VIOLATED - Standards Already Met

These areas were checked and found compliant:

| Standard | Status | Notes |
|----------|--------|-------|
| [Standard Checked] | PASS | [Notes] |

___

## 🃏 The Cluster Deck

> **How to use**: Work through one cluster at a time — fix everything in the area before moving on. Within each cluster, cards run highest-to-lowest severity. Boss cards are the entry point for clusters with 3+ issues. Check off cards as you go.
>
> **Card types**: 🔥 Arch | ⚙️ Design | 🧹 Quality | 🗃️ Data | ♿ Access | 👾 Boss
>
> **Difficulty**: 🟢 Quick (<30 min) | 🟡 Medium (30-60 min) | 🔴 Large (1-3 hr) | ⚫ XL (3+ hr)
>
> **Risk**: Low (isolated) | Medium (shared interface) | High (core component)

### Cluster: [Module / File Area]

Files: `[file paths]`
Total: [n] cards | Est. effort: [time] | Risk ceiling: [highest risk level in cluster]

| # | Done | Card | Type | Difficulty | Risk | Time |
|---|------|------|------|------------|------|------|
| 1 | [ ] | [BOSS-001] | 👾 | 🔴 | High | 90 min |
| 2 | [ ] | [ARCH-001] | 🔥 | 🔴 | High | 45 min |
| 3 | [ ] | [QUALITY-002] | 🧹 | 🟡 | Low | 20 min |

**Total estimated effort**: [hour estimate]

```
