# Scenarios: semgrep-rule-authoring

All scenarios: Status: written, not executed (against an agent). The example rules in `examples.md` were executed with Semgrep 1.174.0; the scenarios below were not run as agent evaluations.

## 1. Positive Activation

Prompt: "We just fixed a bug where `yaml.load` was called on request bodies. Write a Semgrep rule so it never comes back, and test it."

Expected: skill activates; the agent asks for or writes a vulnerable and fixed snippet, creates a test file with `ruleid:` and `ok:` cases (for example `yaml.safe_load`), validates, runs `semgrep --test`, and reports results and blind spots.

Status: written, not executed

## 2. Negative Activation

Prompt: "Run the default Semgrep ruleset on this repo and summarize the findings." or "Is this SQL injection finding exploitable?"

Expected: skill does not activate as the primary guide. The first is stock-ruleset review (`security-code-review`); the second is `vulnerability-validation`.

Status: written, not executed

## 3. Execution Evaluation

Task: Given a Python file where `os.system(cmd)` receives `request.args["q"]` in one function and a constant in another, produce a taint rule and tests.

Pass rubric (all required):
- Rule has `id`, `message`, `severity`, `languages`, and `mode: taint` with sources and sinks.
- Test file has at least one `ruleid:` and at least two `ok:` cases, including a near-miss (sanitized or constant).
- `semgrep --validate` and `semgrep --test` were actually run and their result is quoted.
- The agent states at least one false-negative class (for example flows across files).
- No claim of verification if Semgrep was not run.

Fail: rule delivered without tests, tests claimed but not run, or regex used where a structural pattern works.

Status: written, not executed
