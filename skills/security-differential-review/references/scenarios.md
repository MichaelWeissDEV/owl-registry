# Scenarios: security-differential-review

All scenarios: Status: written, not executed.

## 1. Positive Activation

Prompt: "Security-review PR #214 before we merge; it touches the session middleware and the auth helpers."

Expected: skill activates; agent computes the merge-base diff, triages by risk, examines removed lines, searches callers of changed functions, and reports with a "Not reviewed" section.

Status: written, not executed

## 2. Negative Activation

Prompt: "Audit the whole repository for SQL injection." or "Draw a STRIDE model for our new payment service."

Expected: skill does not activate as primary; the first is `security-code-review`, the second `threat-modeling`.

Status: written, not executed

## 3. Execution Evaluation

Task: Given a small repository where a commit removes an ownership check from `get_document()` and a third, unchanged caller depends on it, perform the differential review.

Pass rubric (all required):
- Uses base...head diff and records both commit hashes.
- Identifies the removed check as the highest-risk change.
- Searches for callers beyond the diff and finds the unchanged caller.
- Finding includes location, diff evidence, broken invariant, impact, confidence, fix.
- Includes "Not reviewed" and does not run PR code with real credentials.

Fail: reviews only added lines, accepts the PR description at face value, or reports without evidence citations.

Status: written, not executed
