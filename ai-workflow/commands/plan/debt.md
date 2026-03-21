---
description: DEPRECATED — use /plan:audit instead. Generates a standalone technical debt document. Retained for reference only.
allowed-tools: Bash, Read, Write, Grep, Glob
---

> **Deprecated**: This command has been replaced by `/plan:audit`, which runs debt analysis and test analysis together and produces both an agent-executable auto-fix list and a gamified human review deck. Do not run this command for new audits.

# Assess Technical Debt

**Skill:** Load `my-style`

## Resume Detection

Before starting, check if `_planning/technical_debt.md` exists with `<!-- STATUS: DRAFT -->`. If so, read it to identify which modules/clusters are already written. Continue from the next unwritten section — do not redo completed analysis.

## Steps

1. **Read**: `_planning/codebase.md` to understand project structure. Read `_planning/requirements.md` and `_planning/decisions.md` for context.
	1. If the `_planning` directory does not exist, STOP. Instruct the user to run /plan:init first.
2. **Map module structure**: Use Glob to enumerate source files and directories. Use Grep to find pattern violations (e.g., string concatenation in queries, manual DB open/close).
3. **Triage**: From `codebase.md`, identify the business logic and core modules. Rank by importance: business logic > data layer > API/routes > utilities > config.
4. **Scaffold the document**: Read `commands/plan/references/debt-templates.md` for card and document templates. Write `_planning/technical_debt.md` with `<!-- STATUS: DRAFT -->`, the document header, and the module priority list. This file is now the working output.
5. **Analyze by module** (highest priority first): Delegate to a `code-reviewer` subagent with that module's files and `my-style` standards. Use Grep for function/class definitions to see all symbols in each file being reviewed. Evaluate against `my-style` standards plus these debt-specific checks:
	- File organization follows feature-folder pattern
	- DB connections use context managers (no manual open/close)
	- All queries use parameterized syntax (no string concatenation or f-strings)
	- Semantic HTML used appropriately (not div-for-everything)
	- Interactive elements have ARIA labels, keyboard navigation, and focus management
	- **Dead code detection** — use Grep to identify:
		- Functions/methods defined but never called (search for function name across codebase)
		- Classes never instantiated or imported elsewhere
		- Public functions with no callers outside their own file
		- Exported symbols that nothing imports
		- Each candidate requires manual verification (grep for false positives like dynamic calls, test fixtures, API endpoints) — do not flag without confirming
		- Create CLEANUP cards for confirmed dead code with HIGH severity
	- **Redundant code detection** — look for:
		- Near-identical functions across files (same logic, different names)
		- Copy-paste artifacts (variable names that don't match their content)
		- Multiple implementations of the same utility
		- Create CLEANUP cards with MEDIUM severity
	- **AI-generated anti-patterns** — read `my-style/references/antipatterns.md` and use Grep to find:
		- CRITICAL patterns first: environment workarounds, error handling issues, mutable defaults
		- HIGH patterns next: state issues, database anti-patterns, testing gaps
		- Each match becomes an ARCH or QUALITY card with severity from the reference

	Create cards using this template:
	```markdown
	### [TYPE]-[NNN]: [Issue Name]
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
	**Write each completed module's cards to the document before moving to the next module.**
6. **Research**: relevant architectural patterns for the project's language, framework, and type. Append findings to the document.
7. **Generate the cluster deck**: Group issues into clusters by files/modules they affect. Within each cluster, order highest-to-lowest severity. Order clusters so higher-severity clusters come first; if equal severity, prioritize clusters whose files are touched by other clusters. **Cards in clusters must use the same `[TYPE]-[NNN]` identifiers from step 5** — this lets readers cross-reference between the severity exposition and the action-oriented clusters.
8. **Finalize**: Generate the severity summary at the top of the document. Replace `<!-- STATUS: DRAFT -->` with `<!-- STATUS: COMPLETE -->`.

## Rules

- Do not rewrite code in codebase
- Provide brief corrected examples in the document when clear
- Explain why each change is necessary

$ARGUMENTS
