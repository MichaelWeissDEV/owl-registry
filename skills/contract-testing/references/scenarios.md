# Scenarios: contract-testing

All scenarios: Status: written, not executed.

## 1. Positive activation

Status: written, not executed.

Prompt: "Our mobile app keeps breaking when the backend team renames response fields. We can't run end-to-end tests for every deploy. What should we do?"

Expected: skill activates; recommends consumer-driven contracts (Pact), broker, provider verification in provider CI, `can-i-deploy` gating, and an expand-then-contract migration for renames.

## 2. Negative activation

Status: written, not executed.

Prompt: "Design the REST endpoints for a new billing service." (api-design) and "Test the checkout flow in the browser." (playwright-testing). Skill should not activate.

## 3. Execution evaluation

Status: written, not executed.

Task: Consumer `web-app` reads `id` and `total` from `GET /users/{id}/orders`. Produce a Pact consumer test and a deploy-gate plan.

Pass rubric:
- Interaction has a named provider state and request, response with type matchers (`like`/`eachLike`), only `id` and `total` asserted
- At least one non-happy-path interaction (e.g., 404) the consumer handles
- Version = commit SHA, branch published; main branch configured
- Provider verification with selectors (mainBranch, deployedOrReleased) and pending pacts
- `can-i-deploy` before deploy and `record-deployment` after
- No real data or secrets; broker token via CI secret
- Honest note on what was not executed

Fail: whole-response exact match; contract generated from provider; skipping record-deployment; targeting production with a fuzzer.

## 4. Edge: public API

Status: written, not executed.

Task: public API with unknown consumers. Pass: agent chooses OpenAPI diff + Schemathesis against a disposable instance and explains why Pact alone is insufficient.
