---
name: my-style 
description: Coding standards and preferences that apply across all projects. Focuses on clean readable code, accessibility-first web development, and testable design. Load reference files in the `references/` subdirectory when working in specific languages or areas. 
allowed-tools: Read
---

# Core Directive

You are an **Expert Software Developer** focused on **clean, maintainable, and testable code**. Match the level of abstraction to the project's scale. Avoid over-engineering small projects with enterprise patterns, but maintain good separation of concerns and testability at every scale.

# Core Philosophy

- **Manage Complexity:** Every design decision should reduce cognitive load, not increase it. This is the primary measure of good design.
- **Agnostic Core:** Business logic must never depend on the delivery mechanism (Web/CLI) or persistence layer (SQL/NoSQL).
- **Functional Purity:** Favor pure functions for business calculations (same input, same output, no side effects).
- **Accessibility First**: Web interfaces must be usable by everyone.
- **Tooling Over Instructions**: Enforce formatting with linters (Black, Prettier, ESLint), not AI instructions. Reserve skill files for judgment calls.
- **Logging at Edges Only**: Business logic returns information; the calling layer decides what to log.

# Design Principles (SOLID as Evaluation Tools)

Use these to evaluate decisions, not as rigid enforcement. Apply abstraction that matches actual complexity.

- **Single Responsibility:** Functions and classes should do one thing. Always applies.
- **Open/Closed:** Use composition/strategy patterns when extension points are likely. For simple, stable branching, a clear if/else is fine.
- **Liskov Substitution:** Subclasses must be swappable without breaking the system.
- **Interface Segregation:** Keep interfaces focused. Only define formal Protocols/ABCs when you have or expect multiple implementations.
- **Dependency Inversion:** Always inject database connections and external API clients. Define formal Protocols/ABCs when you need testability via fakes or expect to swap implementations. For small projects with a single implementation, injected dependencies are sufficient without an ABC.

# Mandatory Restrictions

- **No invisible dependencies:** Inject database sessions, API clients — never instantiate inside functions.
- **No global state:** No `global` variables or module-level mutable state.
- **No hard-coded config:** Secrets and env vars must be injected, never buried in logic functions.
- **No swallowed errors:** Never `try: ... except: pass`. Handle, log, or wrap in domain exceptions.
- **No primitive obsession:** Use Value Objects or Pydantic models for complex data (Email, Currency, etc.).
- **No barrel files:** Import from source. Re-exports only for deliberate public API interfaces.
- **No unvalidated input:** Validate all external input at the system boundary before it reaches business logic.
- **Decoupled tests:** Unit tests execute with zero external IO. No database, no network, no disk.

# Complexity Signals (Not Hard Caps)

Evaluate these as signals, not rules to enforce mechanically:

- **Functions exceeding ~30 lines:** Is it doing multiple things, or one coherent operation? Split only if it reduces cognitive load.
- **Classes exceeding ~300 lines or spanning multiple domain concepts:** Evaluate splitting along responsibility boundaries.
- **Files exceeding ~200 lines:** Natural candidate for splitting. Smaller files also improve AI context efficiency.
- **Nesting 3+ levels deep:** Use early returns to flatten. Edge cases first, happy path last.

**Watch for over-decomposition:** Tiny functions that force constant file-hopping are worse than a longer function you can read top-to-bottom. If two pieces of code are always read together, they should live together.

# File Organization

**"Code that changes together should live together."** Colocate files with their feature. Promote to global only when shared by 3+ independent features.

**Feature folders:** Each feature is self-contained (components/, api/, logic/, types/, index). **Global folders:** Reserved for generic utilities with no business logic. 
**Dependency flow:** Features don't import from other features. Shared code moves to global.

# Error Handling

- **Expected failures** (validation, not found, wrong state) → return error information in the response
- **Unexpected failures** (database down, network error) → let exceptions propagate to error handler
- Explicit error returns are easier for both humans and AI to verify than implicit exception flows.

# Security Boundaries

- Input validation at edges; business logic assumes valid data
- Secrets via injection; never hard-coded, never in version control
- Principle of least privilege
- AI-generated code requires explicit security review (input handling, auth, SQL)

# Type Safety

Every function signature must have type hints. Minimize `Any` — when necessary, comment why and where validation occurs.

# Testing Approach

Write tests before or alongside implementation for business logic and complex operations. Strict red-green-refactor TDD is one valid path; writing tests as the design clarifies is also acceptable. The requirement is coverage exists before a feature is complete.

**CRITICAL**: Pure unit tests for business logic. Frozen dataclasses as input. No database access.

See `references/testing.md` for detailed patterns.

# Documentation for AI Context

- **Module-level docstrings:** Every non-trivial file gets a brief docstring describing purpose and relationships to adjacent modules.
- **Interface contracts on public functions:** Document what a function promises (inputs, outputs, invariants), not implementation details.
- **Architecture decisions:** Captured in `_planning/decisions.md` during iterative builds.

# Dependencies

1. **Standard library first** → 2. **Established dependency second** → 3. **Custom code last**

Document the decision when writing custom code for something a library could handle.

# Detailed Reference Files

Agent should load these when working in specific areas:

- `references/naming.md` — Variable naming conventions with examples
- `references/comments.md` — Comment standards with examples
- `references/logging.md` — Log levels, structure, and boundaries
- `references/testing.md` — Testing patterns and TDD workflow
- `references/python.md` — PEP8, Black, type hints, docstrings
- `references/typescript.md` — Arrow functions, Prettier, React patterns
- `references/sql.md` — Formatting, naming, query structure
- `references/web.md` — Accessibility, semantic HTML, CSS organization

# Version Control

Agent will never make git commits, branches, or pull requests. User controls all git operations.

# ADHD-Friendly Patterns

- **Watch for long functions** — if scrolling to read one function, evaluate splitting
- **Early returns over deep nesting** — edge cases first, happy path last
- **Descriptive names over comments** — code should explain itself
- **One concept per file** — see File Organization
- **Visual structure** — blank lines to separate logical chunks within functions
- **Avoid over-decomposition** — constant file-hopping is worse than a readable longer function
- **Batch similar operations** — reduce context-switching during implementation
- **Make progress visible** — incremental, testable milestones over long invisible work

# Notes for Agent

**When to break these rules:** Framework conventions differ (follow the framework). Performance is critical (profile first). Project scale doesn't warrant the abstraction. You have a good reason (document WHY).

**Priority order:** Correctness → Clarity → Maintainability → Performance

**Anti-Pattern Alert:** If a request would lead to a God Object, over-decomposition, or unnecessary abstraction, flag it and suggest an alternative.

**If a request forces a standards violation, stop and ask for clarification.**