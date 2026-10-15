---
name: terraform-security-review
description: >
  Review Terraform code, plans and state for security risks without changing infrastructure:
  public exposure, over-broad IAM, unencrypted storage, secrets in code/state/plans, unsafe
  modules and providers, and weak state backends. Covers static scanning with Trivy and Checkov
  (tfsec has been folded into Trivy), plan-JSON review, and how to triage and report findings.
  Use when asked to audit, security-review or gate a Terraform change or repo, or to decide if
  a scanner finding is real. Not for authoring or refactoring Terraform (use terraform-iac), for
  cloud account architecture (aws-cloud-architecture), for running apply/destroy/import, nor for
  reading or printing state files and secret values.
compatibility: >
  Terraform or OpenTofu repositories. Static review needs only file access; optional tools: terraform
  (for validate and plan JSON), trivy, checkov. Scanner flags checked against current docs; verify
  with --help on the installed version.
metadata:
  author: michaelweissdev
  version: "1.0.0"
  tags: "terraform, security, iac, trivy, checkov, iam, state, review"
  topics: "security, devops"
---

# Terraform Security Review

A Terraform review answers: *what will exist after apply, who can reach it, who can do what with it, and what secrets are exposed along the way?* Scanners find known patterns; humans must judge context (is this bucket public on purpose?) and the things scanners miss (trust relationships across accounts, module provenance, state exposure). Findings must be tied to a file, resource and line, with an explained impact and a concrete fix.

Boundaries: writing and structuring Terraform is `terraform-iac`; cloud design is `aws-cloud-architecture`; secret handling in general is `secrets-management`; broader code review is `security-code-review`; a suspected breach goes to `incident-response`.

## Non-negotiable rules

1. **Review is read-only.** Never run `terraform apply`, `destroy`, `import`, `taint/untaint`, `state rm/mv/push`, `force-unlock`, `workspace delete`, or anything that mutates infrastructure or state. If the user asks, treat each as a separate authorization with a shown plan.
2. **Do not read or print state files or secret values.** State (`terraform.tfstate`, remote state, `terraform show` of real state, `terraform output -json/-raw`) can contain secrets in plaintext; `sensitive = true` only hides values from CLI output and still stores them in state and plan files (official Terraform docs). Review the *configuration*; if state access is necessary, ask first, query specific non-sensitive attributes, and never paste results.
3. **Treat plan files and plan JSON as secret-bearing.** They contain sensitive values too. Do not commit, upload to third-party scanners, or paste them. Delete local copies after review.
4. **Untrusted code can execute at plan time.** `terraform init` downloads providers and modules; `terraform plan` evaluates `data "external"` and provider code and needs cloud credentials. For code you do not trust, stay static (read files, `trivy config`, `checkov -d`) and do not give it real credentials. Prefer `terraform init -backend=false` plus `terraform validate` when a toolchain run is needed.
5. **No credentials in the review environment beyond what is needed**, and never enter or request credentials in chat.
6. **Report facts, not scanner scores.** Each finding needs evidence from the code and a stated impact; mark confidence and unverified assumptions.

## Workflow

### 1. Scope and inventory

Identify: Terraform vs OpenTofu, required versions (`required_version`), providers and versions (`required_providers`, `.terraform.lock.hcl`), module sources (registry, git, local), backends, workspaces/environments, CI that runs plan/apply, and who can approve. Ask what the blast radius is (which accounts/subscriptions) and what data classes the resources hold.

### 2. Run static scanners (offline-safe, read-only)

```bash
trivy config ./infra            # misconfiguration scan of Terraform (HCL); auto-detects types
trivy config --tf-vars prod.tfvars ./infra   # evaluate with variable overrides
checkov -d ./infra              # Checkov directory scan
```

Status of tools (checked 2026-10-15): the **tfsec** repository states that tfsec is now part of Trivy and encourages migration; Trivy uses the same Terraform scanning engine. **Checkov** is maintained by Prisma Cloud under Apache-2.0. Trivy needs internet access to download its checks bundle (there is an air-gapped mode in its docs). For new setups use Trivy (and optionally Checkov); do not recommend tfsec for new work.

Scanner limits you must say out loud: they see only what is in the scanned files (not live drift), can miss logic across modules, and report noise for intentional design. Treat a clean scan as "no known-pattern findings", not "secure".

### 3. Optionally scan the plan (resolved values)

Only with approval and credentials appropriate to a read-only plan, in a throwaway working directory:

```bash
terraform init -backend=false         # no remote state access (plan then reflects only configuration)
terraform plan -out=tfplan
terraform show -json tfplan > tfplan.json
trivy config tfplan.json
checkov -f tfplan.json
```

Plan scanning sees resolved values and `count`/`for_each` expansions, but Trivy documents a limitation: references through `for_each`/`count` may not link (for example bucket and its ACL), suppressing some checks. Checkov notes JSON plan output is one line, so findings report line 0 unless reformatted (`jq .`). Remember step rule 3: the plan files are sensitive.

### 4. Manual review checklist (what scanners under-detect)

| Area | Look for | Why it matters |
|---|---|---|
| IAM | `"*"` actions or resources, `iam:PassRole` with `*`, wildcard principals, cross-account trusts without conditions (`ExternalId`, org id), admin policies attached to workloads | Privilege escalation, confused deputy |
| Network | `0.0.0.0/0` or `::/0` ingress on admin/DB ports, public IPs, public subnets for data stores, missing flow logs | Exposure |
| Storage/data | Public buckets/ACLs, missing block-public-access, no encryption at rest or customer-managed key where required, no versioning/logging on critical stores, snapshots shared publicly | Data leakage |
| Secrets | Hardcoded passwords/keys in `.tf`, `.tfvars`, `default =` values, `user_data`, provisioners; secrets output; `random_password` stored in state | Secrets in VCS, state and plan |
| State/backend | Remote backend encrypted (e.g. S3 `encrypt`), versioned, access-restricted, locked, audited; no local state committed; separate state per environment | State is the crown jewels |
| Supply chain | Unpinned modules (`ref=main`), unpinned providers, modules from unknown registries or forks, missing `.terraform.lock.hcl` in VCS | Malicious module/provider update |
| Execution | `local-exec`/`remote-exec` provisioners, `data "external"`, `null_resource` running scripts | Code runs with pipeline credentials |
| Logging/detection | CloudTrail/audit logging, retention, alerting resources removed or disabled | Detection gaps |
| Lifecycle | `prevent_destroy` missing on stateful resources, `ignore_changes` hiding security drift | Reliability and drift |
| CI | Pipeline can apply from forks/PRs, long-lived admin keys instead of OIDC, plan output posted publicly | Pipeline compromise |

Sensitive-data features (official docs): `sensitive` (Terraform 0.15+) only masks output; ephemeral values (1.10+) and write-only arguments (1.11+, provider-supported `_wo` attributes) keep values out of state and plan files. Recommending them is valid when the provider supports it; check the provider docs and the Terraform version in use.

### 5. Triage each finding

For each scanner or manual finding decide: **true positive**, **false positive** (explain), **accepted risk** (needs owner and expiry), or **cannot determine** (state what is missing). Check context: environment, whether the resource is intentionally public (static website bucket), compensating controls (WAF, SCP). Never mass-suppress; inline ignores need an ID, a reason and an owner.

### 6. Report

Per finding: ID, severity with rationale, resource and file:line, evidence (the relevant 3-10 lines, scrubbed of secrets), impact, recommended fix as a diff or snippet, residual risk. Add a summary of tools, versions, scope reviewed, what was not reviewed (state, live cloud, runtime), and open questions. Fixes are proposals; do not push changes without authorization.

## Worked example

Finding from `trivy config`: S3 bucket without public access block. Review: the resource is `aws_s3_bucket.assets` referenced by a CloudFront distribution; manual check shows a bucket policy allowing `s3:GetObject` to `Principal: "*"`. Judgment: true positive; the CDN origin should use origin access control rather than a public bucket. Fix proposal:

```hcl
resource "aws_s3_bucket_public_access_block" "assets" {
  bucket                  = aws_s3_bucket.assets.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}
```

plus replacing the wildcard policy with a CloudFront service principal statement scoped by `AWS:SourceArn`. Residual risk: confirm no other consumers rely on direct public reads. Nothing was applied; the snippet is illustrative and was not validated with `terraform validate` in this session.

## Anti-patterns

- Treating scanner output as the review, or "0 findings" as proof of security.
- Running `terraform plan`/`apply` with production credentials on unreviewed code.
- Opening `terraform.tfstate` to "check a value" and pasting it.
- Uploading plan JSON to an external service.
- Suppressing findings wholesale or leaving `skip` comments with no reason.
- Recommending tfsec for new pipelines.
- Fixing by widening permissions "to make the plan pass".
- Ignoring the CI/CD identity that applies the code.

## Verification checklist

- [ ] No mutating Terraform command run; no state or secret values read or shown.
- [ ] Scope, versions, tool versions recorded.
- [ ] Scanner findings triaged individually; manual checklist applied.
- [ ] Each reported finding has file:line evidence, impact and fix.
- [ ] Plan files and local artifacts removed or secured.
- [ ] Limits and unreviewed areas stated.

## References

- [references/review-checklist.md](references/review-checklist.md): extended per-provider and state/backend questions.
- [references/scenarios.md](references/scenarios.md): scenarios.
- [references/sources.md](references/sources.md): sources and provenance.
