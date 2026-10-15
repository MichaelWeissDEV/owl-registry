# Scenarios for web-accessibility-review

## 1. Positive Activation
Status: written, not executed

Prompt: "Review this custom dropdown component for accessibility; axe says 'ARIA attribute not allowed'."
Expected: skill activates; agent prefers native elements or the APG pattern, checks names/roles/states, keyboard model, focus handling, and reports findings with WCAG criteria.
Pass: findings cite criteria and evidence; fix prefers native HTML.

## 2. Negative Activation
Status: written, not executed

Prompts: "Make the landing page look more modern" and "Explain flexbox gap."
Expected: skill does not activate (frontend-design-review and web-html-css respectively).
Pass: no a11y review workflow invoked.

## 3. Execution Evaluation
Status: written, not executed

Task: Review `<div class="btn" onclick="del()"><img src="trash.png"></div>` in a 16 by 16 px area with 2:1 contrast.
Rubric (all required):
- Identifies missing keyboard access, role/name, alt/label, contrast, and target size with the correct criteria (2.1.1, 4.1.2, 1.1.1, 1.4.11, 2.5.8).
- Proposes a `<button type="button">` with an accessible name and visible `:focus-visible` style.
- Includes a verification step with keyboard and the accessibility tree, not only a scanner.
- Does not claim full conformance.
Fail: only adds `role="button"` and `aria-label` to the div, or cites 4.1.1 Parsing as current.
