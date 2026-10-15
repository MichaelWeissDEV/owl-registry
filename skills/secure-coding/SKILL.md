---
name: secure-coding
description: >
  Apply defensive programming and secure software engineering principles
  to prevent common vulnerabilities (OWASP Top 10, CWE Top 25). Use when
  validating user input, parameterizing database queries, preventing XSS/CSRF/SSRF,
  handling sensitive authentication tokens, or configuring secure defaults.
compatibility: >
  Agent Skills-compatible coding agents writing, reviewing, or securing
  application code across languages.
metadata:
  author: michaelweissdev
  version: "1.0.0"
  tags: "security, secure-coding, owasp, injection, sanitization, cwe, auth"
  topics: "security, software-development"
---

# Defensive Secure Coding Practices

Secure coding is the practice of developing software in a manner that protects against vulnerabilities and security flaws. By applying strict input validation, contextual output encoding, cryptographic rigor, and the principle of least privilege, developers prevent exploitation of the OWASP Top 10 and CWE Top 25 flaws.

## Core Rules

1. **Never trust external input**: Treat all data originating from users, HTTP headers, query parameters, webhooks, or file uploads as untrusted. Validate on an allow-list basis.
2. **Always parameterize database queries**: Never concatenate user input directly into SQL, NoSQL, LDAP, or shell command strings.
3. **Contextual output encoding**: Encode data immediately before rendering it in browser contexts (HTML, JavaScript, CSS, URL) to prevent Cross-Site Scripting (XSS).
4. **Never hardcode secrets**: API keys, passwords, and tokens must be loaded from secure environment variables or vault secret managers, never committed to source control.
5. **Enforce least privilege**: Run processes under dedicated service accounts with minimal necessary filesystem, network, and database permissions.
6. **Use established cryptographic primitives**: Never invent custom encryption, hashing, or random number algorithms. Use standard libraries (e.g., `argon2id`, `bcrypt`, `crypto/rand`).

---

## 1. Preventing Injection Flaws (SQLi, Command Injection)

### SQL Injection Prevention
Always use parameterized queries or type-safe ORMs:

```python
# VULNERABLE: Direct string interpolation (SQL Injection!)
# cursor.execute(f"SELECT * FROM users WHERE email = '{user_email}'")

# SECURE: Parameterized query (driver handles escaping and typing)
cursor.execute("SELECT * FROM users WHERE email = %s", (user_email,))
```

### Command Injection Prevention
Avoid spawning shell interpreters (`shell=True` in Python or `exec()` in Node). Pass arguments as an explicit array directly to the operating system:

```python
# VULNERABLE: Invokes shell, vulnerable to 'filename.txt; rm -rf /'
# subprocess.run(f"convert {filename} output.png", shell=True)

# SECURE: Array execution without shell interpretation
subprocess.run(["convert", filename, "output.png"], check=True)
```

---

## 2. Preventing Cross-Site Scripting (XSS)

- In template engines (Jinja2, React, Blade), ensure auto-escaping is active.
- When rendering user-supplied HTML (e.g. Markdown output), sanitize with an allow-list sanitizer (DOMPurify, bleach).

```javascript
// SECURE in browser environments:
import DOMPurify from 'dompurify';

const cleanHtml = DOMPurify.sanitize(userSuppliedMarkdownHtml);
containerElement.innerHTML = cleanHtml;
```

---

## 3. Server-Side Request Forgery (SSRF) Prevention

When fetching URLs provided by users (e.g. webhooks, avatars):
1. Parse the scheme and allow only `https://` (block `file://`, `gopher://`, `dict://`).
2. Resolve DNS and verify that the target IP does **not** point to private/loopback address ranges (`127.0.0.0/8`, `10.0.0.0/8`, `172.16.0.0/12`, `192.168.0.0/16`, `169.254.169.254` AWS metadata).

```python
import ipaddress
import socket
from urllib.parse import urlparse

def is_safe_external_url(target_url: str) -> bool:
    parsed = urlparse(target_url)
    if parsed.scheme not in ("http", "https"):
        return False
    
    hostname = parsed.hostname
    if not hostname:
        return False

    try:
        # Resolve all IPs for hostname
        addr_info = socket.getaddrinfo(hostname, None)
        for _, _, _, _, sockaddr in addr_info:
            ip = ipaddress.ip_address(sockaddr[0])
            # Block loopback, private, link-local, and multicast addresses
            if ip.is_private or ip.is_loopback or ip.is_link_local:
                return False
        return True
    except socket.gaierror:
        return False
```

---

## 4. Password Hashing and Timing Attacks

1. Always hash passwords with modern memory-hard password functions (`Argon2id` or `bcrypt` with work factor >= 12).
2. Always compare authentication tokens, API keys, and HMAC signatures with **constant-time equality** to eliminate side-channel timing attacks:

```python
import hmac

# VULNERABLE: Leaks timing information byte-by-byte
# if provided_signature == expected_signature: ...

# SECURE: Constant-time comparison
if hmac.compare_digest(provided_signature, expected_signature):
    # Authenticated successfully
```

---

## 5. Common Mistakes and Anti-Patterns

| Anti-Pattern | Vulnerability | Correct Practice |
| :--- | :--- | :--- |
| `eval()` or `Function()` with user input | Remote Code Execution (RCE) | Parse with `JSON.parse()` or strict schema parser |
| Storing plain MD5 or SHA256 for passwords | Trivial lookup via rainbow tables / GPU cracking | Use `argon2id` or `bcrypt` with salt |
| Missing rate limiting on login/reset endpoints | Credential stuffing & brute-force | Implement exponential backoff or token bucket rate limiting |
| Trusting `X-Forwarded-For` without proxy trust config | IP spoofing and rate-limit bypass | Only trust proxy headers when IP matches configured reverse proxy |

---

## 6. Verification Checklist

- [ ] All database queries use parameterized placeholders.
- [ ] No direct shell execution (`shell=True`, `system()`, backticks) with external inputs.
- [ ] Constant-time comparison (`hmac.compare_digest`) used for token and signature verification.
- [ ] SSRF defenses validate resolved IP addresses against private network ranges.
- [ ] Security scanners (e.g. Bandit, Semgrep, CodeQL) report 0 high/critical issues.
