# Per-change-type security checks

Use after triage. Each row: what to look for in the diff, and the question that exposes it.

## Authentication and authorization
- Check removed, reordered, or made conditional? Is it still before the sink on every branch (including error and early-return paths)?
- New route, RPC, GraphQL field, or CLI command: does it carry the same decorator/middleware as siblings? Is object-level ownership checked, not just "logged in"?
- Role names or permission strings renamed: are all enforcement sites updated (a stale string often fails open)?
- Token or session lifetime, audience, issuer, or algorithm checks changed? (see `oauth-jwt-auth`)

## Input handling
- New parser, deserializer, or file/archive reader: size limits, depth limits, type allowlists, path containment.
- Validation moved to another layer: do all entry points (including jobs, webhooks, imports) still pass through it?
- Regex changes: anchors dropped, `.*` added, catastrophic backtracking on user input.

## Output and queries
- String concatenation or formatting near SQL, shell, templates, HTML, LDAP, headers: parameterized or escaped for that exact context?
- Raw-HTML escape hatches added to templates (`safe`, `dangerouslySetInnerHTML`, `|raw`).

## Secrets and logging
- New config keys, env vars, or test fixtures that look like credentials (report location only; recommend rotation; see `secrets-management`).
- New log lines that include request bodies, tokens, or personal data.

## Cryptography
- Algorithm, mode, key size, IV/nonce source, or comparison function changed; hand-rolled primitives. Escalate to `cryptographic-code-review`.

## Dependencies and build
- Manifest or lockfile changes: new packages, version range widening, registry or URL changes, install scripts, integrity hashes removed. Escalate to `software-supply-chain-audit`.
- CI workflow changes: new triggers (`pull_request_target`), permissions widened, third-party actions not pinned to a commit. See `github-actions-security`.
- Dockerfile/IaC: user switched to root, ports or security groups opened, TLS verification disabled. See `container-security`, `terraform-iac`.

## Concurrency and state
- Check-then-act on files, balances, or quotas without a lock or transaction (TOCTOU).
- Caches keyed without tenant or user identity.

## Tests
- Deleted tests, `skip`/`xfail`, loosened assertions, mocks that replace the auth layer.

## Report severity guide (triage only; confirm with `vulnerability-validation`)
- Critical/High: missing or bypassable authorization or authentication, injection with attacker-reachable input, secrets committed.
- Medium: weakened defaults, missing limits, information disclosure.
- Low/Info: hardening gaps with no demonstrated path.
