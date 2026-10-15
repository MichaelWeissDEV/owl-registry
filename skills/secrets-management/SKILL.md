---
name: secrets-management
description: >
  Manage, rotate, inject, and protect application secrets, API keys, certificates,
  and credentials throughout development and deployment lifecycles. Use when
  configuring environment variables, implementing secret stores (Vault, AWS Secrets
  Manager), enforcing .gitignore hygiene, detecting committed secrets with gitleaks,
  or executing credential rotation and revocation procedures.
compatibility: >
  Agent Skills-compatible coding agents managing configurations, infrastructure,
  or source repositories.
metadata:
  author: michaelweissdev
  version: "1.0.0"
  tags: "secrets, security, credentials, gitleaks, vault, api-keys, env-vars"
  topics: "security, devops"
---

# Secrets Management & Credential Hygiene

Secrets (API tokens, private encryption keys, database passwords, OAuth client secrets) are high-value targets. Hardcoding secrets in source control or leaving them in unencrypted configuration files risks immediate compromise. Secure systems enforce zero-knowledge repository storage, dynamic injection at runtime, automated leak scanning, and regular credential rotation.

## Core Rules

1. **Zero secrets in source control**: Never commit credentials, passwords, or tokens to git repositories—even private repositories or scratch branches.
2. **Never log secrets or environment dumps**: Sanitize logs and never execute `env` or `print(os.environ)` in scripts whose outputs are logged.
3. **Use `.env.example` templates**: Commit sanitized templates with dummy values (`DATABASE_URL=postgres://user:pass@localhost:5432/db`) to document required keys without exposing real values.
4. **Scan pre-commit with Gitleaks**: Block secrets before they reach git commits using automated pre-commit hooks and CI scanners.
5. **Immediate revocation on exposure**: If a secret is committed or leaked, consider it immediately compromised. Invalidate and rotate the credential immediately—merely rewriting git history is insufficient.

---

## 1. Local Development Secrets & Git Hygiene

Ensure all local secret files are strictly excluded in `.gitignore`:

```gitignore
# Environment & Secrets
.env
.env.local
.env.*.local
*.pem
*.key
*.p12
*.crt
id_rsa
id_ed25519
credentials.json
service_account.json
```

### Loading Environment Variables Safely
```python
import os
from pathlib import Path

def get_required_secret(name: str) -> str:
    val = os.getenv(name)
    if not val:
        raise RuntimeError(
            f"Required secret '{name}' is not set in environment. "
            "Ensure it is configured in your secret manager or local .env file."
        )
    return val
```

---

## 2. Automated Secret Detection with Gitleaks

Detect accidentally staged or committed credentials before pushing:

```bash
# Scan local git repository history for high-entropy secrets and known signatures
gitleaks detect --verbose

# Run scan on uncommitted working tree and staged index
gitleaks protect --staged --verbose
```

---

## 3. Incident Response: Remediation of Leaked Secrets

If a secret is accidentally committed to a repository:

```
[ALERT: Secret Committed to Repository]
                   │
                   ▼
1. REVOKE & ROTATE IMMEDIATELY (Highest Priority!)
   - Go to vendor portal (AWS, Stripe, GitHub, Database).
   - Invalidate the old key and issue a new one.
   - Update running production instances with the new key.
                   │
                   ▼
2. ASSESS BLAST RADIUS
   - Inspect cloud audit logs (CloudTrail, vendor access logs)
     to check if the exposed key was used by an attacker.
                   │
                   ▼
3. PURGE GIT HISTORY
   - Use `git-filter-repo` or BFG Repo-Cleaner to rewrite history.
   - (Note: Rewriting git history does NOT un-leak a key if the repo
     was pushed or scraped by bots. Revocation is always mandatory!)
```

Purging history with `git-filter-repo`:
```bash
# Remove a file from all commits in history
git-filter-repo --path credentials.json --invert-paths
```

---

## 4. Production Secret Injection Patterns

In cloud environments (Kubernetes, AWS, GCP), inject secrets into process memory at runtime rather than baking them into container disk images:

- **AWS Secrets Manager**: Injected via IAM role-based SDK fetches or CSI Secrets Store driver.
- **HashiCorp Vault**: Injected via sidecar agent into an in-memory `tmpfs` volume (`/vault/secrets/config.json`).
- **Kubernetes Secrets**: Mounted as files in read-only tmpfs volumes (`/etc/secrets/token`).

---

## 5. Common Mistakes and Anti-Patterns

| Anti-Pattern | Risk | Correct Practice |
| :--- | :--- | :--- |
| Committing `.env` with production keys | Immediate credential compromise | Add `.env` to `.gitignore`; commit `.env.example` |
| Pasting API keys into pull request comments | Logged in GitHub database and sent via unencrypted email notifications | Use secret managers and local env files |
| Deleting a commit with a secret via `git reset` | Secret remains in git reflog and remote cache | Revoke the secret immediately at the provider |
| Hardcoding secrets in Dockerfiles (`ENV API_KEY=...`) | Baked permanently into Docker image layers | Pass via build secrets (`--secret id=...`) or runtime env |

---

## 6. Verification Checklist

- [ ] `.gitignore` contains patterns for `.env`, `*.pem`, `*.key`, and credential JSON files.
- [ ] Gitleaks scan (`gitleaks detect`) passes with 0 findings.
- [ ] No hardcoded tokens, passwords, or private keys in the code diff.
- [ ] `.env.example` documents all required configuration variables without real secrets.
