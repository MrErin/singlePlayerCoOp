---
description: Process the backlog inbox — classify items, assign stable IDs, apply templates, and append to catalog files. Run on demand after dumping ideas into _inbox.md. Handles ambiguity by asking, never guesses priority, never discards anything.
allowed-tools: Read, Write, Glob
---

# Triage Inbox

## Steps

1. **Read `_planning/backlog/_inbox.md`**.
   - If the file doesn't exist, tell the user to run `/backlog:init` first.
   - If the inbox has no items (only the heading and separator), say "📥 Inbox is empty — nothing to triage." and stop.

2. **Parse items**: Split on bullets (`-`), numbered items (`1.`), or blank-line-separated paragraphs. Each becomes one backlog entry.

3. **For each item, classify**:

   | Type | Prefix | Catalog file | Signal |
   |------|--------|-------------|--------|
   | Bug | `B` | `bugs.md` | Something broken, wrong behavior, error, regression |
   | Feature | `F` | `features.md` | New capability, enhancement, improvement |
   | Question | `Q` | `questions.md` | Uncertainty, design decision, open-ended exploration |
   | Data change | `D` | `data-changes.md` | Seed data, content updates, CSV changes, rebalancing |

   - Honor user-provided prefixes (e.g., `B: fix the login` → bug)
   - If ambiguous (e.g., a bug that implies a feature), **ask the user** — do not guess
   - If an item contains multiple distinct ideas, split them and confirm with the user

4. **Check for duplicates**: Before assigning an ID, scan the target catalog file for entries with similar descriptions. If a potential duplicate exists, flag it: "🔍 This looks similar to existing `F-012` — add as new entry anyway?" Wait for user response.

5. **Assign the next available ID**:
   - Read the target catalog file
   - Find the highest existing ID number for that prefix
   - Assign the next sequential number, zero-padded to 3 digits: `B-001`, `F-014`, `Q-003`
   - IDs are permanent — never renumber, never reuse

6. **Apply the template** and append to the catalog file:

   ### Bug entry
   ```markdown

   ### B-NNN — Short description
   **Status:** open
   **Area:** (infer from context, or leave as "TBD")

   Description of the bug — what happens vs. what should happen.
   ```

   ### Feature entry
   ```markdown

   ### F-NNN — Short description
   **Status:** open
   **Size:** —
   **Spec:** —

   Description. Sub-ideas as bullets if the inbox item had them.
   ```

   ### Question entry
   ```markdown

   ### Q-NNN — Short description
   **Status:** open
   **Relates to:** (link to F/B-NNN if obvious, otherwise "—")

   The question and why it matters. Any initial thoughts from the inbox item.
   ```

   ### Data change entry
   ```markdown

   ### D-NNN — Short description
   **Status:** open
   **Skill/Area:** (infer from context, or leave as "TBD")

   What needs to change in the data.
   ```

7. **Clear triaged items from inbox**: Remove processed bullets/paragraphs but **keep everything above the `---` separator** (the heading, instructions, and type hint legend). Leave a single empty bullet so the file is ready for the next idea:

   ```markdown
   ---

   -
   ```

8. **Report summary**:
   ```
   ✅ Triaged N items:
   • B-004 — Login crash on empty password
   • F-026 — Dark mode toggle
   • F-027 — Export to CSV
   • Q-002 — Should we support offline mode?
   ```

## Edge Cases

- **Multi-line items**: If a bullet has sub-bullets or continuation lines, keep them together as one entry. The sub-bullets become part of the description.
- **Items with existing IDs**: If someone pasted an already-cataloged item (e.g., `F-012 — ...`), skip it and warn: "⚠️ Skipped item that already has an ID: F-012"
- **Huge inbox**: If there are more than 15 items, process in batches of 10 and confirm between batches: "Triaged 10 items so far. Continue with the remaining N?"

## Rules

- **Never assign priority or size** — the user decides during planning
- **Never merge or deduplicate without asking** — flag potential duplicates, let user decide
- **Never discard anything** — every inbox item gets cataloged somewhere
- **Never modify existing catalog entries** — append only
- **Never touch files outside `_planning/backlog/`**
- Keep descriptions concise — don't inflate one-liners into paragraphs

$ARGUMENTS
