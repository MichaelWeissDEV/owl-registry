# WCAG 2.2 quick map

Criteria referenced by the skill. Level in parentheses. Always read the normative text at https://www.w3.org/TR/WCAG22/ before citing in a formal report.

| SC | Name | Level | Practical test |
|---|---|---|---|
| 1.1.1 | Non-text Content | A | Meaningful images have text alternatives; decorative use empty alt |
| 1.3.1 | Info and Relationships | A | Structure conveyed by markup (headings, lists, labels) |
| 1.4.1 | Use of Color | A | Not the only cue |
| 1.4.3 | Contrast (Minimum) | AA | 4.5:1 text, 3:1 large text |
| 1.4.4 | Resize Text | AA | 200% without loss |
| 1.4.10 | Reflow | AA | 320 CSS px wide, no 2D scroll |
| 1.4.11 | Non-text Contrast | AA | 3:1 for UI components and graphics |
| 1.4.12 | Text Spacing | AA | Overrides do not break content |
| 2.1.1 | Keyboard | A | All functionality by keyboard |
| 2.1.2 | No Keyboard Trap | A | Can always leave |
| 2.2.2 | Pause, Stop, Hide | A | Controls for moving content |
| 2.3.1 | Three Flashes or Below | A | No flashing over three per second |
| 2.4.1 | Bypass Blocks | A | Skip link or landmarks |
| 2.4.3 | Focus Order | A | Logical sequence |
| 2.4.4 | Link Purpose (In Context) | A | Link text meaningful |
| 2.4.7 | Focus Visible | AA | Visible indicator |
| 2.4.11 | Focus Not Obscured (Minimum) | AA, new in 2.2 | Focused item not entirely hidden by author content |
| 2.5.3 | Label in Name | A | Accessible name contains visible label |
| 2.5.7 | Dragging Movements | AA, new in 2.2 | Single-pointer alternative |
| 2.5.8 | Target Size (Minimum) | AA, new in 2.2 | 24 by 24 CSS px or spacing exception |
| 3.2.6 | Consistent Help | A, new in 2.2 | Help in same place |
| 3.3.1 / 3.3.3 | Error Identification / Suggestion | A / AA | Errors described in text with suggestion |
| 3.3.7 | Redundant Entry | A, new in 2.2 | Do not ask twice |
| 3.3.8 | Accessible Authentication (Minimum) | AA, new in 2.2 | No cognitive function test without alternative |
| 4.1.2 | Name, Role, Value | A | Exposed to AT |
| 4.1.3 | Status Messages | AA | Announced without focus change |

Removed in 2.2: 4.1.1 Parsing. New in 2.2 and AAA (not covered above): 2.4.12, 2.4.13, 3.3.9.

## Useful commands and checks

- DevTools: Elements > Accessibility pane for the computed name/role; Rendering tab to emulate `prefers-reduced-motion` and vision deficiencies.
- Playwright with `@axe-core/playwright`: `new AxeBuilder({ page }).withTags(['wcag2a','wcag2aa','wcag22aa']).analyze()` (verify tag names for your installed axe-core version).
