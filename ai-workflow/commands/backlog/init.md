---
description: Initialize the backlog system for a project. Creates _planning/backlog/ with catalog files and inbox. Safe to run on existing projects — skips files that already exist. Use when adopting the backlog workflow in a new or existing project.
allowed-tools: Bash, Read, Write, Glob
---

# Initialize Backlog

## Steps

1. **Check for `_planning/`**: If `_planning/` does not exist, warn the user: "No `_planning/` directory found. Run `/plan:init` first to set up the planning workflow, or confirm you want a standalone backlog." Wait for confirmation before continuing.

2. **Check for existing backlog**: If `_planning/backlog/` already exists with catalog files, report what's already there and ask: "Backlog directory already exists. Want me to add any missing files, or is this already set up?"

3. **Create the directory structure**:

   ```
   _planning/backlog/
   ├── _inbox.md
   ├── bugs.md
   ├── features.md
   ├── questions.md
   ├── data-changes.md
   └── specs/            (empty directory)
   ```

4. **Write each file using the templates below.** Skip any file that already exists — never overwrite.

5. **Output**: Confirm what was created. If the project has existing unstructured backlog files (e.g., `changes.md`, `TODO.md`, `backlog.md` in `_planning/` or project root), mention them: "Found existing files that might contain backlog items: [list]. You can paste their contents into `_inbox.md` and run `/backlog:triage` to catalog them."

---

## File Templates

### _inbox.md

```markdown
# 📥 Inbox

Dump ideas here. One bullet per thought — that's the only rule.

If you're feeling organized, prefix with a type hint:
- **B** — bug (something broken)
- **F** — feature (something new)
- **Q** — question (something uncertain)
- **D** — data change (content/seed data)

But don't stress about it. Triage sorts everything out.

---

-
```

### bugs.md

```markdown
# 🐛 Bugs

Tracked bugs with stable IDs. Once assigned, an ID never changes or gets reused.

| Status | Meaning |
|--------|---------|
| `open` | Not yet planned |
| `planned` | Pulled into an active feature |
| `shipped` | Fixed and deployed |
| `wont-fix` | Intentionally declined |

---
```

### features.md

```markdown
# ✨ Features

Feature ideas and enhancements with stable IDs.

**Size guide** (optional — assign during planning, not triage):
- **small** — a few hours, limited scope
- **medium** — a day or two, new UI or backend logic
- **large** — multi-phase, needs full `/plan:interrogate`

| Status | Meaning |
|--------|---------|
| `open` | Not yet planned |
| `planned` | Pulled into an active feature |
| `shipped` | Completed and deployed |
| `wont-fix` | Intentionally declined |

---
```

### questions.md

```markdown
# 🤔 Questions

Open design questions and uncertainties. Questions graduate to features once they have an answer — set status to `shipped` with a note pointing to the new feature entry.

| Status | Meaning |
|--------|---------|
| `open` | Still thinking |
| `planned` | Being addressed in active feature |
| `shipped` | Resolved (see linked feature) |
| `wont-fix` | No longer relevant |

---
```

### data-changes.md

```markdown
# 📊 Data Changes

Content updates, seed data modifications, and dataset tasks.

| Status | Meaning |
|--------|---------|
| `open` | Not yet planned |
| `planned` | Pulled into an active feature |
| `shipped` | Applied and deployed |
| `wont-fix` | Intentionally declined |

---
```

## Rules

- Never overwrite existing files — skip and report
- Always create the `specs/` subdirectory (use `mkdir -p`)
- This command is safe to re-run — it only fills gaps

$ARGUMENTS
