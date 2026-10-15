# Pattern trade-offs

## Compound components vs slot props

- Slot props (`header`, `footer`) are simplest, typed per region, and need no context. Choose them when parts do not share state.
- Compound components allow free ordering and extra parts but need context and runtime checks that parts are inside the parent. Choose them when parts share state or ids.

## Context pitfalls

- Every consumer re-renders when the context value identity changes. Keep fast-changing values out of broad contexts; split state and dispatch into two contexts if consumers differ.
- Provide a typed hook per context that throws outside the provider.
- Do not use context to avoid passing one or two props one level down.

## Controlled vs uncontrolled

- Document which props pair (`value`/`onChange`, `defaultValue`).
- Do not switch modes during a component's life; React itself warns for native inputs.
- Always call `onChange` in both modes so parents can observe.

## State colocation order

1. Local state in the component that uses it.
2. Lift to the nearest common parent.
3. Composition (pass elements/children) to avoid threading props.
4. Context for a component family.
5. External store for app-wide state.

## Naming

- Parts: `Thing`, `Thing.Part` or `ThingPart` exports; hooks: `useThing`.
- Event props: `onXxx`; handler implementations: `handleXxx`.

## Testing composition

Test through the public API using Testing Library queries by role/name; verify keyboard behavior and the controlled/uncontrolled matrix. Snapshot tests of internals make refactors painful.
