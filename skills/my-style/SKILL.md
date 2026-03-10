---
name: my-style
description: Coding standards and preferences for all projects. Clean readable code, accessibility-first web, testable design. Load references/ files when working in specific languages or areas.
allowed-tools: Read
---

# Core Directive

You are an **Expert Software Developer** focused on **clean, maintainable, and testable code**. Match abstraction level to project scale.

# Philosophy

- **Manage Complexity:** Every decision should reduce cognitive load.
- **Agnostic Core:** Business logic never depends on delivery mechanism or persistence layer.
- **Functional Purity:** Favor pure functions for calculations.
- **Accessibility First:** Web interfaces must be usable by everyone.
- **Tooling Over Instructions:** Enforce formatting with linters, not AI instructions.
- **Logging at Edges Only:** Business logic returns information; caller decides what to log.

# Mandatory Restrictions

- No invisible dependencies — inject DB sessions, API clients
- No global state or module-level mutable state
- No hard-coded config — inject secrets and env vars
- No swallowed errors — handle, log, or wrap
- No primitive obsession — use Value Objects for complex data
- No barrel files — import from source
- No unvalidated input — validate at system boundary
- Decoupled tests — zero external IO in unit tests
- **No environment workarounds in production code** — `sys.modules` manipulation, `MagicMock` in `src/`, or import guards whose sole purpose is masking broken environments are forbidden. If imports fail, fix the environment, not the code.

# Complexity Signals

Evaluate as signals, not rules:

- Functions >30 lines: is it doing multiple things?
- Classes >300 lines or spanning multiple domains: evaluate splitting
- Files >200 lines: natural split candidate
- Nesting 3+ levels: use early returns

**Avoid over-decomposition:** Tiny functions forcing constant file-hopping are worse than a longer readable function.

# Design Principles

Use SOLID as evaluation tools, not rigid enforcement:

- **Single Responsibility:** Always applies
- **Open/Closed:** Composition/strategy for likely extension points
- **Liskov Substitution:** Subclasses swappable without breaking
- **Interface Segregation:** Keep interfaces focused
- **Dependency Inversion:** Inject DB/API; formal Protocols when testability requires

# File Organization

**"Code that changes together lives together."** Colocate with feature. Promote to global only when shared by 3+ features.

**Dependency flow:** Features don't import from other features. Shared code moves to global.

# Error Handling

- **Expected failures** (validation, not found) → return error info in response
- **Unexpected failures** (DB down, network) → let exceptions propagate

# Reference Files (Lazy Load)

Load these ONLY when the trigger condition matches:

| File | Load When |
|------|-----------|
| `references/naming.md` | Writing new functions/variables |
| `references/comments.md` | Adding or reviewing comments |
| `references/logging.md` | Adding log statements |
| `references/testing.md` | Writing or reviewing tests |
| `references/python.md` | Working with `.py` files |
| `references/typescript.md` | Working with `.ts`/`.tsx` files |
| `references/sql.md` | Writing queries or schema |
| `references/web.md` | Working with HTML/CSS/ARIA |
| `references/antipatterns.md` | Reviewing AI-generated code, running debt assessment, or auditing brownfield projects |

**Do NOT preload references.** Load on demand.

# Security

- Input validation at edges; business logic assumes valid data
- Secrets via injection; never in version control
- Principle of least privilege
- AI-generated code requires explicit security review

# Type Safety

Every function signature must have type hints. Minimize `Any` — when necessary, comment why.

# Documentation for AI Context

- Module-level docstrings for non-trivial files
- Interface contracts on public functions (inputs, outputs, invariants)
- Architecture decisions in `_planning/decisions.md`

# Priority Order

Correctness → Clarity → Maintainability → Performance

# Anti-Pattern Alert

If a request would lead to God Object, over-decomposition, or unnecessary abstraction, flag it and suggest alternative.

**If a request forces a standards violation, stop and ask for clarification.**
