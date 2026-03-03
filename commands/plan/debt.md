---
description: Generate or update the technical_debt document for a brownfield project. Use to assess existing code base against preferences and best practices outlined in my-style skill
allowed-tools: bash_tool create_file str_replace view
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
1. **Recommend**: a priority order for addressing issues incrementally, optimizing for focusing effort in the same parts of the app at a given time, prioritizing most severe/critical fixes

## Standards to Evaluate Against
- [ ] No invisible dependencies (injected, not instantiated)
- [ ] No global state
- [ ] No hard-coded config/secrets
- [ ] No swallowed errors
- [ ] No unvalidated input at boundaries
- [ ] Type hints on all public functions
- [ ] Functions under complexity signals
- [ ] File organization follows feature-folder pattern
- [ ] Error handling uses expected/unexpected split
- [ ] Tests exist for business logic (pure, no IO)

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

## Recommended Priority Order and Checklist

[Items in this table/list should appear in priority order]

| Checkbox | Issue Number | Brief Description of Fix | Estimation of Time, Risk to Application, etc. |
|----------|--------|-------|-------|  
| [ ] | [Number] | [Description] | [e.g. 1 hour, zero risk] |
...

**Total Estimated Effort:** [hour estimate]

```


## Rules

- Do NOT rewrite any code in the codebase
- Do NOT make git commits
- Do provide examples of corrected code inside the technical_debt document if that example is brief and clear
- Do provide information for why the change is necessary