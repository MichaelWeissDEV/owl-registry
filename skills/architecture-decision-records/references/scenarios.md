# Scenarios: architecture-decision-records

All scenarios: Status: written, not executed.

## 1. Positive activation

Prompt: "We just agreed to switch from REST to gRPC between our internal services. Write this up so we remember why."

Expected: skill activates; agent finds the repo's ADR convention, drafts a Proposed ADR with context, alternatives, decision sentence, and consequences including downsides.

Status: written, not executed.

## 2. Negative activation

Prompt: "Draw the component diagram for our checkout system."

Expected: skill does not activate; diagram and system design skills apply.

Status: written, not executed.

## 3. Execution evaluation

Task: Repo has `docs/adr/0001-*.md` through `0004-*.md`. Draft an ADR for adopting PostgreSQL over MongoDB for the orders service, given a short list of stated requirements.

Pass rubric (all required):
- New file is numbered 0005 and follows the existing naming/template.
- Exactly one decision; at least two alternatives with honest downsides.
- Consequences include negatives and a revisit condition.
- Status is Proposed, not Accepted.
- No invented benchmarks; any numbers are labelled as assumptions or cited.

Fail if: renumbers existing files, marks Accepted unilaterally, or lists only benefits.

Status: written, not executed.

## 4. Execution evaluation: superseding

Task: ADR 0003 chose library X; team now chooses library Y.

Pass rubric: new ADR 0006 created referencing 0003; 0003 changed only in status and link; body of 0003 untouched. Fail if 0003's reasoning is rewritten or the file is deleted.

Status: written, not executed.
