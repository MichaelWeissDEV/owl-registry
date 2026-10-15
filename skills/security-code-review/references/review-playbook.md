# Review Playbook: Sinks, Triage, Severity

## Sink catalog (what to grep, what to check)

| Class (CWE) | Dangerous patterns to search | Safe pattern to look for |
| :--- | :--- | :--- |
| SQL injection (CWE-89) | string formatting or concatenation into `execute`/`query`; ORM raw fragments | bound parameters; allow-listed identifiers |
| Command injection (CWE-78) | `os.system`, `subprocess(..., shell=True)`, `child_process.exec`, backticks, `Runtime.exec(String)` | argument array, no shell, allow-listed command |
| Path traversal (CWE-22) | `open(base + user)`, `path.join(base, user)` without containment check, archive extraction | canonical path inside base; extraction that rejects `..`, absolute paths, symlinks |
| XSS (CWE-79) | `innerHTML`, `dangerouslySetInnerHTML`, `v-html`, template `\|safe` filter, `Markup()` | framework auto-escaping; sanitizer with a strict allow-list |
| SSRF (CWE-918) | HTTP client with user URL | host allow-list, post-DNS IP checks, redirect re-validation, scheme limits |
| Unsafe deserialization (CWE-502) | `pickle.loads`, `yaml.load` (unsafe loader), Java `ObjectInputStream`, `unserialize` | JSON/data-only formats; safe loaders |
| XXE (CWE-611) | XML parser with entity/DTD resolution on | parser configured to disable DTDs and external entities |
| Open redirect (CWE-601) | `redirect(request.args["next"])` | relative-path or allow-list validation |
| CSRF (CWE-352) | cookie-authenticated state change without token or SameSite | CSRF token and `SameSite`, or non-cookie auth |
| Mass assignment (CWE-915) | `Model(**request.json)`, `update(request.body)` | explicit field allow-list |
| Race / TOCTOU (CWE-367) | check then act on file or balance | atomic operation, lock, or constraint |
| Weak randomness (CWE-330) | `random`, `Math.random` for tokens | CSPRNG |
| Hard-coded secrets (CWE-798) | keys/tokens in source, test fixtures that look real | secret manager, placeholders |
| Sensitive data in logs (CWE-532) | logging request bodies, headers, tokens | redaction, allow-listed fields |
| Template injection (CWE-1336) | rendering user-controlled template strings | fixed templates, user data as variables only |
| Missing TLS verification (CWE-295) | `verify=False`, `rejectUnauthorized: false` | default verification |
| Prompt injection into LLM tools | untrusted text concatenated into tool-using prompts; tool output trusted as instructions | separation of data from instructions, least-privilege tools, human confirmation for sensitive actions |

## False-positive triage

Before reporting, answer: (1) Is the value attacker-controlled? (2) Is there validation or encoding between source and sink that fits the sink's context? (3) Is the code reachable in production (feature flags, test-only, dead code)? (4) Does the framework mitigate it by default? (5) What is the privilege needed to reach it? If you cannot answer, label confidence "needs runtime check" rather than guessing.

## Severity guidance

| Impact | Typical examples |
| :--- | :--- |
| Critical | Unauthenticated remote code execution; auth bypass; cross-tenant read/write of all data |
| High | Authenticated BOLA exposing other users' records; SQL injection reachable by low-privilege users; stored XSS in admin views |
| Medium | Reflected XSS needing interaction; SSRF limited by network controls; missing rate limiting on login |
| Low | Verbose errors; missing security headers without exploit path |

Adjust by exploitability (preconditions, privileges, user interaction) and asset sensitivity. Say why.

## Reviewing a pull request efficiently

1. Read the description and the files changed; list new routes, queries, parsers, file operations, and config changes.
2. For each new ingress, trace to sinks. For each changed authorization check, read the old and new logic side by side.
3. Check tests: do they cover the negative case (other tenant, bad role, malformed input)?
4. Check dependency and config changes (new packages, relaxed CORS, debug flags, widened IAM or token permissions).
5. Write findings in order of severity; keep style nits out of the security report.

## Safe handling of proof-of-concept

Prefer a unit or integration test that fails before the fix and passes after. Use local fixtures, not real data or live targets. Do not include working payloads for third-party systems.
