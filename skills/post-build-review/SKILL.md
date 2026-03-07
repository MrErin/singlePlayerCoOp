---
name: post-build-review 
description: Generate comprehensive review documentation after completing a build. Creates ADHD-friendly guides with checkboxes, time estimates, and progressive disclosure to help users test, understand, and extend the codebase without feeling overwhelmed. 
allowed-tools: Read, Write
---

# Post-Build Review Skill

## Purpose

Generate review documentation after completing any multi-file project or iterative build.

**Output Location:** `_planning/review_guide.md`

## ADHD-Friendly Requirements (Critical)

**Every section must include:**

- [ ] **Checkboxes** for progress tracking
- [ ] **Time estimates** (realistic, not rushed)
- [ ] **Clear structure** with numbered steps
- [ ] **Expected output** after each step

**Document structure:**

- Progressive disclosure (simple → complex)
- Short sections (5-20 min each)
- Can be completed in multiple sessions
- Clear stopping points

## Required Sections

### 1. Quick Start (5 minutes)

**Goal:** Get the app running to verify it works

**Include:**

- Prerequisites checklist
- Numbered setup steps
- Expected output after each step
- "If all steps work, proceed. If not, see Troubleshooting"

### 2. Feature Testing Checklist (15-20 minutes)

**Goal:** Test each feature to understand what the app does

**For each feature:**

- Brief description: "What it does"
- Test steps (checkboxes)
- Expected results
- How to verify (database queries if applicable)
- Common troubleshooting

**Format:** One feature per subsection with clear boundaries

### 3. Code Understanding Guide (30-45 minutes)

**Goal:** Learn the codebase in logical order (not alphabetical)

**Structure as levels:**

- **Level 1: Data Structure** - CSV files, schemas, static data
- **Level 2: How Data Flows** - Init scripts, data loading
- **Level 3: Application Logic** - Routes, business logic
- **Level 4: Database Operations** - Queries, functions
- **Level 5: Frontend** - Templates, UI

**For each file:**

- Read time estimate
- "What it does" (one sentence)
- "Key concepts" to understand
- "Look for" (specific things to notice)
- "You can skip" (what to ignore for now)
- "Try it" (optional hands-on test)

**Ordering principle:** Build mental model progressively, don't jump around

### 4. Testing Guide 

**Include (for automated tests):**

- How to run automated tests
- What each test validates
- Expected coverage
- How to add new tests following existing patterns

**Keep brief** - user can read test files for details

Also include instructions for manual testing of main features

### 5. Known Issues / Limitations

**Be honest about:**

- Features not yet implemented (from original spec)
- Technical limitations
- Edge cases not handled
- Performance considerations
- Browser compatibility

**Format:** Checklists and bullet points, not paragraphs

### 6. Next Steps

**Suggest improvements ordered by:**

1. Easiest additions (1-2 hours)
2. Medium additions (3-5 hours)
3. Larger features (8+ hours)

**For each suggestion:**

- Complexity level (Low/Medium/High)
- Impact on user experience
- Files to add/modify
- Brief implementation approach

## What to Skip

**Don't include:**

- Trivial comments explaining obvious code
- Line-by-line code walkthroughs
- Detailed algorithm explanations for standard patterns
- Setup instructions Agent already covered in phase testing docs

**Focus on:**

- Why decisions were made
- How pieces connect
- Where to look to understand specific features
- What to test to verify it works

## Integration with iterative-build

**Greenfield projects:**

- Generate as `review_guide.md` after Phase 5 complete

**Feature additions:**

- Generate as `feature_[name]_review_guide.md`
- Focus review on the new feature and its integration points

## Critical Reminders

- User has ADHD - structure reduces cognitive load
- Checkboxes provide sense of progress
- Time estimates help planning
- Testing-first approach (do before reading code)
- Code reading order is logical, not alphabetical
- Break into resumable sections

**Focus:** Help user understand and test without feeling overwhelmed