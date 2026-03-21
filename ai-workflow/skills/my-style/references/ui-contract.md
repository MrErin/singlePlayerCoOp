# UI Design Contract Template

Define UI decisions *before* coding. This contract forces specificity upfront, preventing "I'll figure it out during implementation" quality drift.

Create this file at `phases/[NN-name]/ui-contract.md` when a phase involves UI work.

---

## Spacing

**Allowed values:** 0, 1, 2, 4, 6, 8, 12, 16, 24, 32, 48, 64

**Grid:** 4px base unit, 8px preferred for most spacing

| Element | Value |
|---------|-------|
| Component internal padding | `p-2` to `p-4` |
| Between related items | `gap-2` to `gap-4` |
| Between sections | `gap-6` to `gap-8` |
| Page margins | `p-4` to `p-8` |

**Never use arbitrary values** like `p-[13px]` or `gap-[7px]`.

---

## Typography

**Maximum 4 font sizes.** Maximum 2 font weights.

| Role | Size | Weight | Example |
|------|------|--------|---------|
| Heading | `text-lg` or `text-xl` | `font-semibold` | Page titles |
| Subheading | `text-base` | `font-semibold` | Section headers |
| Body | `text-sm` or `text-base` | `font-normal` | Content |
| Caption | `text-xs` | `font-normal` | Hints, timestamps |

**Line height:** 1.5 for body text, 1.25 for headings.

---

## Color

**60/30/10 rule:**

| Percentage | Role | Usage |
|------------|------|-------|
| 60% | Neutral | Backgrounds, surfaces, borders |
| 30% | Secondary | Cards, muted text, secondary actions |
| 10% | Accent | CTAs, highlights, links, active states |

**Semantic tokens only.** Never hardcode colors like `bg-blue-600` or `text-gray-500`.

```css
/* ✅ Good - semantic tokens */
.bg-primary { background: var(--color-primary); }
.text-muted-foreground { color: var(--color-muted-foreground); }

/* ❌ Bad - hardcoded colors */
.bg-blue-600 { background: #2563eb; }
.text-gray-500 { color: #6b7280; }
```

**Accent color reserved-for list:**
- Primary CTAs
- Active navigation
- Links
- Error/destructive actions (use `destructive` token)
- Focus indicators

---

## Copywriting

**CTAs: verb + noun.** Never generic labels.

| ❌ Bad | ✅ Good |
|--------|---------|
| Submit | Save Changes, Create Account, Post Comment |
| OK | Confirm Delete, Accept Invitation |
| Cancel | Discard Changes, Go Back |
| Done | Finish Setup, Complete Order |

**Empty states:** Explain what's missing + how to fix it.

```markdown
❌ "No items found."
✅ "No projects yet. Create your first project to get started."
```

**Error messages:** Specific + actionable.

```markdown
❌ "An error occurred."
✅ "Could not connect to server. Check your network connection and try again."
```

---

## States

Every interactive element needs these states defined:

| State | Visual Cue |
|-------|------------|
| Default | Normal appearance |
| Hover | `hover:bg-accent` or `hover:opacity-80` — subtle shift |
| Focus | `ring-2 ring-primary ring-offset-2` — visible ring, never color-only |
| Disabled | `opacity-50 cursor-not-allowed` — reduced opacity, pointer blocked |
| Loading | `animate-spin` for action spinners; `animate-pulse` skeleton for content |
| Error | `border-destructive` ring + `<p className="text-destructive text-sm mt-1">` message |

**Loading states:** Use skeletons for content areas, spinners for actions.

---

## Accessibility (Non-Negotiable)

These requirements cannot be compromised for design preferences.

- **Keyboard navigation:** All interactive elements reachable via Tab
- **Focus indicators:** Visible on all focusable elements, not color-only
- **Screen reader support:** All images have alt text, icons have aria-labels
- **Color contrast:** WCAG AA minimum (4.5:1 for text)
- **Not color-only:** Never use color as the only indicator

**If accessibility conflicts with design, accessibility wins.**

---

## TUI-Specific Requirements

For terminal-based interfaces.

### Terminal Assumptions

| Setting | Value |
|---------|-------|
| Minimum width | 80 columns |
| Comfortable width | 120 columns |
| Color support | 16-color safe fallback required |
| Unicode | Assume limited support, ASCII preferred |

### Keyboard Navigation

- **Vim-style keys:** `j/k` for up/down, `h/l` for left/right (where applicable)
- **Arrow keys:** Must also work for users unfamiliar with vim
- `Enter` to select/confirm
- `Esc` to cancel/go back
- `q` to quit (where applicable)
- `?` for help

### `--plain` Mode (Non-Negotiable)

Every TUI must support a `--plain` flag that:

1. **Removes all colors** — no ANSI color codes
2. **Removes decorative boxes/borders** — use plain indentation and spacing
3. **Linear output** — screen readers parse sequentially
4. **Full keyboard support** — no mouse-only interactions
5. **Semantic structure** — headers as text, not visual formatting

```bash
# Rich mode (default)
my-app dashboard

# Plain mode (accessibility)
my-app dashboard --plain
```

**Plain mode is not optional.** It ensures accessibility for screen readers and terminals with limited capabilities.

### TUI/Web Concept Mapping

When building parallel interfaces (TUI + browser), keep concepts consistent:

| TUI | Web |
|-----|-----|
| Focus highlight | Focus ring |
| Key binding hint | Keyboard shortcut tooltip |
| Status line | Toast notification |
| `--plain` mode | High contrast / reduced motion mode |

---

## State Diagram

For interactive UIs with multiple states, include a simple state diagram:

```
[Empty] --"fetch"--> [Loading]
[Loading] --"success"--> [Populated]
[Loading] --"error"--> [Error]
[Error] --"retry"--> [Loading]
[Populated] --"clear"--> [Empty]
```

This surfaces all states upfront, preventing "I forgot the loading state" during implementation.

---

## Quality Gates

Before marking UI work complete:

- [ ] All spacing uses allowed values
- [ ] Typography uses max 4 sizes, max 2 weights
- [ ] All colors are semantic tokens
- [ ] All CTAs are verb+noun
- [ ] Empty states explain + guide
- [ ] Error messages are specific + actionable
- [ ] All interactive elements have hover/focus/disabled states
- [ ] Loading states use skeletons or spinners appropriately
- [ ] Keyboard navigation works for everything
- [ ] Focus indicators are visible
- [ ] Color is not the only indicator
- [ ] TUI: `--plain` mode implemented and tested
