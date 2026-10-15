---
name: security-code-review
description: >
  Perform structured, evidence-based security code reviews to identify vulnerabilities,
  trust boundary violations, and injection flaws. Use when auditing pull requests
  for security regressions, mapping findings to CWE and OWASP classifications,
  tracing untrusted data flows, or validating cryptographic implementations.
compatibility: >
  Agent Skills-compatible coding agents performing security analysis on source code.
metadata:
  author: michaelweissdev
  version: "1.0.0"
  tags: "security, code-review, vulnerabilities, cwe, owasp, trust-boundaries, audit"
  topics: "security, software-development"
---

# Security-Focused Code Review

A security code review differs from a general quality review by specifically auditing trust boundaries, untrusted data flows, authorization gates, and vulnerability classes (CWE / OWASP). Security findings must be evidence-backed, reproducible, and classified by impact and exploitability.

## Core Rules

1. **Map the attack surface first**: Identify every ingress point where external data enters the system (HTTP params, headers, WebSockets, file uploads, environment variables, webhooks).
2. **Follow data flow from Source to Sink**: Trace untrusted input from the source (e.g. `request.body`) to sensitive sinks (e.g. SQL query, system shell, file path, HTML template, cryptographic key).
3. **Never trust client-side validation**: Frontend checks are convenience features for honest users; attackers bypass them entirely. All security invariants must be enforced on the backend.
4. **Identify trust boundary crossings**: Any data crossing between processes, networks, privilege levels, or tenants must be validated and authenticated.
5. **Map findings to formal CWE / OWASP taxonomy**: Standardized vulnerability definitions eliminate ambiguity and streamline remediation.

---

## 1. Security Review Methodology (Source-to-Sink Analysis)

```
[Sources: Untrusted Input]
├── HTTP Query/Body/Headers
├── File Uploads / Tarballs
├── Webhooks / 3rd Party APIs
└── Database / Redis Reads (if stored by other users)
         │
         ▼ (Tracing Data Flow & Transformations)
[Sanitization & Validation Boundaries]
         │
         ▼
[Sinks: Dangerous Operations]
├── Database Execution ────────> Check for SQL Injection (CWE-89)
├── Shell / Process Execution ──> Check for Command Injection (CWE-78)
├── Filesystem Path / Read ─────> Check for Path Traversal (CWE-22)
├── HTML / DOM Output ──────────> Check for Cross-Site Scripting (CWE-79)
└── Outbound HTTP Fetch ────────> Check for SSRF (CWE-918)
```

---

## 2. Security Review Checklist

### 1. Authentication & Session Management
- Are passwords hashed using Argon2id or bcrypt (work factor >= 12)?
- Are session tokens and JWTs verified for signature, expiration (`exp`), and algorithm (`alg != "none"`)?
- Are tokens invalidated on logout or password reset?

### 2. Authorization & Multi-Tenancy (BOLA / IDOR)
- Does the endpoint verify that the authenticated user **owns** the requested object ID (`/api/documents/{id}`)?
- Are role checks enforced on every state-changing route (RBAC / ABAC)?

### 3. Cryptography & Secrets
- Are secrets loaded from environment variables rather than hardcoded in source?
- Is encryption using modern authenticated ciphers (e.g. AES-256-GCM, ChaCha20-Poly1305)?
- Are random values generated with cryptographically secure PRNGs (`crypto/rand`, `secrets`)?

---

## 3. High-Impact Finding Template

```markdown
### [CRITICAL] Insecure Direct Object Reference (IDOR / BOLA) allows tenant data exfiltration
- **CWE**: [CWE-639](https://cwe.mitre.org/data/definitions/639.html): Authorization Bypass Through User-Controlled Key
- **OWASP**: API1:2023 Broken Object Level Authorization
- **Location**: `src/api/reports.py#L38-L45`

#### Vulnerability Description
The endpoint `GET /api/v1/reports/{report_id}` fetches a report by its UUID without checking whether
the report belongs to the authenticated user's `organization_id`. Any authenticated user can enumerate
or provide another tenant's report UUID to download proprietary financial statements.

#### Vulnerable Code
```python
@router.get("/reports/{report_id}")
async def get_report(report_id: UUID, current_user: User = Depends(get_current_user)):
    report = await db.fetch_one("SELECT * FROM reports WHERE id = :id", {"id": report_id})
    if not report:
        raise HTTPException(404, "Report not found")
    return report # Missing tenant ownership check!
```

#### Remediation
Enforce tenant isolation in the SQL query:
```python
report = await db.fetch_one(
    "SELECT * FROM reports WHERE id = :id AND organization_id = :org_id",
    {"id": report_id, "org_id": current_user.organization_id}
)
```
```

---

## 4. Verification Checklist

- [ ] All external input sources identified and mapped to sinks.
- [ ] Findings categorized by standard CWE and severity ratings.
- [ ] No hardcoded secrets, test credentials, or private keys in the diff.
- [ ] Remediation provides explicit code snippets and tests.
