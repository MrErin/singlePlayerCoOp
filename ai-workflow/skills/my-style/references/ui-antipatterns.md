# UI Anti-Patterns

Detectable patterns in UI code that indicate quality issues, accessibility gaps, or style drift.

Use these patterns during code-fixer passes and `/plan:review` to catch UI issues deterministically.

---

## Severity Classification

- **CRITICAL** — Accessibility violations, will exclude users
- **HIGH** — Quality issues that will cause maintenance pain or confusion
- **MEDIUM** — Style drift, should be cleaned but not blocking
- **LOW** — Minor inconsistency, fix opportunistically

---

## Generic CTA Labels (HIGH)

Buttons with vague labels that don't tell users what will happen.

| Pattern | Search | Severity | Action |
|---------|--------|----------|--------|
| Generic submit | `(?i)(submit|ok|cancel|done|go|continue)` in button context | HIGH | Replace with verb+noun |
| Standalone "Add" | `>Add<` or `Add` as only button text | MEDIUM | Add what? "Add Item", "Add User" |
| Contextless "Delete" | `>Delete<` without object | MEDIUM | "Delete Account", "Remove Item" |

### Grep Patterns

```bash
# Generic button text
grep -rnE '(?i)(submit|cancel|ok|done|go)\s*['"'"`](\s*>)?' --include="*.tsx" --include="*.jsx" --include="*.html"

# Button with generic label
grep -rnE '<button[^>]*>\s*(Submit|OK|Cancel|Done|Go|Continue)\s*</button>' --include="*.tsx" --include="*.jsx" --include="*.html"
```

### Examples

```tsx
// ❌ Generic - what happens?
<button onClick={handleSubmit}>Submit</button>
<button onClick={handleClose}>Cancel</button>

// ✅ Specific - clear action
<button onClick={handleSubmit}>Save Changes</button>
<button onClick={handleClose}>Discard Changes</button>
```

**Why it matters:** Generic labels create cognitive load. Users must read surrounding context to understand what the button does. Verb+noun makes the action explicit.

---

## Hardcoded Colors (HIGH)

Non-semantic color classes that break theming and dark mode.

| Pattern | Search | Severity | Action |
|---------|--------|----------|--------|
| Tailwind color classes | `bg-(blue|red|green|yellow|purple|pink|gray)-[0-9]+` | HIGH | Replace with semantic token |
| Text color classes | `text-(blue|red|green|yellow|purple|pink|gray)-[0-9]+` | HIGH | Replace with semantic token |
| Border color classes | `border-(blue|red|green|yellow|purple|pink|gray)-[0-9]+` | MEDIUM | Replace with semantic token |

### Grep Patterns

```bash
# Hardcoded background colors
grep -rnE 'bg-(blue|red|green|yellow|purple|pink|orange|indigo|cyan|teal)-[1-9][0-9]?0?' --include="*.tsx" --include="*.jsx" --include="*.css"

# Hardcoded text colors
grep -rnE 'text-(blue|red|green|yellow|purple|pink|gray)-[0-9]+' --include="*.tsx" --include="*.jsx"

# Inline hex colors in style
grep -rnE 'style="[^"]*#[0-9a-fA-F]{3,6}' --include="*.html" --include="*.tsx"
```

### Examples

```tsx
// ❌ Hardcoded - breaks theming
<button className="bg-blue-600 text-white">Submit</button>
<p className="text-gray-500">Secondary text</p>

// ✅ Semantic tokens - theming works
<button className="bg-primary text-primary-foreground">Submit</button>
<p className="text-muted-foreground">Secondary text</p>
```

**Why it matters:** Hardcoded colors prevent dark mode, high-contrast themes, and brand customization. Semantic tokens separate intent from implementation.

**Exceptions:** Prototype/demo code that will be replaced. Document these.

---

## Arbitrary Spacing Values (MEDIUM)

Tailwind arbitrary values that bypass the spacing scale.

| Pattern | Search | Severity | Action |
|---------|--------|----------|--------|
| Arbitrary padding | `(p|pt|pb|pl|pr|px|py)-\[([0-9]+)px\]` | MEDIUM | Use scale value |
| Arbitrary margin | `(m|mt|mb|ml|mr|mx|my)-\[([0-9]+)px\]` | MEDIUM | Use scale value |
| Arbitrary gap | `gap-\[([0-9]+)px\]` | MEDIUM | Use scale value |

### Grep Patterns

```bash
# Arbitrary spacing values
grep -rnE '(p|m|gap)(t|b|l|r|x|y)?-\[[0-9]+(px|rem|em)\]' --include="*.tsx" --include="*.jsx" --include="*.css"
```

### Examples

```tsx
// ❌ Arbitrary - inconsistent
<div className="p-[13px] gap-[7px]">

// ✅ Scale values - consistent
<div className="p-3 gap-2">
```

**Allowed values:** 0, 1, 2, 4, 6, 8, 12, 16, 24, 32, 48, 64 (4px base, 8px preferred)

**Why it matters:** Arbitrary values create visual inconsistency and make systematic adjustments impossible. "Change all spacing by 2px" only works with a scale.

---

## Missing Accessibility Attributes (CRITICAL)

Interactive elements without proper accessibility support.

| Pattern | Search | Severity | Action |
|---------|--------|----------|--------|
| Icon-only button without label | `<button[^>]*>\s*<[^>]*icon[^>]*>\s*</button>` without `aria-label` | CRITICAL | Add `aria-label` |
| Image without alt | `<img[^>]*(?!alt=)[^>]*>` | CRITICAL | Add `alt` attribute |
| Input without label | `<input[^>]*>` without `id` matching `<label>` or `aria-label` | CRITICAL | Add label association |
| Click handler on non-interactive | `onClick` on `<div>` or `<span>` without `role="button"` | HIGH | Use `<button>` or add role + keyboard handler |

### Grep Patterns

```bash
# Icon button without aria-label
grep -rnE '<button[^>]*>\s*<[A-Z][a-zA-Z]*Icon' --include="*.tsx" --include="*.jsx" | grep -v 'aria-label'

# Image without alt
grep -rnE '<img[^>]*>' --include="*.tsx" --include="*.jsx" --include="*.html" | grep -v 'alt='

# Clickable div without role
grep -rnE '<div[^>]*onClick' --include="*.tsx" --include="*.jsx" | grep -v 'role='

# Input without label association
grep -rnE '<input[^>]*>' --include="*.tsx" --include="*.jsx" | grep -v 'aria-label\|id='
```

### Examples

```tsx
// ❌ Screen reader can't announce purpose
<button onClick={handleDelete}>
  <TrashIcon />
</button>

// ✅ Accessible
<button onClick={handleDelete} aria-label="Delete item">
  <TrashIcon />
</button>
```

```tsx
// ❌ Clickable div - not keyboard accessible
<div onClick={handleClick}>Click me</div>

// ✅ Use button for interactive elements
<button onClick={handleClick}>Click me</button>

// ✅ If div is required, add accessibility
<div
  onClick={handleClick}
  role="button"
  tabIndex={0}
  onKeyDown={(e) => e.key === 'Enter' && handleClick()}
>
  Click me
</div>
```

**Why it matters:** Screen readers need semantic information to navigate. Icon-only buttons are invisible without labels. Non-interactive elements with click handlers can't receive keyboard focus.

---

## Missing State Styles (HIGH)

Interactive elements without hover/focus/disabled states.

| Pattern | Detection | Severity | Action |
|---------|-----------|----------|--------|
| Button without hover | `<button` with className but no `hover:` variant | HIGH | Add hover state |
| Button without focus | `<button` with className but no `focus:` variant | HIGH | Add focus state |
| Disabled without visual | `disabled` prop without `disabled:` styling | MEDIUM | Add disabled state |

### Grep Patterns

```bash
# Button without hover state
grep -rnE '<button[^>]*className="[^"]*"' --include="*.tsx" --include="*.jsx" | grep -v 'hover:'

# Button without focus state
grep -rnE '<button[^>]*className="[^"]*"' --include="*.tsx" --include="*.jsx" | grep -v 'focus:'
```

**Note:** Component libraries may handle states internally. Check the component's implementation before flagging.

---

## Color-Only Indicators (CRITICAL)

Using color as the only way to convey information.

| Pattern | Detection | Severity | Action |
|---------|-----------|----------|--------|
| Status color only | `bg-red-*`/`bg-green-*` on element with no visible text | CRITICAL | Add visible text label + icon; replace color class with `bg-success`/`bg-destructive` semantic token (see token table below) |
| Error highlight only | `border-red-*`/`border-destructive` on input with no adjacent error message | HIGH | Add `<p className="text-destructive text-sm mt-1">` error message below the field |
| Required field indicator | `*` asterisk marker with no accompanying text label | MEDIUM | Add visible `<span> (required)</span>` alongside the asterisk |

### Semantic Token Reference

When replacing hardcoded colors, use these semantic tokens — never substitute a different color class:

| Meaning | Background | Text | Border | Use for |
|---------|------------|------|--------|---------|
| Error / Danger | `bg-destructive` | `text-destructive-foreground` | `border-destructive` | Error states, delete actions |
| Success / Active | `bg-success` | `text-success-foreground` | `border-success` | Confirmed states, active status |
| Warning | `bg-warning` | `text-warning-foreground` | `border-warning` | Caution states, pending indicators |
| Muted / Inactive | `bg-muted` | `text-muted-foreground` | `border-muted` | Secondary content, inactive states |
| Primary action | `bg-primary` | `text-primary-foreground` | `border-primary` | CTAs, active navigation |

### Grep Patterns

```bash
# Background color classes used for status (likely color-only indicators)
grep -rnE 'bg-(green|red|amber|yellow|orange)-[0-9]+' --include="*.tsx" --include="*.jsx"
# Verify each match: if the element contains only an icon and no text, it is a color-only indicator

# Error border without adjacent error message
grep -rnE 'border-(red-[0-9]+|destructive)' --include="*.tsx" --include="*.jsx"
# Verify each match: look for a sibling/child with text-destructive, role="alert", or visible error text

# Required asterisk without text label
grep -rnE 'aria-required|required.*\*|\*.*required' --include="*.tsx" --include="*.jsx" --include="*.html"
```

### Examples

```tsx
// ❌ Color-only - colorblind users can't distinguish
<span className="bg-green-500">Active</span>
<span className="bg-red-500">Inactive</span>

// ✅ Color + text + icon
<span className="bg-success text-success-foreground">
  <CheckIcon aria-hidden /> Active
</span>
<span className="bg-destructive text-destructive-foreground">
  <XIcon aria-hidden /> Inactive
</span>
```

**Why it matters:** ~8% of men have color vision deficiency. Color-only indicators are invisible to these users.

---

## TUI Antipatterns (HIGH)

Terminal UI-specific issues.

| Pattern | Detection | Severity | Action |
|---------|-----------|----------|--------|
| Missing --plain flag | TUI app without `--plain` option | CRITICAL | Add plain mode |
| Mouse-only interaction | Click handlers without keyboard equivalent | CRITICAL | Add key binding |
| No quit command | Interactive TUI without `q` to quit | HIGH | Add quit key |
| Hardcoded colors | ANSI codes without fallback | HIGH | Check NO_COLOR env, provide --plain |
| Assuming true color | 24-bit color without 16-color fallback | MEDIUM | Detect terminal capabilities |

### Grep Patterns

```bash
# ANSI color codes without fallback check
grep -rnE '\\x1b\[' --include="*.py" --include="*.js" --include="*.ts" | grep -v 'NO_COLOR\--plain'

# Mouse handler without key equivalent
grep -rnE 'on_click|onClick' --include="*.py" | grep -v 'key\|bind'
```

### Examples

```python
# ❌ No fallback, no --plain option
def render():
    print("\033[31mError\033[0m")

# ✅ Respects environment, has fallback
def render(plain: bool = False):
    if plain or os.environ.get("NO_COLOR"):
        print("Error")
    else:
        print("\033[31mError\033[0m")
```

**Why it matters:** Terminals vary widely in capability. Screen readers can't parse ANSI formatting. `--plain` mode is required for accessibility.

---

## Empty State Gaps (MEDIUM)

Missing empty/loading/error states.

| Pattern | Detection | Severity | Action |
|---------|-----------|----------|--------|
| List render without empty | `.map()` without empty check | MEDIUM | Add empty state |
| Data fetch without loading | `useEffect` + state without loading state | HIGH | Add loading state |
| Async without error | `try/catch` around fetch without error state | HIGH | Add error state |

### Grep Patterns

```bash
# List rendering without empty state
grep -rnE '\.map\(.*=>' --include="*.tsx" --include="*.jsx" | grep -v 'length\|empty\|No '

# Fetch without loading state
grep -rnE 'fetch\(|useQuery\(' --include="*.tsx" --include="*.jsx" | grep -v 'loading\|isLoading'
```

### Examples

```tsx
// ❌ Crashes or shows nothing on empty list
{items.map(item => <ItemCard key={item.id} item={item} />)}

// ✅ Handles empty state
{items.length === 0 ? (
  <EmptyState message="No items yet. Add your first item to get started." />
) : (
  items.map(item => <ItemCard key={item.id} item={item} />)
)}
```

---

## How to Use This Reference

### For code-fixer agent

Run grep patterns against modified files. Focus on CRITICAL patterns first (accessibility), then HIGH (quality). Report matches but don't auto-fix — many require human judgment about correct labels/tokens.

### For /plan:review

Include a "UI Quality" section in the review output:
1. Run grep patterns against all frontend files modified in the phase
2. Count violations by severity
3. List top 5 most common violations
4. Flag any CRITICAL violations for immediate attention

### For /plan:build

Before implementing UI tasks, check if `ui-contract.md` exists for the phase. If not, prompt user to create one. The contract prevents antipatterns before they're written.

---

## Pattern Discovery Log

When you encounter a new UI anti-pattern in the wild, add it here:

```
## [Date] [Pattern Name]
**Found in:** [project/framework context]
**Pattern:** [description or code snippet]
**Search:** [grep pattern if detectable]
**Severity:** [CRITICAL/HIGH/MEDIUM/LOW]
**Why it matters:** [explanation]
**Action:** [what to do]
```
