# Pact CI recipe (sketch)

Names of environment variables and secrets are placeholders; store tokens in your CI secret store, never in the repo.

## Consumer pipeline

1. Run consumer tests (they write the pact files to the pact directory).
2. Publish:

```sh
pact-broker publish ./pacts \
  --broker-base-url "$PACT_BROKER_BASE_URL" \
  --consumer-app-version "$GIT_SHA" \
  --branch "$GIT_BRANCH"
```

3. Gate: `pact-broker can-i-deploy --pacticipant web-app --version "$GIT_SHA" --to-environment production`
4. After the real deploy: `pact-broker record-deployment --pacticipant web-app --version "$GIT_SHA" --environment production`

Broker credentials: the CLI reads a token via `--broker-token` or the corresponding `PACT_BROKER_TOKEN` environment variable (verify for your CLI version).

## Provider pipeline

1. Start the provider locally with downstream services stubbed and a throwaway database.
2. Run the verification test with: provider name, version = commit SHA, branch, selectors `mainBranch` + `deployedOrReleased` (+ `matchingBranch` for coordinated work), `enablePending: true`, publish results only when `CI` is set.
3. Gate: `can-i-deploy --pacticipant orders-api --version "$GIT_SHA" --to-environment production`; then `record-deployment`.
4. Webhook: create one on the broker for `contract_requiring_verification_published` that triggers the provider's verification job with the pact URL.

## Debugging a failed verification

- Read which interaction failed and the diff (missing field vs type vs status).
- Re-run only that interaction locally if your verifier supports filtering by description/state.
- If the provider state handler failed, fix the arrangement before blaming the provider code.
- If it only fails after a consumer change, check whether the consumer over-specified a matcher.

## GitHub Actions tie-in

Run provider verification as a normal job. For an N-way matrix over provider language versions or OS, see `cross-platform-testing`; keep verification itself on a single configuration to avoid duplicate result publishing.
