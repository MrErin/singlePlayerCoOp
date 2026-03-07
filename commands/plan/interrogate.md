---
description: Conduct a structured requirements interview to produce a completed requirements.md. Adapts to three contexts - new project (full interview from scratch), new feature (scoped to the feature and its integration points), or clarify existing (targeted gap analysis). Ask one topic at a time, push back on vague answers, discuss tradeoffs critically. Synthesize responses into a running draft that updates after each section. Use before /plan:init on any new project or feature. 
allowed-tools: bash_tool create_file str_replace view
---

# Requirements Interrogation

## Purpose

Produce a completed `requirements.md` through conversation — not by handing the user a template. Ask focused questions, challenge vague answers, name real tradeoffs, and synthesize responses into a running draft that grows section by section.

**Critical behavior:** You are not a yes-machine. If an approach has real costs, name them. If an acceptance criterion is untestable, say so. If a data model decision will be painful to undo later, flag it before moving on. The goal is a requirements doc that reflects considered decisions, not a transcription of first instincts.

---

## Step 1: Context Detection

Read the project directory before asking anything. Determine which mode applies:

### Mode A: New Project

**Signals:** No `_planning/` directory exists, or it exists but has no `requirements.md` and no significant codebase.

**Action:** Full interview from scratch. Follow the New Project Interview sequence. **Output:** `_planning/requirements.md`

### Mode B: New Feature

**Signals:** `_planning/` exists, a codebase exists, user invokes with a feature name or description.

**Read first:** `_planning/roadmap.md`, `_planning/decisions.md`, `_planning/codebase.md`, any phase summaries that exist, and `_planning/project-requirements/index.md` if it exists. Use what you find — don't ask questions you can already answer from context.

**Check:** If `_planning/requirements.md` already has active content (not the empty placeholder), warn the user: "requirements.md has content from a previous feature scope. If that feature is complete, run `/plan:archive` before starting new requirements — otherwise new content will overwrite it. Proceed anyway?"

**Action:** Scoped interview covering what's new and how it integrates with what already exists. **Output:** `_planning/requirements.md`

### Mode C: Clarify Existing Requirements

**Signals:** `_planning/requirements.md` exists with content. User invokes to fill gaps or resolve ambiguity.

**Read first:** `_planning/requirements.md`, `_planning/decisions.md` if it exists, and `_planning/project-requirements/index.md` if it exists.

**Action:** Identify gaps, vague acceptance criteria, undecided data model questions, and contradictions. Interview only about those areas. Don't re-litigate settled decisions. **Output:** Update `_planning/requirements.md` in place.

**If unclear:** Ask — "Are we starting a new project, adding a feature to an existing one, or clarifying something in an existing requirements doc?"

---

## Step 2: Running Draft

Create or open the output file before starting the interview. After completing each section, write or update the file immediately. Tell the user when you've done so: "I've updated the draft with [section name]."

Don't wait until the end to synthesize. The user should be able to stop the interview at any point and have a useful (if incomplete) document.

---

## Step 3: Interview Behavior

**One topic at a time.** Never present a numbered list of questions. Finish exploring one area before moving to the next.

**Follow up on vague answers.** "I'll figure it out later" is acceptable for soft decisions. It is not acceptable for load-bearing ones (see below). Ask again with more specificity.

**Distinguish load-bearing from soft decisions:**

- _Load-bearing:_ data model structure and relationships, authentication approach, multi-user vs. single-user, state management architecture, any decision that would require significant refactoring to change. Push hard on these.
- _Soft:_ specific field names, UI copy, color choices, minor business rule details, exact validation messages. Let these slide — they can be adjusted later.

**Name tradeoffs honestly.** If the user's preference has a real downside, say so and offer alternatives. They can override your recommendation, but they should do it with information.

**Park what can't be decided.** If something genuinely can't be resolved now, add it to the Open Questions section and move on. Don't let a hard question stall the whole interview.

**For Mode B and C:** Treat `decisions.md` as settled ground. Don't re-ask questions that are already answered there.

---

## New Project Interview Sequence

Work through these sections in order. After each one, update the draft and check it off. When all are checked, move to Coverage Confirmation.

```
Checklist:
[ ] 1. Problem & Purpose
[ ] 2. User Stories
[ ] 3. Tech Stack
[ ] 4. Data Model
[ ] 5. Future Features
[ ] 6. Business Rules & Validation
[ ] 7. UI/UX
[ ] 8. Non-Functional Requirements
[ ] 9. Out of Scope
[ ] 10. Coverage Confirmation
```

---

### Section 1: Problem & Purpose

**Goal:** Understand the problem, the user, and why this instead of an existing tool.

**Explore:**

- What problem does this solve?
- Who uses it? ("Just me" is a complete answer — but it has architectural implications worth naming.)
- What's the current workaround, and what's frustrating about it?
- Why a custom tool and not [research obvious existing alternatives before asking this]?

**Push back if:**

- The problem is vague — "I want to track things" needs a follow-up about what, why, and to what end.
- The scope sounds like three different apps.
- The "why not existing tool" answer is weak — if Notion or Obsidian obviously solves this, say so.

**Draft update:** Write the project name and Overview section.

---

### Section 2: User Stories

**Goal:** Capture what the app must actually do, in user terms, with testable acceptance criteria.

**Process:**

1. Ask: "What's the first thing someone should be able to do with this app?"
2. Help shape it into a proper user story if needed: "As a [user], I want to [action] so that [value]."
3. Ask for acceptance criteria: "How would we know this works? What are the specific conditions?"
4. Ask: "What else should users be able to do?" Repeat until the user stalls or says they're done.
5. Review the list together: "Here's what we have — does this cover everything that needs to be in v1?"

**Push back if:**

- Acceptance criteria are vague ("it should work correctly" — define correctly).
- A story sounds like two stories collapsed into one.
- A story implies significant infrastructure that hasn't been discussed — name it. (e.g., "see updates in real time" implies websockets; "share with my team" implies authentication.)

**Draft update:** Write user stories as they're finalized.

---

### Section 3: Tech Stack

**Goal:** Confirm the stack and flag mismatches with the problem.

**Explore:**

- Backend language/framework
- Frontend approach (if any — not all apps need one)
- Database choice
- Deployment target (local only? home server? cloud?)

**Push back if:**

- Stack choice is mismatched to the problem (heavy React frontend for a single-user CLI tool, for example).
- A dependency is being added without a clear reason.
- The user is reaching for something complex when something simpler would work.

**For established stack users:** Confirm rather than re-litigate. "You typically use Flask + SQLite — does that apply here, or is there a reason to do something different?"

**Draft update:** Write the Tech Stack section.

---

### Section 4: Data Model

**Goal:** Identify core entities and get the load-bearing structural decisions right. Fields can be adjusted; relationships are expensive to undo.

**Explore:**

- Core entities — the nouns in the user stories are usually the tables.
- Key relationships — one-to-many? many-to-many? Is the relationship optional or required?
- Any entities where the "right" structure isn't obvious.

**Flag explicitly (these are load-bearing):**

- Many-to-many relationships (junction tables — "easy to add later" is rarely true).
- Entities that might need hierarchy or tree structure.
- Anything that might need to be polymorphic.
- Whether soft deletes vs. hard deletes matter for any entity.
- Single-user vs. multi-user — if multi-user is possible later, say so now. It touches nearly everything.

**Frame it clearly:** "The specific fields can be added or changed later without much pain. What I want to get right now is the structure — which entities exist and how they relate to each other."

**Note for the draft:** Domain fields only. Agent will add id, timestamps, foreign keys, and indexes. Note any non-obvious required fields explicitly.

**Draft update:** Write the Data Model section.

---

### Section 5: Future Features

**Goal:** Stress-test the data model against plausible future needs. Not a backlog — a check that the foundation doesn't accidentally foreclose likely options.

**Process:**

1. Ask: "Think about what this app might need to do in a year that it doesn't need to do in v1. Be loose — even speculative ideas are useful here."
2. Collect ideas without filtering.
3. For each idea, ask: "Does the data model we just discussed support this, or would we need to restructure something?"
4. If restructuring would be needed: "Is this likely enough that we should account for it now, or is it truly speculative?"

**Common failure modes to probe:**

- Adding multi-user support to a single-user schema
- Adding reporting or aggregations that require denormalization
- Adding tags, categories, or classification to entities that don't have them
- Adding history or audit trails to mutable entities
- Adding relationships that currently don't exist between entities

**If a future feature reveals a structural gap:** Update Section 4 accordingly before moving on.

**Draft update:** Write the Future Features section. If Section 4 changed, update it too.

---

### Section 6: Business Rules & Validation

**Goal:** Capture non-obvious rules that govern what the app should and shouldn't allow.

**Ask:** "Are there any rules about what data is valid, what actions are allowed, or what should be prevented?"

**Only document what's non-obvious.** Skip standard validation (required fields, email format, positive numbers). Agent already knows those. Document the rules that are specific to this domain and wouldn't be guessed from the user stories alone.

**Push back if:**

- A rule sounds like it's hiding a missing user story.
- A rule contradicts an earlier decision.

**Draft update:** Write the Business Rules section.

---

### Section 7: UI/UX

**Goal:** Describe the experience, not the implementation. Screens and interactions — not components or libraries.

**Explore:**

- Key screens and what they accomplish
- Information hierarchy that matters ("the timer must always be visible while working")
- Mobile considerations if relevant
- Any specific interaction that's important to get right

**Do not discuss:** specific UI components, CSS frameworks, animation libraries, or implementation approaches. Those belong in Phase 5.

**Draft update:** Write the UI/UX section.

---

### Section 8: Non-Functional Requirements

**Goal:** Capture constraints that affect how the app is built but aren't features.

**Only ask about what's likely to matter for this specific project:**

- Performance (if significant data volume or concurrent users)
- Security (if sensitive data or users other than the developer)
- Accessibility (WCAG level?)
- Browser/platform support
- Offline capability

**Skip anything that clearly doesn't apply.** A single-user local tool doesn't need a concurrent users section. Don't pad this.

**Draft update:** Write the Non-Functional Requirements section.

---

### Section 9: Out of Scope

**Goal:** Explicitly document what v1 will not include, to prevent scope creep during the build.

**Ask:** "Is there anything we discussed — or anything that might seem obvious — that should explicitly be out of scope for v1?"

**Also:** Review the Future Features list together. Confirm which items are explicitly deferred to post-v1.

**Draft update:** Write the Out of Scope section.

---

### Section 10: Coverage Confirmation

When all sections are checked:

1. Present a summary: "Here's what we've covered: [one-line summary of each section]."
2. Ask: "Does anything feel missing, unclear, or underdecided?"
3. Review the Open Questions section together. For each item: is it genuinely deferrable, or does it need a decision before building starts?
4. Tell the user: "Your requirements doc is at `_planning/requirements.md`. Take a look and make any edits you want before running `/plan:init`. You don't need to finalize everything — you can always revisit with `/plan:interrogate` before starting a phase."
5. **STOP. Do not run `/plan:init` automatically.**

---

## New Feature Interview Sequence

```
Checklist:
[ ] 1. Read existing context
[ ] 2. Feature definition & user stories
[ ] 3. Integration points with existing code
[ ] 4. Data model changes
[ ] 5. Business rules specific to this feature
[ ] 6. UI/UX for this feature
[ ] 7. Out of scope for this feature
[ ] 8. Coverage confirmation
```

Read `_planning/decisions.md`, `_planning/codebase.md`, and relevant phase summaries before the first question. Use what you find to ask informed questions and avoid re-asking anything already decided.

Treat `decisions.md` entries as settled ground unless the user explicitly raises one.

Output to `_planning/requirements.md`.

---

## Clarify Existing Requirements Sequence

1. Read `_planning/requirements.md` (and `decisions.md` if it exists).
2. Identify: vague acceptance criteria, missing data model structure decisions, undefined business rules, thin or contradictory sections.
3. Present findings clearly: "I found [N] things that could use more definition before building. Want to work through them?"
4. Work through gaps one at a time using the same interview behavior as above.
5. Update the file as each gap is resolved.
6. Confirm when done.

---

## Rules

- Do NOT run `/plan:init` or any build command. Planning only.
- Do NOT make git commits.
- Do NOT ask all questions at once.
- Do NOT accept vague answers for load-bearing decisions.
- DO update the draft file after each completed section.
- DO name tradeoffs honestly — the user can override, but should do so with information.
- DO use existing context (decisions.md, codebase.md, phase summaries) to avoid re-asking settled questions.

$ARGUMENTS