# Scenarios: property-based-testing

All scenarios: Status: written, not executed (as agent-behavior evaluations). The Hypothesis snippets in SKILL.md were run by the author locally; the scenarios themselves have not been run against an agent.

## 1. Positive activation

Status: written, not executed.

Prompt: "Our `parse_duration('1h30m')` keeps getting edge-case bugs reported. Can you make the tests find these ourselves instead of us adding one example per bug?"

Expected: skill activates; agent selects properties (round-trip with a formatter, no-crash with typed errors, oracle against a simple reference), builds a bounded generator, and does not just add more examples.

## 2. Negative activation

Status: written, not executed.

Prompt: "Add a unit test that `get_user(5)` returns 404 when the mock repository is empty."

Expected: skill does not activate (single example with mocking: `unit-testing`). Also should not activate for "find crashes in this C image decoder with coverage guidance" (fuzz-testing) or "are my tests any good" (mutation-testing).

## 3. Execution evaluation

Status: written, not executed.

Task: Given `encode`/`decode` run-length functions where digits in input are not escaped, write a Hypothesis test and fix the bug.

Pass rubric (all required):
- Round-trip property over `st.text()` (or a justified alphabet) written without re-implementing the codec
- Test run; failure observed; the shrunk counterexample is quoted and explained (digit collision)
- Fix changes the format or escapes digits; test passes afterwards
- Counterexample pinned with `@example` plus a plain unit test
- No `assume()` used to dodge the digit case; any restriction is documented
- CI settings discussed: deadline and `derandomize` or equivalent, regression pinning

Fail: weakens the property to digit-free input without saying so; deletes the test; claims it passed without running it.

## 4. Edge case: stateful

Status: written, not executed.

Task: test an LRU cache. Pass: uses a `RuleBasedStateMachine` with a dict/OrderedDict model, a capacity invariant, and a precondition-gated eviction rule; reports the minimal rule sequence if it fails.
