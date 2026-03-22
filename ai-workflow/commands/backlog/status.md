---
description: Show a summary of the backlog — counts by type and status, recent additions, and stale items. Read-only. Use to get a quick picture of what's queued up without opening four files.
allowed-tools: Read, Glob
---

# Backlog Status

## Steps

1. **Check for backlog directory**: If `_planning/backlog/` doesn't exist, say "No backlog found. Run `/backlog:init` to set one up." and stop.

2. **Read all catalog files**: `bugs.md`, `features.md`, `questions.md`, `data-changes.md`. Parse all entries (look for `### [PREFIX]-NNN` headings and their `**Status:**` fields).

3. **Check inbox**: Read `_inbox.md` and count items below the `---` separator (non-empty bullets or paragraphs).

4. **Build the status report**:

   ```
   📋 Backlog Status
   ═══════════════════════════════

   📥 Inbox: N items waiting for triage

   🐛 Bugs
      open: N  │  planned: N  │  shipped: N  │  wont-fix: N

   ✨ Features
      open: N  │  planned: N  │  shipped: N  │  wont-fix: N

   🤔 Questions
      open: N  │  planned: N  │  shipped: N  │  wont-fix: N

   📊 Data Changes
      open: N  │  planned: N  │  shipped: N  │  wont-fix: N

   ═══════════════════════════════
   Total open: N  │  Total planned: N  │  Total shipped: N
   ```

5. **List open items** (if any exist, grouped by type):

   ```
   📌 Open Items
   ─────────────
   🐛 B-003 — Login crash on empty password
   🐛 B-005 — Progress bar overflows on small screens
   ✨ F-012 — Dark mode toggle
   ✨ F-018 — Export to CSV
   🤔 Q-001 — Should we support offline mode?
   📊 D-002 — Add advanced skating drills
   ```

6. **Flag stale items**: If any open items haven't changed status since they were created and the catalog has 10+ shipped items (suggesting the project is active), note them: "🕸️ These items have been open for a while — worth reviewing?"

7. **Suggest next action**:
   - If inbox has items: "Run `/backlog:triage` to process the inbox."
   - If there are open items but no planned items: "Consider pulling items into your next feature with `/plan:feature`."
   - If everything is shipped/closed: "🎉 Backlog is clear!"

## Rules

- Read only — do not modify any files
- Keep output concise — this is a dashboard, not a report
- Omit sections with zero entries (e.g., don't show Data Changes if there are none)

$ARGUMENTS
