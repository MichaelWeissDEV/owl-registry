# Scenarios: implementation-planning

All scenarios: Status: written, not executed.

## 1. Positive activation

Prompt: "We need to move session storage from cookies to a server-side store across the web app. Plan it before we touch anything."

Expected: skill activates; agent surveys the code, lists blocking questions, produces ordered steps with verification and rollback, flags irreversible steps for approval.

Status: written, not executed.

## 2. Negative activation

Prompt: "Fix the typo 'recieve' in README.md."

Expected: skill does not activate; the agent makes the one-line edit directly.

Status: written, not executed.

## 3. Execution evaluation

Task: In a small repo with a CLI `report` command, plan (do not implement) adding a `--json` flag.

Pass rubric (all required):
- Opens at least the CLI entry point and existing tests before writing steps.
- States goal, acceptance criteria, and out-of-scope items.
- Every step lists files and a verification; at least the schema or format assumption is called out.
- A refactor-only step precedes the behavior change, or a reason is given for not separating.
- Names no file or function that does not exist in the repo.

Fail if: steps lack verification, plan references unconfirmed APIs, or scope includes unrequested changes.

Status: written, not executed.

## 4. Execution evaluation: ambiguous request

Task: "Make search faster." No other context.

Pass rubric: agent asks or lists blocking questions (what is slow, measured how, target) rather than inventing an optimization plan; proposes a measurement step first.

Status: written, not executed.
