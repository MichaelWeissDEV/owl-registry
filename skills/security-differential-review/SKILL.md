---
name: security-differential-review
description: >
  Review a code change (pull request, commit range, release diff) for security
  regressions by focusing on what the diff adds, removes, and silently changes,
  including deleted checks, weakened defaults, and callers outside the diff.
  Use when asked to security-review a PR or branch, audit what changed between
  two releases, or triage a large diff by risk. Not for whole-codebase audits
  (use security-code-review), threat models (use threat-modeling), or deciding
  exploitability of one finding (use vulnerability-validation).
compatibility: >
  Agent Skills-compatible coding agents with git and read access to the repository.
metadata:
  author: michaelweissdev
  version: "1.0.0"
  tags: "security, code-review, diff, pull-request, regression, git, risk-triage"
  topics: "security, code-review"
---

# Security Differential Review

A diff is a statement of intent plus side effects. The security question is not "is this code secure" but "does this change make the system less safe than before, or add attack surface that is not guarded?" The riskiest lines are often the ones that were deleted or that sit unchanged next to the diff.

Boundaries: `security-code-review` covers source-to-sink analysis of code as it stands; this skill is the change-oriented workflow on top of it. Use `threat-modeling` for design-level risk, `vulnerability-validation` to confirm a finding, `variant-analysis` to look for the same bug elsewhere, `software-supply-chain-audit` when the diff touches dependencies or build files, and `github-actions-security` for workflow changes.

## Non-negotiable rules

1. Read-only. Review with `git diff`, `git show`, `git log`; do not check out untrusted branches and run their code, scripts, or hooks outside a sandbox.
2. Treat the PR title, description, commit messages, and code comments as claims, not facts. "Only refactoring" is a hypothesis to test against the diff.
3. Every finding cites file, line, the diff hunk, and the invariant it breaks. No evidence, no finding.
4. State what you did not review (generated files, vendored code, files over your budget). Silence implies coverage.
5. Never paste secrets found in a diff into the report; cite the location and recommend rotation.

## Workflow

### 1. Establish the base and the scope
```bash
git merge-base origin/main HEAD          # real fork point
git diff --stat --find-renames origin/main...HEAD
git log --oneline origin/main..HEAD
```
The three-dot form compares against the merge base, which is what a PR actually introduces. Record the two commit hashes you reviewed.

### 2. Triage files by risk before reading any
Rank changed files; read high-risk first and say what you skipped.

| Risk | Typical files |
| --- | --- |
| Highest | authn/authz, session/token handling, crypto, input parsing, deserialization, file/path/URL handling, SQL/shell/template construction, permission or ACL tables |
| High | middleware order, CORS/CSP/cookie settings, CI workflows, Dockerfiles, IaC (network rules, IAM), dependency manifests and lockfiles, build scripts |
| Medium | business logic touching money, tenancy, or ownership; logging (PII leakage); error handling |
| Low | docs, tests (but see below), pure formatting |

### 3. Read removals first
Deleted lines are where silent regressions hide.
```bash
git diff origin/main...HEAD | grep -E '^-[^-]'   # lines removed
git diff --diff-filter=D --name-only origin/main...HEAD   # deleted files
```
For each removed check ask: was it a guard (auth check, validation, escaping, rate limit, lock, bounds check, `try/finally` cleanup)? If so, where is the equivalent now? A moved check must still run before the sink on every path.

### 4. Read additions against trust boundaries
For each added or modified function: what inputs does it take, which are attacker-controlled, which sinks does it reach, and what validates between them. Use the source-to-sink method from `security-code-review`.

### 5. Look beyond the hunks
- **Callers**: if a function's contract changed (nullable return, new default, relaxed validation), search every caller (`rg -n 'funcName\('`). The vulnerable code may be an unchanged caller that assumed the old contract.
- **Sibling code paths**: a new endpoint, handler, or CLI command should have the same guards as its siblings. Compare the new route list against existing ones.
- **Defaults and flags**: changed constants, config defaults, feature flags, env var names. A default flipped from deny to allow is a finding even if it is one line.
- **Tests**: deleted or weakened tests, `skip`/`xfail` additions, assertions loosened. Tests are evidence of intent.
- **History**: `git log -S'check_permission' -p -- path` finds when a guard was introduced or removed; `git blame -w -C -C path` shows who last touched a line and why.

### 6. Check the change as a whole
Do the pieces compose safely? Example: validation added in the API layer while a new background job writes the same field directly. Consider concurrency, ordering (check then use), and partial failure.

### 7. Report
Order by severity. For each finding give: title, location, what changed, broken invariant, concrete impact in terms of this system, confidence, and a minimal fix. Add a "Not reviewed" section and a "Verified safe" list of risky-looking changes you examined and cleared, with the reason. Hand uncertain findings to `vulnerability-validation`.

## Worked example

A PR titled "Simplify document access" changes:

```diff
-def get_document(user, doc_id):
-    doc = db.documents.get(doc_id)
-    if doc.owner_id != user.id and not user.is_admin:
-        raise Forbidden()
-    return doc
+def get_document(doc_id):
+    return db.documents.get(doc_id)
```
and updates two callers in the diff. Triage puts it in the highest tier. The removed lines were an ownership check (CWE-639/CWE-862 class). Step 5 greps for callers: `rg -n 'get_document\('` finds a third caller in `export_job.py`, unchanged, that previously relied on the exception. The finding: the authorization moved nowhere, and one unchanged caller is now reachable without any check. Evidence: the removed hunk, the caller's line, the route that reaches it. Impact is stated in terms of tenant data exposure, confidence is high because no other check was found in the call chain (state which files were traced). Fix: restore the check in the function or enforce it at a documented single choke point and test both.

## Anti-patterns

- Reviewing only the green lines of the diff.
- Trusting the description ("no behavior change") without checking.
- Flagging style or generic hardening advice as security findings; it buries the real ones.
- Reporting a vulnerable-looking line without checking whether the caller already sanitizes.
- Reviewing a squashed 5,000-line diff linearly; triage by risk, and ask for it to be split if you cannot cover it.
- Running the PR's code locally on your workstation with real credentials in the environment.

## Verification checklist

- [ ] Base and head commits recorded; three-dot diff used
- [ ] Files ranked by risk; skipped files listed
- [ ] All removed lines in high-risk files examined
- [ ] Callers and sibling paths of changed contracts searched
- [ ] Config/default/dependency/CI changes checked
- [ ] Each finding has location, evidence, broken invariant, impact, confidence
- [ ] "Not reviewed" and "Verified safe" sections present

## References

- [references/checklist.md](references/checklist.md): per-change-type checks
- [references/scenarios.md](references/scenarios.md): activation and evaluation scenarios
- [references/sources.md](references/sources.md): sources and provenance
