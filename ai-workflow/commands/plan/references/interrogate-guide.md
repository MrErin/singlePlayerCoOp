# Requirements Interrogation Guide

Load this file when conducting requirements interviews. Contains detailed probing questions for each section.

---

## Section 1: Problem & Purpose

### Questions to Ask
- What problem does this solve?
- Who uses it? ("Just me" is valid but has architectural implications)
- What's the current workaround, and what's frustrating about it?
- Why a custom tool and not [research existing alternatives first]?

### Push Back If
- Problem is vague ("I want to track things" — what, why, to what end?)
- Scope sounds like three different apps
- "Why not existing tool" answer is weak — if Notion/Obsidian obviously solves this, say so

---

## Section 2: User Stories

### Process
1. "What's the first thing someone should be able to do?"
2. Shape into story: "As a [user], I want to [action] so that [value]"
3. "How would we know this works?" → acceptance criteria
4. "What else?" → repeat until done
5. Review list together

### Push Back If
- Acceptance criteria are vague ("it should work correctly")
- Story sounds like two stories collapsed
- Story implies un-discussed infrastructure (real-time → websockets; sharing → auth)

---

## Section 3: Tech Stack

### Questions to Ask
- Backend language/framework
- Frontend approach (if any)
- Database choice
- Deployment target (local? home server? cloud?)

### Push Back If
- Stack mismatched to problem (heavy React for single-user CLI)
- Dependency added without clear reason
- Reaching for complex when simple would work

### For Established Stack Users
Confirm rather than re-litigate: "You typically use Flask + SQLite — does that apply here?"

---

## Section 4: Data Model

### Questions to Ask
- Core entities (nouns in user stories → tables)
- Key relationships (1:1, 1:N, M:N, optional or required?)
- Any entities with unclear structure

### Load-Bearing Decisions (Push Hard)
- Many-to-many relationships (junction tables — not easy to add later)
- Hierarchies or tree structures
- Polymorphic entities
- Soft deletes vs hard deletes
- Single-user vs multi-user (touches everything if added later)

### Frame It
"Specific fields can change later. What matters now is structure — which entities exist and how they relate."

---

## Section 5: Future Features

### Process
1. "What might this app need in a year that it doesn't need in v1? Be speculative."
2. Collect without filtering
3. For each: "Does the data model support this, or would we need to restructure?"
4. If restructuring needed: "Likely enough to account for now?"

### Common Failure Modes to Probe
- Multi-user on single-user schema
- Reporting requiring denormalization
- Tags/categories on entities without them
- History/audit trails on mutable entities
- New relationships between existing entities

---

## Section 6: Business Rules & Validation

### Question
"Are there rules about what data is valid, what actions are allowed, or what should be prevented?"

### Guidance
Only document non-obvious rules. Skip standard validation (required fields, email format, positive numbers).

### Push Back If
- Rule hides a missing user story
- Rule contradicts earlier decision

---

## Section 7: UI/UX

### Explore
- Key screens and their purpose
- Information hierarchy that matters ("timer must always be visible")
- Mobile considerations
- Specific interactions that matter

### Do Not Discuss
UI components, CSS frameworks, animation libraries — those belong in polish phase.

---

## Section 8: Non-Functional Requirements

### Only Ask What's Likely Relevant
- Performance (if significant volume or concurrent users)
- Security (if sensitive data or non-developer users)
- Accessibility (WCAG level?)
- Browser/platform support
- Offline capability

### Skip anything that clearly doesn't apply.

---

## Section 9: Out of Scope

### Question
"Is there anything we discussed — or that might seem obvious — that should be out of scope for v1?"

### Also
Review Future Features list. Confirm which are explicitly deferred.

---

## Interview Behavior

### Core Principles
- One topic at a time. Never present a numbered list of questions.
- Follow up on vague answers. "I'll figure it out later" is OK for soft decisions, not load-bearing ones.
- Name tradeoffs honestly. User can override, but should do it with information.
- Park what can't be decided. Add to Open Questions, move on.

### Load-Bearing vs Soft Decisions
- **Load-bearing:** data model, auth, multi-user, state management, anything hard to refactor
- **Soft:** field names, UI copy, minor business rules, validation messages

### For Mode B/C (Existing Project)
Treat `decisions.md` as settled ground. Don't re-ask answered questions.

### Package Feasibility Check

Before accepting any third-party dependency as part of the solution:

1. **Verify via Context7** — check the package docs for the specific capability needed
2. **Name limitations explicitly** — if a package does 80% but not the critical 20%, say so
3. **Don't assume** — "there's probably a library for that" is not a plan

Common failure modes:
- Assuming a JS framework has built-in state management it doesn't
- Assuming a Python library handles async when it doesn't
- Assuming a database supports a query pattern it doesn't

If you can't verify, flag it as an Open Question: "Need to confirm [package] supports [feature]."
