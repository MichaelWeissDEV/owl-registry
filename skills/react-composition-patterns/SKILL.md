---
name: react-composition-patterns
description: >
  Design React component APIs through composition: children and slots, compound
  components with context, controlled vs uncontrolled state, render props and custom
  hooks, and React 19 conventions (ref as a prop, Context as provider, use() for context).
  Use when a component has grown a long boolean-prop list, a design-system component
  needs a flexible API, state is prop-drilled, or a refactor of component structure is
  requested. Do not use for rendering speed (react-performance), accessibility semantics
  (web-accessibility-review), typing generics in depth (typescript-development), or
  non-React frameworks.
compatibility: >
  React 18/19 with TypeScript/TSX. React 19-specific advice is marked; older versions
  still need forwardRef and Context.Provider.
metadata:
  author: michaelweissdev
  version: "1.0.0"
  tags: "react, composition, compound-components, context, hooks, api-design, typescript, react-19"
  topics: "frontend, react, software-design"
---

# React Composition Patterns

Prefer composing small components over configuring one large component with many props. A good component API makes the common case short, the flexible case possible, and illegal states hard to express.

Related skills: `react-performance` (composition often fixes re-renders), `web-accessibility-review` (compound widgets must carry correct semantics), `typescript-development`, `refactoring`, `api-design` (same principles, different surface).

## When to use / not use

Use when: a component has more than about five props that toggle structure (`showHeader`, `hasFooter`, `iconLeft`, ...), variants multiply, consumers keep forking the component, state is threaded through several layers, or you are building a reusable library component.

Do not use for: one-off page components used in a single place, performance tuning, or visual design decisions.

## Non-negotiable rules

1. **Compose first, configure second.** If a prop only decides which child to render, accept the child instead.
2. **One source of truth for state.** A value is either controlled by the parent or owned internally, never silently both.
3. **Keep context narrow.** A context carries the minimum shared state of one component family; it is not a global store.
4. **Accessibility travels with the pattern.** A compound component (tabs, menu, dialog) must wire roles, ids, and keyboard behavior internally. See `web-accessibility-review`.
5. **Do not break the Rules of React**: hooks at top level, pure render, no mutation of props. The React Compiler and StrictMode depend on this.

## Pattern chooser

| Situation | Pattern |
|---|---|
| Layout wrapper with arbitrary content | `children` |
| A few distinct regions (header, actions) | Slot props (`header={...}`) or compound parts |
| Related parts that share state (Tabs, Accordion, Select) | Compound components + context |
| Reusable stateful logic, no UI | Custom hook |
| Caller must control what renders per item with internal data | Render prop (function child), sparingly |
| Many boolean variants | Variant prop (`variant="danger"`) or separate components |
| Component must work both with and without parent state | Controlled/uncontrolled pair |

## Workflow

1. **List the real use cases** (three or more actual call sites or stories). Design for them, not for hypotheticals.
2. **Find the axes of variation.** Structure (what is rendered) belongs to composition; appearance belongs to a small set of variant props.
3. **Choose the pattern** from the table; start with `children`.
4. **Write the consumer code first.** If the call site reads awkwardly, change the API before implementing.
5. **Type it** so illegal combinations fail to compile (discriminated unions for mutually exclusive props).
6. **Implement, then test via the public API** (`unit-testing`), including controlled and uncontrolled use.

## Patterns with code

### Children and slots

```tsx
type CardProps = { header?: React.ReactNode; children: React.ReactNode };
function Card({ header, children }: CardProps) {
  return (
    <section className="card">
      {header ? <header>{header}</header> : null}
      {children}
    </section>
  );
}
```

### Compound components with context

```tsx
import { createContext, use, useId, useState } from "react";

type Ctx = { open: boolean; toggle: () => void; panelId: string };
const DisclosureContext = createContext<Ctx | null>(null);

function useDisclosure(): Ctx {
  const ctx = use(DisclosureContext); // React 19: use() can read context; useContext works in all versions
  if (!ctx) throw new Error("Disclosure parts must be used inside <Disclosure>");
  return ctx;
}

function Disclosure({ children }: { children: React.ReactNode }) {
  const [open, setOpen] = useState(false);
  const panelId = useId();
  return (
    <DisclosureContext value={{ open, toggle: () => setOpen((o) => !o), panelId }}>
      {children}
    </DisclosureContext>
  );
}

function DisclosureButton({ children }: { children: React.ReactNode }) {
  const { open, toggle, panelId } = useDisclosure();
  return (
    <button type="button" aria-expanded={open} aria-controls={panelId} onClick={toggle}>
      {children}
    </button>
  );
}

function DisclosurePanel({ children }: { children: React.ReactNode }) {
  const { open, panelId } = useDisclosure();
  return <div id={panelId} hidden={!open}>{children}</div>;
}

Disclosure.Button = DisclosureButton;
Disclosure.Panel = DisclosurePanel;
```

`<Context value={...}>` as a provider is React 19; use `<Context.Provider>` on React 18. The context value above is a new object each render; for large subtrees, hoist state and memoize the value or rely on React Compiler (see `react-performance`).

### Controlled and uncontrolled

Accept `value` + `onChange` (controlled) or `defaultValue` (uncontrolled). Decide the mode once at mount; warn in development if it flips.

```tsx
// needs: import { useRef, useState } from "react"
function useControllable<T>(value: T | undefined, defaultValue: T, onChange?: (v: T) => void) {
  const [inner, setInner] = useState(defaultValue);
  const controlled = value !== undefined;
  const wasControlled = useRef(controlled);
  if (process.env.NODE_ENV !== "production" && wasControlled.current !== controlled) {
    console.warn("Component switched between controlled and uncontrolled; decide once at mount.");
    wasControlled.current = controlled; // warn once per flip
  }
  const current = controlled ? value : inner;
  const set = (next: T) => {
    if (!controlled) setInner(next);
    onChange?.(next);
  };
  return [current, set] as const;
}
```

### ref as a prop (React 19)

Function components receive `ref` as an ordinary prop; `forwardRef` is needed only for React 18 and earlier.

```tsx
function TextInput({ ref, ...rest }: React.ComponentPropsWithRef<"input">) {
  return <input ref={ref} {...rest} />;
}
```

Ref callbacks may return a cleanup function in React 19; use block bodies (`ref={(el) => { node = el; }}`) so TypeScript does not read the assignment as a return value.

### Custom hooks over render props

Share logic with a hook (`useDisclosure`, `useDebouncedValue`) and keep markup in the component. Use render props only when the caller must supply markup that depends on internal state per item.

### Polymorphism without prop explosion

Prefer an `as`-free design: export distinct components (`Button`, `LinkButton`) sharing styles. If polymorphism is required, constrain it with TypeScript generics and test that props and `ref` types are correct.

## Worked example

Before: `<Modal title icon showClose footerButtons primaryLabel secondaryLabel onPrimary onSecondary danger />` with 14 props and three forks in the codebase.

After:
```tsx
<Dialog open={open} onOpenChange={setOpen}>
  <Dialog.Title>Delete project</Dialog.Title>
  <Dialog.Body>This cannot be undone.</Dialog.Body>
  <Dialog.Actions>
    <Button variant="secondary" onClick={() => setOpen(false)}>Cancel</Button>
    <Button variant="danger" onClick={confirm}>Delete</Button>
  </Dialog.Actions>
</Dialog>
```
`Dialog` owns focus management, `aria-labelledby` wiring (title id via `useId`), Escape handling, and controlled/uncontrolled open state. Footer variants no longer need new props. Migrate call sites one at a time, keeping the old component until the last is moved.

## Anti-patterns

- Boolean prop soup (`isLarge isPrimary isGhost`): use `variant`/`size` unions.
- Cloning children (`React.cloneElement`) to inject props: fragile; use context.
- A single global context for unrelated state.
- Deriving state from props in an effect; derive during render or lift state.
- Prop drilling through four levels when composition (passing the element) would remove the layers.
- Premature abstraction from one use case.
- Context hooks that silently return `undefined` outside the provider (throw a clear error instead).

## Verification checklist

- [ ] Call sites read clearly; the common case is short
- [ ] No prop only toggles which child renders
- [ ] Controlled/uncontrolled behavior documented and tested
- [ ] Context scope is minimal and throws outside its provider
- [ ] Types reject illegal prop combinations
- [ ] Accessibility roles/ids/keyboard handled inside the component family
- [ ] Works under StrictMode; tests use the public API

## References

- [Pattern details and trade-offs](references/patterns.md)
- [Scenarios for evaluating this skill](references/scenarios.md)
- [Sources and provenance](references/sources.md)
