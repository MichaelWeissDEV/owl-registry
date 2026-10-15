# Test plan template and evidence format

## Plan

```
Target(s):            (exact hosts/URLs, environment)
Authorization basis:  (own localhost app | staging owned by us | written scope ref + date)
Window:               (start/end, timezone)
Allowed techniques:   (passive, authenticated manual, active scan Y/N)
Prohibited:           (DoS, social engineering, data extraction, production writes)
Rate limit:           (requests per second)
Accounts/roles:       (test users: user A, user B, admin; how created)
Data handling:        (synthetic only; where evidence is stored; deletion date)
Contacts / stop rule: (who to call, what triggers an immediate stop)
Priority areas:       (from threat model)
```

## Finding record

```
ID / Title:
WSTG category + test ID:
Asset:
Preconditions:        (role, state, data)
Steps to reproduce:   (numbered, minimal, using test data)
Expected (secure) behavior:
Observed behavior:
Evidence:             (redacted request/response summary, screenshot)
Impact:               (C/I/A in business terms)
Severity + method:    (e.g. CVSS vector or High/Med/Low rubric)
Recommendation:
Retest result:
```

## Evidence handling

- Redact cookies, tokens, `Authorization` headers, personal data.
- Store evidence in the agreed location; delete per the data-handling rule.
- Do not include working exploit chains; include only the minimal steps needed for the owner to reproduce.

## Security headers quick reference (verify against current MDN/OWASP guidance)

| Header | Purpose |
|---|---|
| `Strict-Transport-Security` | Force HTTPS |
| `Content-Security-Policy` | Restrict script/style/frame sources; `frame-ancestors` controls embedding |
| `X-Content-Type-Options: nosniff` | Disable MIME sniffing |
| `Referrer-Policy` | Limit referrer leakage |
| `Permissions-Policy` | Restrict powerful browser features |
| `Cache-Control: no-store` | On responses with sensitive data |

Check with `curl -sI https://staging.example.test`, only against targets you are authorized to test.
