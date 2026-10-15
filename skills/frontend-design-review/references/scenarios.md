# Scenarios for frontend-design-review

## 1. Positive Activation
Status: written, not executed

Prompt: "Here's the new pricing page (screenshot + repo). Give it a design review before we ship."
Expected: skill activates; agent reviews hierarchy, spacing, type, responsive and states, using multiple widths, and reports prioritized findings with concrete fixes.
Pass: findings have priority, user impact, and specific changes; unchecked areas are listed.

## 2. Negative Activation
Status: written, not executed

Prompts: "Is this page WCAG 2.2 AA conformant?" and "Why is my React list slow?"
Expected: skill does not lead (accessibility goes to web-accessibility-review; slowness to react-performance).
Pass: correct sibling skill is used.

## 3. Execution Evaluation
Status: written, not executed

Task: Review a card grid where three buttons are all filled blue, spacing uses 10/14/18 px, and the table overflows at 360 px.
Rubric (all required):
- Flags the mobile overflow as highest priority with a scroll-container or stacking fix.
- Identifies the unclear primary action and proposes primary/secondary/tertiary styles.
- Replaces ad hoc spacing with a scale or tokens.
- Lists what was not reviewed (dark mode, RTL, real devices).
Fail: gives only subjective remarks, proposes a full redesign, or claims accessibility compliance.
