# Equivalent mutants and common operators

## Typical operators

| Operator family | Example change | Test that kills it |
|---|---|---|
| Relational boundary | `<` to `<=`, `>` to `>=` | value exactly at the boundary |
| Negate condition | `if c` to `if not c` | one case per branch with different observable output |
| Arithmetic | `+` to `-`, `*` to `/` | non-trivial operands (avoid 0, 1, 2x multiples that coincide) |
| Return value | return constant / `None` / empty | assert exact value, not truthiness |
| Statement removal | delete a call | assert the side effect or state change |
| Logical | `and` to `or` | cases with exactly one operand true |
| Constants | `0` to `1`, string to other | assertions that depend on the constant |

Weak assertion smells: `assert result`, `assert result is not None`, `len(x) > 0`, `no exception raised`, mocks verified only by "was called".

## Why equivalent mutants occur

1. Redundant guards (`if x < 0: x = 0` before `max(x, 0)`).
2. Loop bounds where the extra iteration is a no-op.
3. Performance hints and caches whose only observable effect is time.
4. Logging, metrics, comments in strings.
5. Unreachable by invariant (callers guarantee non-empty).
6. Commutative reordering.

## Handling them

- Prove by reasoning on the invariant; write one line of justification at the exclusion site (`# pragma: no mutate  -- reason`, `#[mutants::skip]`, Stryker comment/ignore or config, PIT exclusion by mutator/class).
- Prefer simplifying the code (remove the redundant guard) to excluding the mutant.
- Re-check exclusions when the invariant changes.

## Score arithmetic

Score = killed / (generated minus equivalent minus unviable/compile-error). Tools differ on whether timeouts count as killed and how no-coverage mutants are scored: read the tool's definition before comparing numbers across tools or versions.

## Cost control

- Per-test coverage selection (Stryker `coverageAnalysis: perTest`, PIT's built-in coverage targeting) runs only tests that execute the mutated line.
- Incremental/history modes (Stryker `incremental`, PIT `withHistory`) skip unchanged code.
- Shard across CI jobs (cargo-mutants `--shard`).
- Fail fast on a mutant at the first failing test.
