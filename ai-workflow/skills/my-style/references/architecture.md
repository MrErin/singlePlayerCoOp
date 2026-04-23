# Architecture Guardrails

Rules for structural decisions. Load when creating new modules, adding cross-layer dependencies, or extending the data/service layer.

## Dependency Direction

- Dependencies flow one way: UI → Services → Data → Infrastructure
- High-level modules never import from low-level modules
- Backend never imports from frontend
- Shared types live in a neutral package, not owned by any layer
- `TYPE_CHECKING` guards are for type-only imports, not for hiding circular dependencies — if you can't import without it, you have a circular dependency; fix the structure

## Separation of Concerns

- **Models:** Pure data, no behavior, no imports from service/DB/UI layers
- **Repositories / DB:** Pure CRUD, no business logic beyond data access
- **Services / orchestration:** Business logic lives here, not in UI or DB
- **UI / views:** Thin rendering layer, no business logic, no direct DB access
- **Bridge / query layer:** If one exists, use it consistently — don't let higher layers bypass it
- Functions that take a container/context object and reach into multiple subsystems are a coupling smell

## Data Layer

- Schema changes require a migration system — never manual SQL or `CREATE TABLE IF NOT EXISTS` as a migration strategy
- Column lists appear in ONE place (model or constant), not copy-pasted across INSERT/SELECT/UPDATE
- Repositories are single-responsibility — one per conceptual domain
- Query results map to typed models, not raw tuples/dicts
- Adding a new table should touch ≤3 files: model + migration + repository
- Adding a new column should touch ≤3 files: model + migration + repository

## External Service Integration

- Adding a provider should require changing ≤3 files (factory, config, adapter)
- Provider config is externalized (env vars, config file), never hardcoded
- Retry logic distinguishes transient errors (rate limits, timeouts) from permanent errors (auth, invalid request)
- Error handling is consistent across all provider callers
- Structured output has validation, fallback parsing, and truncation recovery
- Dead code paths for handling provider differences (denylist AND config flag for same concern) are a smell

## Error Handling Structure

- Domain errors (invalid state, business rule violations) are separate types from infrastructure errors (DB failure, network)
- Callbacks invoked from your code are error-wrapped — a callback that raises crashes the caller
- Functions return domain-specific error types, not `None` on failure — callers may not check for `None`
- Error paths include useful context (what operation failed, what input caused it)

## Configuration

- Constants are defined in one place, not scattered across modules
- Display names / user-facing strings are never duplicated between constants and view layer
- Enum values are self-describing — no separate display-name mapping dict that must be manually kept in sync
- Provider-specific config values (env vars, URLs) are defined in one place only

## Code Duplication

- Column lists, filter strings, and exclusion patterns are never duplicated across methods
- Input preparation logic is shared between single-call and batch versions of the same function
- Two functions doing the same thing with slightly different signatures → consolidate

## Extensibility

Before adding a new structural element (table, provider, screen, enum value), estimate the file touch count:
- **Low friction (1-3 files):** Good — follows existing patterns
- **Medium friction (4-6 files):** Acceptable — document the pattern
- **High friction (7+ files):** Stop — this needs a prerequisite refactoring, not more boilerplate

Each "high friction" scenario is a candidate for a prerequisite refactoring before the next feature.
