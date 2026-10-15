# Scenarios: mutation-testing

All scenarios: Status: written, not executed.

## 1. Positive activation

Status: written, not executed.

Prompt: "Our pricing module has 98% line coverage but a refund bug slipped through. How can we tell whether the tests are actually any good?"

Expected: skill activates; agent proposes mutation testing scoped to the pricing module, explains killed/survived, plans to review survivors.

## 2. Negative activation

Status: written, not executed.

Prompts (skill should not activate for any):
- "Our refactor is done and all 300 tests pass, CI is green. Can I tell the team it is finished?" Near-miss: mentions test results, but the task is a completion claim (verification-before-completion), not measuring test strength.
- "Find crashes in our parser with random bytes." (fuzz-testing)
- "Write tests for this new `slugify` function." (unit-testing / TDD)

## 3. Execution evaluation

Status: written, not executed.

Task: Rust crate with `fn in_range(x: i32, lo: i32, hi: i32) -> bool { x >= lo && x < hi }` and one test `in_range(5, 0, 10)`. Run cargo-mutants (or reason through mutants if the tool is unavailable and say so) and fix survivors.

Pass rubric:
- Baseline test run first and passing
- Survivors identified for boundaries (`>=`, `<`, `&&`)
- Added tests at `x == lo`, `x == hi`, `lo - 1`, `hi - 1`
- Each new test shown to fail on a mutant and pass on the original (or honestly stated as reasoned, not run)
- Report lists counts and dispositions; no pragma-based score inflation
- States mutants stay out of committed code

Fail: tests that only increase line coverage; excluding survivors without justification; claiming to have run the tool when not installed.

## 4. Edge: equivalent mutant

Status: written, not executed.

Task: survivor on `for i in 0..=n` changed to `0..n` where the last iteration appends to a discarded buffer. Pass: agent argues equivalence (or removes the redundant iteration) rather than writing a contrived test.
