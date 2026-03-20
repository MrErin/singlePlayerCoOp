# Web Development Standards (HTML/CSS/JS)

Use alongside the core `my-style` skill.

## Accessibility First (Non-Negotiable)

- Semantic HTML always (not div soup)
- Labels for all inputs
- Keyboard navigation must work
- Focus indicators must be visible
- ARIA to enhance, not replace semantic elements
- Skip links for navigation

**AI-generated markup requires explicit accessibility review.** LLMs frequently produce `<div>` soup with click handlers instead of semantic elements, missing labels, and absent ARIA attributes. Always verify before accepting.

## Framework-Specific Traps
- React: onClick on divs instead of buttons, missing htmlFor on labels
- General: CSS-only dropdowns that trap keyboard focus, custom selects that aren't announced

## Testing Checklist

- [ ] All interactive elements reachable via Tab
- [ ] Tab order is logical
- [ ] Enter/Space work on buttons
- [ ] All images have alt text
- [ ] Form inputs have labels
- [ ] Error messages are announced to screen readers
- [ ] Focus indicators visible
- [ ] Color is not the only indicator
- [ ] Text contrast meets WCAG AA (4.5:1)

## Never Compromise On

- Keyboard navigation
- Screen reader support
- Focus indicators
- Semantic HTML

If accessibility conflicts with a design requirement, accessibility wins.