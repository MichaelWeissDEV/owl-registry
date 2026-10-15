---
name: verification-before-completion
description: >
  Enforce an evidence standard before an AI agent claims work is done, fixed,
  passing, or ready. Use when about to say "done", "fixed", "tests pass", "should
  work", commit, open a PR, or hand work back; when summarizing what a subagent
  reported; or when a claim rests on memory or inference instead of a command run
  in this session. Defines claim-to-evidence mapping, fresh-run rules, and honest
  reporting of unverified items. Not a test-writing guide (see test-driven-development)
  or a review guide (see code-review).
compatibility: >
  Any Agent Skills-compatible coding agent with shell access. Examples use git and
  generic test runners; substitute the project's own commands.
metadata:
  author: michaelweissdev
  version: "1.0.0"
  tags: "verification, evidence, completion, quality-gates, ai-agents, honesty"
  topics: "ai-agents, software-development, devtools"
---

# Verification Before Completion

A completion claim is a factual statement about the world: "the build passes", "the bug is fixed", "all callers updated". Agents tend to make these claims from what they *intended* to do rather than from what they *observed*. This skill sets a simple rule: **no completion claim without evidence produced after the last change, in this session, for exactly the thing being claimed.**

Related skills: [test-driven-development](../test-driven-development/SKILL.md) (how to write the tests that become evidence), [code-review](../code-review/SKILL.md) (reviewing someone else's diff), [debugging-workflow](../debugging-workflow/SKILL.md) (finding the cause when verification fails). Depth: [claim-evidence map](references/claim-evidence-map.md), [scenarios](references/scenarios.md), [sources](references/sources.md).

## When to use

- Just before writing "done", "fixed", "working", "passing", "ready for review", or similar.
- Before committing, tagging, or opening a pull request.
- When relaying a result reported by a subagent, a CI log, or a teammate.
- After a long session where earlier test runs may be stale.

## When not to use

- Exploratory questions where no claim of completion is made.
- Designing the tests themselves (use test-driven-development).
- Judging code quality or design (use code-review).

## Non-negotiable rules

1. **Evidence beats confidence.** Words like "should", "probably", "looks right" are not evidence. Run the check.
2. **Fresh evidence only.** Any edit after a check invalidates that check for everything the edit could touch. Re-run after the final edit.
3. **Evidence must match the claim.** A passing unit test does not prove a UI flow works; a clean build does not prove tests pass; a linter pass does not prove behavior. See the [claim-evidence map](references/claim-evidence-map.md).
4. **Read the output, not just the exit code.** Zero tests collected, skipped suites, or a filtered run can exit 0 and prove nothing.
5. **Report failures and gaps plainly.** If a check was not run, could not be run, or failed, say so in the final message. Never round "not verified" up to "verified".
6. **Verification is read-only by default.** Do not delete data, change settings, push, deploy, or alter shared systems to obtain evidence unless the user explicitly authorized it. Never print or paste secrets from logs or env output into reports.
7. **Subagent and tool output is a claim, not evidence.** Inspect the diff or re-run the check yourself before repeating it as fact.

## Workflow

### 1. State the claim precisely

Write down what you are about to assert, in one sentence per claim. "Fixed the crash" is too vague. "`parse()` no longer raises on empty input" is checkable.

### 2. Pick the cheapest check that could falsify it

Ask: *what observation would prove me wrong?* Prefer a check that fails before your change and passes after it. For a bug fix, reproduce the original failure first (or confirm the regression test fails against the old code), then show it passing.

### 3. Run it fresh, at the right scope

- Run the narrowest relevant check first for speed, then the broader suite the change could affect.
- Run from the project's documented entry point (the same command CI uses) rather than an ad hoc variant.
- Record the exact command and the salient lines of output (counts, failures, versions).

### 4. Inspect the result critically

Decision points:

| Observation | Meaning | Next step |
| --- | --- | --- |
| Failures | Claim is false | Fix, then restart at step 3 |
| 0 tests run / all skipped | Check proves nothing | Fix selection, rerun |
| Pass, but you edited afterward | Stale | Rerun |
| Pass only locally, CI differs | Environment gap | Say so; do not claim CI-green |
| Flaky (passes on retry) | Unreliable evidence | Report flakiness; do not hide with retries |

### 5. Check what the claim implies beyond the test

For "done", also compare the original request to the diff: is every requirement addressed? Run `git status` and `git diff --stat` to confirm there are no stray files, debug output, or unintended edits.

### 6. Report with evidence and gaps

Use this shape in the final message:

```text
Claim: <what is now true>
Evidence: <command> -> <key result, e.g. "42 passed, 0 failed">
Not verified: <anything skipped, with reason>
```

## Worked example

Task: "Fix the off-by-one in pagination."

1. Claim: `page(items, n=2, size=10)` returns items 10-19.
2. Falsifier: a test asserting the first and last element of page 2. Run it on the old code: it fails (returns 9-18). That confirms the test detects the bug.
3. Apply the fix. Rerun the one test: passes.
4. Run the whole pagination test module and then the project suite: `118 passed`, but you notice `3 skipped`. Check why: they are skipped because an optional database is absent. Record this.
5. `git diff --stat` shows one source file and one test file, as intended.
6. Report: "Fixed. Regression test fails before and passes after. Full suite: 118 passed, 3 skipped (DB-backed tests; not run here, so DB pagination is unverified)."

Note what was *not* said: "all tests pass" would have been inaccurate.

## Anti-patterns

- **Stale green.** Citing a test run from before the last edit.
- **Proxy checks.** "It compiles, so it works." "Lint is clean, so behavior is correct."
- **Trusting the summary.** Repeating a subagent's "all fixed" without looking at the diff.
- **Vacuous pass.** A filter that matched nothing, or a test that asserts nothing.
- **Silencing the check.** Deleting, skipping, or loosening a failing test to get green. If a test is truly wrong, say so explicitly and explain the change.
- **Retry until green.** Rerunning a flaky test until it passes and reporting only the pass.
- **Hedge laundering.** Burying "I couldn't run X" mid-paragraph. Put gaps in their own line.
- **Verification theater.** Running many impressive-looking commands unrelated to the claim.

## Verification checklist

- [ ] Each claim is written as a falsifiable sentence.
- [ ] Each claim has a command or observation tied to it.
- [ ] Evidence was produced after the last edit.
- [ ] Output was read (counts, skips, warnings), not just the exit status.
- [ ] Bug fixes show fail-before and pass-after where feasible.
- [ ] `git status` / `git diff --stat` match the intended scope.
- [ ] Final message lists anything not verified and why.
- [ ] No secrets, tokens, or private paths were copied into the report.
