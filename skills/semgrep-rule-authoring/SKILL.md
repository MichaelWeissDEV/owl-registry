---
name: semgrep-rule-authoring
description: >
  Write, test, and tune custom Semgrep rules (YAML) that detect one specific bug
  pattern with low false-positive noise, using pattern operators, metavariable
  constraints, taint mode, and annotated test files run with semgrep --test.
  Use when turning a confirmed vulnerability or review finding into a reusable
  detector, hunting variants across a codebase, or fixing a noisy or silent rule.
  Not for running stock rulesets (use security-code-review) or for deciding
  whether a finding is real (use vulnerability-validation).
compatibility: >
  Agent Skills-compatible coding agents with shell access. Examples verified
  against Semgrep CLI 1.174.0 (Community Edition); re-check the rule syntax
  docs for newer versions.
metadata:
  author: michaelweissdev
  version: "1.0.0"
  tags: "semgrep, static-analysis, sast, custom-rules, taint-analysis, variant-analysis, testing"
  topics: "security, static-analysis"
---

# Semgrep Rule Authoring

A Semgrep rule is a hypothesis about code: "every match of this shape is the bug". A good rule encodes the root cause of one real defect, ships with tests proving it fires and stays quiet where it should, and states its blind spots. Defensive use only: run rules against code you are authorized to analyze.

Related skills: `variant-analysis` (decides what to generalize and where to search), `security-code-review` (manual review, stock rulesets), `vulnerability-validation` (is a match exploitable), `secure-coding` (the fix).

## When to use / not use

Use when a bug class recurs, a review finding should become a regression guard, or a stock rule misses your framework's wrappers. Do not write a rule for a one-off defect that `grep` or a code edit resolves, and do not expect Semgrep to see properties it cannot (cross-service authorization logic, runtime configuration).

## Non-negotiable rules

1. Start from a concrete vulnerable snippet and its fixed version. No example, no rule.
2. Write the test file first, with `ruleid:` (must match) and `ok:` (must not match) cases. A rule without negative cases is untested.
3. Never claim a rule works until `semgrep --test` passed on your machine. Otherwise say "unverified".
4. Use the weakest mechanism that works: `pattern`, then `patterns`, then taint mode.
5. Run on real code and read the findings. Count true and false positives and report them.
6. Never put secrets or real customer data in messages or tests.

## Rule skeleton (current syntax)

Required keys under `rules:` are `id`, `message`, `severity`, `languages`, plus one of `pattern`, `patterns`, `pattern-either`, `pattern-regex` (or `mode: taint` with sources and sinks). Severity values are `LOW`, `MEDIUM`, `HIGH`, `CRITICAL`; legacy `INFO`, `WARNING`, `ERROR` still work and map to LOW, MEDIUM, HIGH. Put CWE and confidence in `metadata`; it does not affect matching.

```yaml
rules:
  - id: md5-sha1-on-password
    languages: [python]
    severity: MEDIUM
    message: >-
      $FUNC is a fast hash and must not protect passwords. Use a password KDF.
    metadata:
      cwe: "CWE-916: Use of Password Hash With Insufficient Computational Effort"
    patterns:
      - pattern-either:
          - pattern: hashlib.$FUNC($PW, ...)
          - pattern: hashlib.$FUNC($PW.encode(...), ...)
      - metavariable-regex:
          metavariable: $FUNC
          regex: ^(md5|sha1|sha256)$
      - metavariable-regex:
          metavariable: $PW
          regex: (?i).*(passw|pwd|passwd).*
```

## Workflow

1. **Pin the root cause** in one sentence: "untrusted X reaches dangerous Y without Z". The sentence picks the mechanism.
2. **Choose the mechanism.**
   - Syntactic shape (banned call, dangerous flag): `pattern` plus `pattern-not`.
   - Shape plus context (inside a handler, not inside a `try`): `pattern-inside` / `pattern-not-inside`.
   - Value constraint (name looks like a password, number under a threshold): `metavariable-regex`, `metavariable-comparison`, `metavariable-pattern`.
   - Data flow with sanitizers: `mode: taint` with `pattern-sources`, `pattern-sinks`, optional `pattern-sanitizers` and `pattern-propagators`.
3. **Write tests first**, in a file with the same base name and a matching extension (`rule.yaml` + `rule.py`). Put the annotation comment on the line directly above the code: `# ruleid: <id>` or `# ok: <id>`. `todoruleid:` / `todook:` mark known gaps without failing the run.
4. **Draft the rule**, run `semgrep --validate --config rule.yaml`, then `semgrep --test --metrics=off <dir>` until green.
5. **Run on the real tree**: `semgrep --config rule.yaml --metrics=off --json src/ > out.json`. Triage every hit as true positive, false positive, or unreachable. Add each false positive as an `ok:` test, then tighten.
6. **Hunt for misses.** Hand-write 3 to 5 variants (renamed import, alias, wrapper function, keyword vs positional argument, `await`ed form) and see which the rule misses. Fix them or record as `todoruleid:`.
7. **Document** blind spots in `metadata` or a comment. The message should say what to do, not only what is wrong.

## Taint-mode essentials

```yaml
mode: taint
pattern-sources:
  - pattern: flask.request.$ATTR
pattern-sinks:
  - patterns:
      - pattern: subprocess.$FUNC($CMD, ..., shell=True, ...)
      - focus-metavariable: $CMD
pattern-sanitizers:
  - pattern: shlex.quote(...)
```

- Taint flows through assignments and call arguments within a function by default. A sanitizer stops flow only for the matched expression.
- Use `focus-metavariable` in the sink so the finding points at the tainted argument rather than the whole call.
- Community Edition analysis does not follow flows across files or into callees defined elsewhere (cross-file analysis needs the paid engine and `interfile`). State this limit, and compensate by listing your wrapper functions as sources or sinks.
- `pattern-propagators` (with `from` and `to` metavariables) teach Semgrep about containers or custom copy functions such as `$LIST.append($X)`.
- Sanitizers are the main source of false negatives. A "sanitizer" that does not neutralize for that sink (HTML escaping before SQL) hides real bugs. Match them narrowly.

## Worked example

Goal: catch `subprocess` calls with `shell=True` fed by Flask request data (CWE-78). The full rule and test are in [references/examples.md](references/examples.md); run with Semgrep 1.174.0, all annotated lines passed (flagged: string concatenation and direct request attribute; not flagged: `shlex.quote`, list argv with `shell=False`, constant command). Design choices worth noticing: the sink is limited to `shell=True` because list-argv calls are not shell-injectable; `shlex.quote` is a sanitizer valid for POSIX shells specifically; the finding is focused on the command argument.

## Anti-patterns

- Name-only matching (`$X.execute(...)`) with no argument constraints; floods results.
- `pattern-regex` where a structural pattern would survive formatting changes.
- Calling a rule "high confidence" without counting hits on a real repository.
- `ok:` cases that are trivially different from the `ruleid:` cases. Make them the hard near-misses.
- Sanitizer lists copied from other rules without checking they fit this sink.
- `fix:` that changes semantics. If you add `fix:`, add a `.fixed` test file and review the diff by hand.
- Treating `severity: HIGH` as validated impact; it is a triage hint only.

## Verification checklist

- [ ] Vulnerable and fixed snippets exist in the test file
- [ ] `semgrep --validate` reports no configuration errors
- [ ] `semgrep --test` passes with `ruleid:` and near-miss `ok:` cases
- [ ] Run on real code; true/false positive counts recorded
- [ ] Known false negatives listed (`todoruleid:` or comments)
- [ ] Message states the fix; metadata carries CWE
- [ ] Semgrep version recorded

## References

- [references/examples.md](references/examples.md): tested rules, tests, and debugging steps
- [references/scenarios.md](references/scenarios.md): activation and evaluation scenarios
- [references/sources.md](references/sources.md): sources and provenance
