---
name: security-code-review
description: >
  Perform structured, evidence-based security reviews of source code and diffs:
  map the attack surface, trace untrusted data from source to sink, check
  authorization and tenancy, assess crypto and secret handling, classify findings
  by CWE and OWASP with severity and a confidence level. Use when reviewing a pull
  request for security regressions, auditing a service or module you are authorized
  to review, or writing remediation guidance with tests. Do not use for exploiting
  systems you do not own, penetration testing live targets, auditing third-party
  agent skills (use skill-security-audit), hardening CI workflows (use
  github-actions-security), or general code-quality review.
compatibility: >
  Agent Skills-compatible coding agents reading source code. Read-only by default;
  running code or tests requires the user's go-ahead. OWASP references checked
  against Top 10:2025 and API Security Top 10:2023 in October 2026.
metadata:
  author: michaelweissdev
  version: "1.1.0"
  tags: "security, code-review, vulnerabilities, cwe, owasp, trust-boundaries, audit"
  topics: "security, software-development"
---

# Security-Focused Code Review

A security review audits trust boundaries, untrusted data flows, authorization decisions, and failure behavior. Every finding must be reproducible from the code, classified, and honest about confidence. Reviewing is defensive: describe how a flaw works and how to fix it; do not produce weaponized exploits or probe systems you were not asked to assess.

Deeper material:
- [Sink catalog, false-positive triage, and severity guidance](references/review-playbook.md)

## When to use / not use

Use on code you are authorized to review (your repository, a PR, an agreed audit scope). Not for live attack of third-party systems, malware development, or evading detection. Related skills: `github-actions-security` (workflows), `skill-security-audit` (agent skills), `postgresql-development` (RLS and SQL design), `mcp-server-development` (MCP servers).

## Core rules

1. **Scope first.** State what is in scope (paths, commit, services) and what was not reviewed. A review of a diff does not cover untouched callers.
2. **Map ingress, then trace to sinks.** Ingress: HTTP parameters/headers/cookies, bodies, uploads, webhooks, message queues, files and archives, environment, CLI args, data stored by other users, LLM output. Sinks: SQL, shell, filesystem paths, template/HTML output, deserializers, XML parsers, redirects, outbound HTTP, crypto primitives, logs.
3. **Server-side enforcement only.** Client checks are not controls. Every invariant (authentication, object ownership, role, input validity, price) must hold on the server.
4. **Check authorization on every object access and state change** (BOLA/IDOR, function-level access, mass assignment). Authentication is not authorization.
5. **Prefer the structural fix** (parameterized query, argument array, allow-list, framework escaping) over blacklist filtering.
6. **Evidence and confidence.** Each finding cites file and line, the data path, and a confidence level (confirmed by reading the full path; probable; needs runtime check). Do not report a pattern match as a vulnerability until you have checked reachability and existing mitigations.
7. **Never read, print, or commit secrets.** If you find one in the diff, report location and type, redact the value, and recommend rotation.
8. **Do not run exploit code against real systems.** If a proof is needed, use a minimal, non-destructive test against a local or disposable instance with the owner's approval.

## Workflow

1. **Understand the change or component**: purpose, actors, assets (what an attacker wants), and trust boundaries (browser, API, service, tenant, third party).
2. **Enumerate ingress points and sensitive sinks** with search (grep for framework route decorators, `exec`, `query(`, `open(`, `deserialize`, `redirect`, `fetch`, `eval`, `innerHTML`, etc.).
3. **Trace each source to a sink**: note transformations and validation. Ask at each hop: who controls this value, is it encoded for this sink's context, and is the check applied before use (TOCTOU)?
4. **Review control families** using the checklist below.
5. **Triage**: discard findings with a strong existing mitigation; downgrade unreachable ones; merge duplicates.
6. **Write findings** with the template; propose a fix and a regression test.
7. **State residual risk and what you did not check.**

## Checklist by control family

**Authentication and sessions**
- Passwords: Argon2id preferred (OWASP minimum m=19456 KiB, t=2, p=1); bcrypt only for legacy (work factor at least 10, 72-byte input limit); never fast hashes (SHA-256, MD5) for passwords.
- Tokens/JWT: server pins the allowed algorithm(s) (do not trust the header `alg`), verifies signature, `exp`, `iss`, and `aud`; session ids are random, rotated on login, invalidated on logout and password change.
- Login, reset, and MFA flows: rate limiting, no user enumeration, single-use short-lived reset tokens.

**Authorization and tenancy**
- Every handler that takes an object id checks ownership or tenant membership in the same query or immediately before use.
- Role checks on state-changing endpoints; deny by default; no authorization decided from client-supplied fields.
- Mass assignment: bind only allow-listed fields; never accept `role`, `tenant_id`, `is_admin` from the request body.

**Input handling and injection**
- SQL: parameterized only; identifiers via allow-list. Shell: no shell, argument arrays, allow-listed commands. Paths: canonicalize and verify containment (including symlinks). Templates/HTML: context-aware escaping; no raw HTML sinks with user data. XML: external entities disabled. Deserialization: no native object deserialization of untrusted data (pickle, Java serialization, unsafe YAML load).
- Outbound requests built from user URLs (SSRF): allow-list hosts, resolve and block private/link-local/metadata addresses after redirects, restrict schemes.
- Redirects: validate target against an allow-list.

**Cryptography and secrets**
- Secrets not in source or logs; loaded from a secret manager or injected environment; rotation path exists.
- Authenticated encryption (AES-GCM, ChaCha20-Poly1305) with unique nonces; no ECB; no home-made schemes; random values from a CSPRNG (`secrets`, `crypto.randomBytes`, `crypto/rand`).
- TLS verification not disabled (`verify=False`, `rejectUnauthorized: false`).

**Error handling, logging, resilience**
- Errors fail closed; exceptions do not grant access; no stack traces or secrets in responses or logs; no unbounded resource use (size limits, timeouts, pagination caps).

**Dependencies and build**
- New dependencies reviewed for need and provenance; lockfile updated; no install-time scripts from unknown sources.

## Finding template

```markdown
### [HIGH] Report endpoint lacks tenant ownership check (BOLA)
- CWE: CWE-639 (Authorization Bypass Through User-Controlled Key)
- OWASP: API1:2023 Broken Object Level Authorization; Top 10:2025 A01 Broken Access Control
- Location: src/api/reports.py:38-45
- Confidence: confirmed (full path read; no middleware enforces ownership)
- Data path: path param report_id -> SELECT by id only -> returned to caller

Description: any authenticated user can fetch another tenant's report by supplying its id.

Fix: constrain the query by the caller's organization.
    SELECT * FROM reports WHERE id = :id AND organization_id = :org_id
Test: user A requests user B's report id and receives 404.
```

Severity: combine impact (data/function exposed, blast radius) and likelihood (reachability, required privileges, preconditions). Use CVSS only when the user needs a score; always explain the reasoning in words.

## Worked example (condensed)

Diff adds `GET /files?name=...` that returns `open(BASE + name).read()`. Source: query param. Sink: filesystem read. Check: no canonicalization. Finding: path traversal (CWE-22), confidence confirmed. Fix: resolve the real path and verify it is inside `BASE` using a path-relation check (not string prefix), reject symlink escapes, and map ids to files instead of accepting names. Test: `../` and absolute-path inputs return 400/404.

## Anti-patterns in reviewing

| Mistake | Consequence | Instead |
| :--- | :--- | :--- |
| Reporting every `exec(` or `eval(` hit | Noise, lost trust | Confirm the argument is attacker-influenced |
| Accepting client-side validation as a control | Bypassed trivially | Require server enforcement |
| Fixing with a regex blacklist | Bypass by encoding | Structural fix at the sink |
| Marking JWT secure because it is signed | `alg` confusion, missing `aud`/`exp` checks | Verify claims and pin algorithm |
| Only reviewing the diff | Missed callers and config | Read the surrounding call path |
| Pasting a found secret into the report | New leak | Redact and recommend rotation |
| Claiming "no vulnerabilities" | Overstated assurance | List what was and was not reviewed |

## Verification checklist

- [ ] Scope and exclusions stated.
- [ ] Every ingress mapped to its sinks; unresolved paths listed.
- [ ] Authorization checked per object access and state change.
- [ ] Each finding has location, data path, CWE/OWASP, severity, confidence, fix, and test.
- [ ] No secret values reproduced; no exploit run against real systems.
- [ ] Residual risk and unreviewed areas stated.

## Sources

- OWASP Top 10:2025: https://top10.owasp.org/2025
- OWASP API Security Top 10 2023: https://owasp.org/API-Security/
- OWASP Password Storage Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html
- MITRE CWE: https://cwe.mitre.org/
