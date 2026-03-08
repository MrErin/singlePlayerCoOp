# Codebase Map

## Stack
- **Runtime:** [e.g., Node.js 20 via nvm]
- **Framework:** [e.g., React 19 + TypeScript (Vite)]
- **Styling:** [e.g., Tailwind CSS]
- **Key dependencies:** [list with versions]
- **Dev tools:** [linter, formatter, test runner]

## Structure
[directory tree of project — src/ level detail, not individual files]

## Key Files
- **Entry point:** [e.g., src/app.py, src/main.tsx]
- **Core business logic:** [e.g., src/services/xp_calculator.py]
- **Data layer:** [e.g., src/database.py, src/models/]
- **Configuration:** [e.g., .env.example, config.py]

## Architecture
- **Data flow:** [how data moves through the app]
- **State management:** [local state, context, store, etc.]
- **Routing:** [if applicable]
- **Key patterns:** [anything a new session needs to know]

## Patterns & Conventions

### Key Patterns Used
[List architectural patterns observed in the codebase]
- [e.g., Repository pattern for data access]
- [e.g., Service layer for business logic]
- [e.g., Factory pattern for object creation]
- [e.g., Observer pattern for event handling]

### Naming Conventions
[Document naming patterns observed in the project]
- **Files:** [e.g., kebab-case for components, PascalCase for classes]
- **Functions:** [e.g., camelCase, verb prefixes like get/set/handle]
- **Classes:** [e.g., PascalCase, suffixes like Service, Repository, Factory]
- **Constants:** [e.g., SCREAMING_SNAKE_CASE]
- **Database:** [e.g., snake_case tables, singular vs plural names]

### Module Boundaries
[How modules are organized and what each is responsible for]
- **[module-name]:** [responsibility, what it exports, who depends on it]
- **[module-name]:** [responsibility, what it exports, who depends on it]

### Dependency Flow
[Direction of dependencies — what can import what]
- [e.g., "UI → Services → Repository → Database" or "No circular imports between modules"]
- [e.g., "Shared utilities have no dependencies on business logic"]

### Import Conventions
[How imports are organized and any project-specific patterns]
- **Order:** [e.g., standard library → third-party → local modules]
- **Aliases:** [e.g., @/ for src/, any path mappings]
- **Barrel exports:** [e.g., index.ts files re-exporting from directories]

## Integrations
[Only include if project has external APIs, databases, or services]
- **[Service name]:** [what it does, auth method, relevant endpoints]