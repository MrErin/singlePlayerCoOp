---
description: Generate or update the technical_debt document for a brownfield project. Use to assess existing code base against preferences and best practices outlined in my-style skill
allowed-tools: Bash, Read, Write, Grep, Glob
---

# Assess Technical Debt

**Skill:** Load `my-style`
**No git commits.**

## Steps

1. **Read**: `_planning/codebase.md` to understand project structure. Read `_planning/requirements.md` and `_planning/decisions.md` for context.
	1. If the `_planning` directory does not exist, STOP. Instruct the user to run /plan:init first.
2. **Index with jcodemunch**: If the project isn't indexed, run `index_folder` on the source directory. Use `get_repo_outline` to see module structure, `search_text` to find pattern violations (e.g., string concatenation in queries, manual DB open/close).
3. **Triage**: From `codebase.md`, identify the business logic and core modules. Rank by importance: business logic > data layer > API/routes > utilities > config.
4. **Analyze by module**: For each module (highest priority first), delegate to a `code-reviewer` subagent with that module's files and `my-style` standards. Use jcodemunch `get_file_outline` to see all symbols in each file being reviewed. Evaluate against `my-style` standards plus these debt-specific checks:
	- File organization follows feature-folder pattern
	- DB connections use context managers (no manual open/close)
	- All queries use parameterized syntax (no string concatenation or f-strings)
	- Semantic HTML used appropriately (not div-for-everything)
	- Interactive elements have ARIA labels, keyboard navigation, and focus management
5. **Research**: relevant architectural patterns for the project's language, framework, and type
6. **Generate**: `_planning/technical_debt.md` — read `commands/plan/references/debt-templates.md` for card and document templates
7. **Organize**: issues by severity (most severe at top), identified by their card type and number. Use this template for each issue:
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
8. **Generate the cluster deck**: Group issues into clusters by files/modules they affect. Within each cluster, order highest-to-lowest severity. Order clusters so higher-severity clusters come first; if equal severity, prioritize clusters whose files are touched by other clusters. **Cards in clusters must use the same `[TYPE]-[NNN]` identifiers from step 7** — this lets readers cross-reference between the severity exposition and the action-oriented clusters.
9. **Progressive output**: If >10 issues found, generate the full severity sections and cluster summary tables, but only expand full card details for the top 4 clusters. Add a note: "Run `/plan:debt [cluster-name]` to expand remaining clusters."

## Rules

- Do not rewrite code in codebase
- Provide brief corrected examples in the document when clear
- Explain why each change is necessary

$ARGUMENTS
