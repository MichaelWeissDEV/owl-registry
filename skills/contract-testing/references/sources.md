# Sources and provenance: contract-testing

Consulted 2026-10-15 (read-only):

- Pact, how Pact works, https://docs.pact.io/getting_started/how_pact_works : consumer/provider/pact/interaction/provider state model, verification semantics.
- Pact matching, https://docs.pact.io/getting_started/matching : strict on requests, loose on responses, `like`/`eachLike`/regex, avoid random data.
- Pact Broker CLI, https://docs.pact.io/pact_broker/client_cli/readme : `publish` (`--consumer-app-version`, `--branch`, `--auto-detect-version-properties`), `can-i-deploy` (`--pacticipant`, `--version`, `--to-environment`), `record-deployment`, `create-webhook` with `--contract-requiring-verification-published`.
- Pact can-i-deploy, https://docs.pact.io/pact_broker/can_i_deploy : exit code semantics.
- Pending pacts, https://docs.pact.io/pact_broker/advanced_topics/pending_pacts : semantics, `enablePending`, broker version note (2.60.0).
- Consumer version selectors, https://docs.pact.io/pact_broker/advanced_topics/consumer_version_selectors : `mainBranch`, `deployedOrReleased`, `matchingBranch`.
- Schemathesis, https://schemathesis.readthedocs.io/en/stable/ and /reference/cli/ : `st run`, `-u/--url`, `-c/--checks`, `-n/--max-examples`, `--phases`, exit codes 0/1/2/130.

Not verified: the Pact JS V3 snippet and Verifier option names (from author knowledge of `@pact-foundation/pact`; not executed); oasdiff CLI (its README URLs returned 404); the `PACT_BROKER_TOKEN` environment variable name; pact-python v3 API (README fetched had no API details).

Provenance: all text is original; no external skill repositories were consulted, so no license decision was needed.
