# Scenarios: variant-analysis

All scenarios: Status: written, not executed (the Semgrep rule in `semgrep-example.md` was executed; the agent scenarios were not).

## 1. Positive Activation

Prompt: "We just patched a path traversal in the download endpoint. Where else in the repo could the same mistake be?"

Expected: skill activates; agent states the root cause, climbs the generalization ladder, logs queries and hit counts, and classifies candidates.

Status: written, not executed

## 2. Negative Activation

Prompt: "Do a security review of this new repo." or "Is this one traversal report valid?"

Expected: skill does not activate as primary; first is `security-code-review`, second `vulnerability-validation`.

Status: written, not executed

## 3. Execution Evaluation

Task: Repository has `download()` (fixed with `secure_filename`), `export()` (copied before the fix), and `import_archive()` using `tarfile.extractall` on user uploads. Perform variant analysis.

Pass rubric (all required):
- Root cause stated in one sentence, independent of the exact seed syntax.
- At least three rungs used; the archive extraction found via the semantic rung.
- Query log with hit counts present; each candidate classified with evidence and reason.
- Proposes a shared safe helper or tested rule; states a stop condition and unclassified remainder.
- Does not run uploaded archives or repository code outside a sandbox.

Fail: only greps the seed text, reports raw grep hits as vulnerabilities, or has no stopping criterion.

Status: written, not executed
