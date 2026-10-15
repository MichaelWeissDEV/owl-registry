---
name: web-accessibility-review
description: >
  Review web UI code and running pages for accessibility against WCAG 2.2 (A/AA) and
  the WAI-ARIA Authoring Practices: semantics, names, keyboard operation, focus,
  contrast, target size, forms, dynamic content, and motion. Use when reviewing a
  component or page for a11y, fixing an axe/Lighthouse finding, building custom widgets
  (dialog, tabs, menu, combobox), or preparing conformance evidence. Combines automated
  scans with manual keyboard and screen-reader checks. Do not use for visual styling
  critique (frontend-design-review), writing HTML/CSS basics (web-html-css), or legal
  compliance opinions.
compatibility: >
  Any web frontend (plain HTML, React, Vue, etc.); Chromium DevTools plus optionally
  axe-core/axe DevTools, Lighthouse, and a screen reader (VoiceOver, NVDA, or Narrator).
metadata:
  author: michaelweissdev
  version: "1.0.0"
  tags: "accessibility, a11y, wcag, aria, keyboard, screen-reader, axe, contrast"
  topics: "frontend, accessibility, quality"
---

# Web Accessibility Review

Automated tools find only a subset of accessibility problems (commonly cited as roughly a third to half). A review needs code inspection, keyboard testing, and at least a spot check with assistive technology. Report findings with the WCAG success criterion, the user impact, and a concrete fix.

Related skills: `web-html-css` (semantic markup basics), `frontend-design-review` (visual hierarchy, responsive), `react-composition-patterns` (building accessible compound widgets), `playwright-testing` (regression tests for a11y checks), `browser-debugging` (DevTools mechanics).

## When to use / not use

Use for reviews of pages, components, forms, and custom widgets; triaging scanner output; writing acceptance criteria. Do not use to certify legal compliance (VPAT/ACR and legal claims need qualified auditors), and do not claim "fully accessible" from an automated scan.

## Non-negotiable rules

1. **Native HTML first.** Use `<button>`, `<a href>`, `<input>`, `<dialog>`, headings, landmarks, lists, and tables before ARIA. First rule of ARIA: if a native element does the job, use it. No ARIA is better than bad ARIA.
2. **Every interactive control has an accessible name, role, and state** exposed programmatically (WCAG 4.1.2).
3. **Everything operable by keyboard**, in a logical order, with a visible focus indicator (2.1.1, 2.4.3, 2.4.7), and no keyboard traps (2.1.2).
4. **Evidence standard:** each finding cites the criterion, the element/selector, how it was observed (tool, keyboard, screen reader), and the fix. Distinguish "confirmed" from "needs manual check".
5. **Test only what you are authorized to test**; do not enter real personal data into forms while testing.

## Workflow

### 1. Scope
Decide the target conformance level (usually WCAG 2.2 AA), the pages/flows (e.g. sign-up, checkout), and supported browsers and assistive technology.

### 2. Automated pass (fast, incomplete)
Run axe (browser extension, or `@axe-core/playwright` in tests) and Lighthouse's accessibility audit. Record violations; treat a clean result as "no detectable failures", not as conformance. Review "incomplete/needs review" items by hand.

### 3. Manual keyboard pass
Unplug the mouse. Using Tab, Shift+Tab, Enter, Space, Escape, and arrow keys:
- Can every control be reached and operated? Is the order logical?
- Is focus always visible, and not hidden behind sticky headers or banners (2.4.11 Focus Not Obscured, new in 2.2)?
- Do dialogs move focus in, trap it while modal, close on Escape, and return focus to the trigger?
- Are there skip links or landmarks to bypass repeated blocks (2.4.1)?

### 4. Semantics and names pass
Inspect the Accessibility tree in DevTools (Elements > Accessibility). Check headings outline (one `h1`, no skipped meaningful levels), landmarks (`header`, `nav`, `main`, `footer`), lists/tables semantics, link text that makes sense out of context (2.4.4), image `alt` (empty `alt=""` only for decorative), form labels tied with `<label for>` or wrapping, and error messages associated with inputs (`aria-describedby`, `aria-invalid`) per 3.3.1 and 3.3.3.

### 5. Visual pass
- Text contrast at least 4.5:1 (3:1 for large text), UI component and graphical object contrast at least 3:1 (1.4.3, 1.4.11).
- Information not by color alone (1.4.1).
- Reflow at 320 CSS px width without two-dimensional scrolling (1.4.10); zoom to 200% without loss (1.4.4); text spacing overrides (1.4.12).
- Pointer targets at least 24 by 24 CSS px, or adequate spacing (2.5.8 Target Size (Minimum), new in 2.2).
- Respect `prefers-reduced-motion`; no content flashing more than three times a second (2.3.1); pausing for auto-moving content (2.2.2).

### 6. Dynamic content and widgets
- Status messages announced without moving focus: `role="status"` / `aria-live="polite"` regions that exist in the DOM before content is injected (4.1.3).
- Custom widgets follow the WAI-ARIA APG pattern: roles, required states (`aria-expanded`, `aria-selected`), and keyboard model (e.g. tabs use arrow keys with roving tabindex; menus use arrows and Escape). Prefer native `<dialog>` with `showModal()` or the `inert` attribute on the background rather than hand-rolled traps.
- Drag interactions have a non-dragging alternative (2.5.7, new in 2.2).

### 7. Screen reader spot check
Test the main flow with one screen reader/browser pair (for example VoiceOver + Safari, NVDA + Firefox or Chrome). Listen for: names read sensibly, state changes announced, reading order matches visual order, no unlabeled controls.

### 8. Authentication and forms (WCAG 2.2 additions)
- Accessible Authentication (Minimum) 3.3.8: do not require a cognitive function test (memorizing, transcribing) to log in unless an alternative exists; allow paste and password managers (`autocomplete` attributes).
- Redundant Entry 3.3.7: do not make users re-enter information already provided in the same process.
- Consistent Help 3.2.6: help mechanisms appear in the same relative place across pages.

### 9. Report
Group by severity (blocker: prevents task completion; major; minor), include criterion, location, evidence, fix, and retest steps. Note what was not tested.

## Worked example

Finding: an icon-only "delete" `<div onclick>` in a table row.

- Issues: not focusable (2.1.1), no role/name (4.1.2), icon contrast 2.1:1 against background (1.4.11), 16 by 16 px target (2.5.8).
- Fix:
```html
<button type="button" class="icon-btn" aria-label="Delete invoice 1042">
  <svg aria-hidden="true" focusable="false" width="20" height="20"><!-- icon --></svg>
</button>
```
```css
.icon-btn { min-inline-size: 24px; min-block-size: 24px; padding: 6px; }
.icon-btn:focus-visible { outline: 3px solid currentColor; outline-offset: 2px; }
```
- Verify: Tab reaches it, Enter/Space activate, the accessibility tree shows role button with the name, and axe no longer reports it. After deletion, move focus to a sensible element and announce the result in a status region.

## Anti-patterns

- `<div role="button">` without keyboard handlers, `tabindex`, and state (use `<button>`).
- `aria-label` that contradicts visible text (breaks voice control; 2.5.3 Label in Name).
- `outline: none` with no replacement focus style.
- `tabindex` greater than 0.
- `aria-hidden="true"` on focusable elements.
- Placeholder as the only label.
- Positive claims from an automated scan alone.
- Live regions inserted at the same moment as their text.
- Disabling zoom (`user-scalable=no`, `maximum-scale=1`).
- Treating 4.1.1 Parsing as a requirement: it was removed in WCAG 2.2.

## Verification checklist

- [ ] Target level and scope stated
- [ ] Automated scan run and incomplete items reviewed
- [ ] Full keyboard walkthrough including dialogs and menus
- [ ] Accessibility tree checked for names, roles, states
- [ ] Contrast, reflow, zoom, target size checked
- [ ] Dynamic updates announced appropriately
- [ ] One screen reader spot check performed or explicitly listed as not done
- [ ] Each finding has criterion, evidence, fix, and retest step

## References

- [WCAG 2.2 quick map of criteria used here](references/wcag-quick-map.md)
- [Scenarios for evaluating this skill](references/scenarios.md)
- [Sources and provenance](references/sources.md)
