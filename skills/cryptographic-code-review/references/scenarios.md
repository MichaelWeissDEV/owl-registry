# Scenarios: cryptographic-code-review

All scenarios: Status: written, not executed.

## 1. Positive Activation

Prompt: "Review this module that encrypts user documents with AES and stores password hashes; look for crypto mistakes."

Expected: skill activates; agent inventories crypto touchpoints, checks mode, nonce source, password KDF parameters, randomness, key handling, and cites standards.

Status: written, not executed

## 2. Negative Activation

Prompt: "Design a custom end-to-end encrypted messaging protocol for us." or "Where should we store our API keys?"

Expected: skill does not design a new protocol (recommends vetted protocols and libraries and specialist review); key storage logistics go to `secrets-management`.

Status: written, not executed

## 3. Execution Evaluation

Task: Review a snippet that encrypts with AES-GCM using a module-level constant 12-byte nonce, hashes passwords with `hashlib.sha256(password)`, and generates reset tokens with `random.choices`.

Pass rubric (all required):
- Three findings: nonce reuse in GCM, fast unsalted hash for passwords, non-CSPRNG token generation.
- Each finding has location, attacker model, CWE, and a fix using a vetted library API.
- Password fix cites current parameters from OWASP or NIST SP 800-132 rather than invented numbers.
- No recommendation to implement a custom primitive; no secrets echoed.

Fail: calls SHA-256 "broken", misses nonce reuse, or recommends a homemade scheme.

Status: written, not executed
