# Scenarios: performance-regression-testing

All scenarios: Status: written, not executed. (The pytest-benchmark save/compare flags were run locally by the author; the agent-behavior scenarios were not.)

## 1. Positive activation

Status: written, not executed.

Prompt: "Last week a PR made our CSV import 30% slower and nobody noticed for days. How do we catch that in CI?"

Expected: skill activates; plans benchmark design, baseline comparison in the same job, noise-aware threshold, artifacts, flag policy.

## 2. Negative activation

Status: written, not executed.

Prompt: "Why is `render_page` slow? Find the hot function." (performance-profiling) and "Can the API handle 5,000 requests per second?" (load testing, out of scope). Skill should not activate.

## 3. Execution evaluation

Status: written, not executed.

Task: Add a regression gate for `parse(data)` in a Python project using pytest-benchmark.

Pass rubric:
- Seeded, in-memory input; at least two input sizes
- Baseline saved on main with `--benchmark-save`/autosave; PR compared via `--benchmark-compare` with `--benchmark-compare-fail` using a justified statistic and percent
- Threshold justified by measuring unchanged-code variation (or stated as provisional with a plan to measure)
- Notes shared-runner noise and proposes same-job A/B or deterministic proxy
- Does not hardcode absolute milliseconds as limits; no network/production data

Fail: single timed run with `time.time()`; threshold of 1% on shared runners; baseline taken on a different machine class without comment.

## 4. Edge: flaky gate

Status: written, not executed.

Task: gate fails intermittently. Pass: agent measures main-vs-main variation, raises threshold or switches statistic with evidence, not arbitrary disabling.
