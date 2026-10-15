# Extended Review Checklist

Review the code; do not open state. Questions are phrased so they can be answered from `.tf` files, `.tfvars` (names only, never values), CI config and documentation.

## Backend and state

- Is a remote backend configured, with encryption at rest, versioning, locking and restricted access?
- Who can read state? Anyone with read access can read every secret stored in it, because Terraform stores `sensitive` values in state and plan files (Terraform docs).
- Is state split per environment/blast radius? Is there a break-glass process for state access, with audit logs?
- Are `terraform.tfstate*`, `*.tfplan`, `crash.log` and `*.tfvars` with secrets in `.gitignore`? (Check with a read-only `git ls-files` for committed ones; report paths, not contents.)

## Providers and modules

- Provider and module versions pinned (`version =`, `ref=<tag or sha>`)? `.terraform.lock.hcl` committed?
- Module sources: pinned registry versions or git SHAs preferred over branches. Unknown publishers or forks need provenance checks.
- Does any module or provider use `external`, `local-exec`, or `http` data sources that send data out or execute code?

## IAM and identity

- Least privilege: enumerate actions and resources of every policy; flag `*:*`, `iam:*`, `sts:AssumeRole` to broad principals, `iam:PassRole` unconstrained.
- Trust policies: who can assume; conditions present for cross-account or OIDC subjects (repo and branch claims for CI OIDC).
- Long-lived access keys created by Terraform (`aws_iam_access_key`) end up in state: prefer short-lived identity.
- Service accounts / managed identities per workload rather than shared.

## Data protection

- Encryption at rest with intended keys; key policies not `*`.
- TLS enforced (bucket policies `aws:SecureTransport`, load balancer listener policies, minimum TLS).
- Backups, snapshots, replicas: encrypted and not public/shared unintentionally.
- Logging buckets protected; retention meets policy.

## Network

- Security groups / firewall rules: source ranges, ports; admin ports (22, 3389, DB ports) not world-open.
- Private endpoints for data services where required; no public IP on data stores.
- Egress controls for sensitive workloads.

## Secrets handling

- Secrets come from a secret manager or are generated and stored there; no literals in code or `default`.
- Variables carrying secrets marked `sensitive`; understand this does not keep them out of state. Where the provider supports it, prefer ephemeral/write-only patterns (Terraform 1.10/1.11+).
- No secrets in `user_data`, tags, outputs, or provisioner commands (they appear in state, logs and cloud consoles).

## CI/CD

- Who can trigger `apply`? Branch protections, required approvals, no apply from forks, plan output not posted publicly.
- Pipeline credentials: OIDC or short-lived, scoped per environment, not org admin.
- Drift detection and policy checks (Trivy/Checkov/OPA) run in PRs and fail on high severity.

## Scanner triage vocabulary

| Verdict | Requirement |
|---|---|
| True positive | Evidence in code plus impact |
| False positive | Explain why (e.g. attribute set via separate resource the scanner could not link) |
| Accepted risk | Named owner, justification, expiry date, inline ignore with ID |
| Undetermined | State what information is missing |
