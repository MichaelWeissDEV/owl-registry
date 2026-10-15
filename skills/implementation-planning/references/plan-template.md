# Plan template

Copy and trim. Delete sections that add nothing for a small task.

```markdown
# Plan: <short title>

## Goal
<one sentence>

## Acceptance criteria
- [ ] <observable outcome>
- [ ] <observable outcome>

## Out of scope
- <explicit exclusion>

## Current state (confirmed)
- <file/behavior you opened and verified>

## Assumptions and open questions
- Blocking: <question> (asked / answer: ...)
- Assumed: <assumption> (cheap to change because ...)

## Steps
1. <imperative title>
   - Files: <paths>
   - Verify: <command or observation>
   - Rollback: <how to undo>
   - Needs approval: yes/no
2. ...

## Risks
- <risk> -> <mitigation or early spike>

## Status log
- <date/step>: <what happened, evidence, plan changes>
```

## Sizing guidance

- If a step description needs the word "and" to join two behaviors, split it.
- If you cannot name the verification, the step is not understood yet.
- If two steps touch disjoint files and do not depend on each other, mark them as parallelizable.

## Ordering heuristics

1. Spike or failing test for the riskiest unknown.
2. Behavior-preserving refactors that make the change easy.
3. The behavior change itself, test first.
4. Docs, changelog, cleanup.
5. Anything requiring approval or touching shared systems goes last and is explicitly confirmed.
