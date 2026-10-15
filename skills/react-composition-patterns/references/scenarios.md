# Scenarios for react-composition-patterns

## 1. Positive Activation
Status: written, not executed

Prompt: "Our `<Modal>` has 14 props and teams keep forking it. Redesign the API."
Expected: skill activates; agent lists real use cases, proposes compound components or slots, writes consumer code first, handles controlled/uncontrolled open state.
Pass: result replaces structural props with composition and keeps accessibility wiring inside the component.

## 2. Negative Activation
Status: written, not executed

Prompts: "The product list re-renders too often, profile it." and "Write a Vue 3 component with slots."
Expected: skill does not activate (first goes to react-performance; second is a non-React framework).
Pass: no React composition workflow invoked.

## 3. Execution Evaluation
Status: written, not executed

Task: Convert `<Tabs tabs={[{label, content}]} />` into a compound API `Tabs`, `Tabs.List`, `Tabs.Tab`, `Tabs.Panel` with shared state.
Rubric (all required):
- Uses context with a hook that throws outside the provider.
- Supports controlled and uncontrolled selection and calls `onChange` in both.
- Wires `role`, `aria-selected`, `aria-controls`/`aria-labelledby` ids (via `useId`) and mentions arrow-key navigation per the WAI-ARIA APG tabs pattern.
- Uses `ref` as a prop only if targeting React 19 (otherwise `forwardRef`), and states the assumption.
Fail: uses `cloneElement` prop injection, global state, or omits keyboard/ARIA wiring.
