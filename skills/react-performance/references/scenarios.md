# Scenarios for react-performance

## 1. Positive Activation
Status: written, not executed

Prompt: "Our React dashboard lags when typing in the search field above a 3,000-row table. Find out why and fix it."
Expected: skill activates; the agent builds or asks for a repro, uses Profiler/Performance evidence, proposes state isolation, deferral or virtualization before memoization, and records before/after numbers.
Pass: measurement-first workflow followed; fixes ordered by cause; no blanket `useMemo`.

## 2. Negative Activation
Status: written, not executed

Prompts: "Why does my Express endpoint take 2 seconds to respond?" and "Center this div vertically."
Expected: skill does not activate (server latency goes to performance-profiling or nodejs-development; layout goes to web-html-css).
Pass: no React performance workflow is invoked.

## 3. Execution Evaluation
Status: written, not executed

Task: `Page` holds `query` state above an `<ExpensiveTree />` that does not use `query`; a PR also wraps ten unrelated callbacks in `useCallback`.
Rubric (all required):
- Proposes moving state down or passing `ExpensiveTree` as children instead of memoizing.
- Flags the unmeasured `useCallback` additions as unjustified or asks for Profiler evidence.
- States how to verify (Profiler recording before/after, production-like build).
- Mentions React Compiler as the alternative to hand memoization without asserting it is installed.
Fail: adds memoization everywhere, claims speedups without numbers, or suppresses hook lint rules.
