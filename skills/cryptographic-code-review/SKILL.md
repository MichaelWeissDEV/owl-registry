---
name: cryptographic-code-review
description: >
  Review application code that uses cryptography for misuse: weak or wrong
  primitives, nonce/IV reuse, unauthenticated encryption, password hashing,
  key derivation, randomness, key management, certificate validation, and
  timing leaks. Use when a diff or codebase calls encryption, hashing, MAC,
  signature, KDF, or TLS APIs, or stores passwords or tokens. Not for
  designing new cryptographic protocols or primitives (do not invent them),
  general JWT/OAuth flow design (use oauth-jwt-auth), or secret storage
  logistics (use secrets-management).
compatibility: >
  Agent Skills-compatible coding agents reviewing code in any language that
  uses a mainstream crypto library.
metadata:
  author: michaelweissdev
  version: "1.0.0"
  tags: "cryptography, code-review, aes-gcm, nonce, password-hashing, kdf, randomness, tls, cwe"
  topics: "security, cryptography"
---

# Cryptographic Code Review

Cryptography fails at the integration layer far more often than in the math: wrong mode, reused nonce, unauthenticated ciphertext, fast hash for passwords, `Math.random()` for tokens, disabled certificate checks. This skill gives a systematic review of how code uses crypto libraries. It does not teach inventing primitives; the correct recommendation to custom crypto is always "use a vetted library and a high-level API".

Related skills: `security-code-review` (general taint review), `secure-coding`, `secrets-management` (where keys live), `oauth-jwt-auth` (token protocols), `vulnerability-validation` (confirming a finding), `security-differential-review` (crypto changes in a diff).

## Non-negotiable rules

1. Review only; never print, log, or paste real keys, tokens, or password hashes found during review. Cite location and recommend rotation.
2. Do not recommend rolling your own primitive, mode, padding, or protocol. Recommend a maintained library's high-level API (AEAD, secretbox, password-hash helper, TLS stack).
3. Name the standard you rely on (NIST SP, RFC, OWASP cheat sheet) and quote parameters from it, not from memory; parameters age.
4. Distinguish what the code does from what a comment claims it does. Trace the actual bytes: where the key comes from, where the nonce comes from, what is authenticated.
5. A finding needs an attacker model: what can the attacker observe, choose, or replay? Weak-looking code with no such path is a hardening note.

## Review procedure

### 1. Inventory every crypto touchpoint
```bash
rg -n -i 'AES|DES|RC4|MD5|SHA-?1|HMAC|pbkdf2|scrypt|bcrypt|argon|Cipher|encrypt|decrypt|sign\(|verify|SecureRandom|urandom|Math\.random|rand\(|InsecureSkipVerify|verify=False|CERT_NONE|ECB|CBC|nonce|iv\b|salt' src/
```
Classify each hit: password storage, data at rest, data in transit, token or ID generation, signature, integrity, key derivation, TLS client/server settings.

### 2. Apply the checks per purpose

| Purpose | Check | Typical CWE |
| --- | --- | --- |
| Encryption | Authenticated encryption (AEAD: AES-GCM, ChaCha20-Poly1305) rather than ECB, or CBC/CTR without a MAC | 327, 780 |
| Nonce / IV | Unique per key for GCM/ChaCha20; never constant, counter reset, or derived from low-entropy data | 323, 1204 |
| Randomness | Keys, nonces, tokens, salts from the OS CSPRNG, not `random`, `Math.random`, time seeds | 330, 338 |
| Password storage | Memory-hard or iterated KDF with per-user salt; not MD5/SHA-family alone | 916, 759, 760 |
| Key derivation | KDF from a high-entropy secret uses HKDF or SP 800-108 style KDF; passwords use a password KDF | 328, 916 |
| MAC / compare | HMAC with a proper key; comparison via constant-time function | 208, 385 |
| Signatures | Modern scheme (Ed25519, ECDSA P-256, RSA-PSS); verification result actually enforced; algorithm not attacker-selectable | 347, 327 |
| Key size/strength | AES-128+ (256 common), RSA 2048+, EC 256+; keys not hard-coded | 326, 321, 798 |
| TLS / certificates | Verification on, hostname checked, minimum TLS 1.2, no pinned test CA in prod | 295, 297 |
| Key lifecycle | Source, storage, rotation, separation per purpose (no one key for encrypt and sign) | 320 |

### 3. Key points per area

**AEAD and nonces.** NIST SP 800-38D (GCM) specifies a 96-bit IV as the default and requires IV uniqueness for a given key; a repeated (key, IV) pair in GCM exposes plaintext relationships and the authentication key. With random 96-bit IVs the SP 800-38D limit is 2^32 invocations per key, so high-volume encryptors need key rotation or a nonce-misuse-resistant or extended-nonce construction (for example AES-GCM-SIV, XChaCha20-Poly1305) from a vetted library. Look for: a nonce created once at startup, nonce derived from a record ID that can repeat, copy-pasted constant IVs, encrypting in several threads with a shared counter. Tag must be verified before using plaintext; check that decrypt exceptions are not swallowed. Bind context with associated data (record ID, version, purpose) when ciphertext could be swapped between rows.

**Unauthenticated modes.** ECB is always a finding for structured data. CBC or CTR without a MAC allows tampering; CBC with padding errors distinguishable by the caller invites padding oracles. Fix: switch to AEAD, not "add a try/except".

**Password hashing.** Parameters from the OWASP Password Storage Cheat Sheet (verified against the live page during authoring): Argon2id minimum m=19 MiB, t=2, p=1 (equivalent trade-offs listed there); scrypt N=2^17, r=8, p=1; bcrypt work factor at least 10 and a 72-byte input limit (legacy use); PBKDF2-HMAC-SHA256 600,000 iterations (PBKDF2 when FIPS compliance is required). NIST SP 800-132 covers PBKDF2 and recommends a random salt of at least 128 bits, with the iteration count set as high as tolerable. Check: per-user random salt (or library-managed), parameters stored with the hash for upgrades, rehash-on-login when parameters are raised, constant-time verify via the library, no truncation surprises with bcrypt.

**Key derivation.** Do not use a raw hash as a KDF from a password; do not use a password KDF where HKDF (RFC 5869) is appropriate. SP 800-108 defines KDFs from a key-derivation key. Use distinct `info`/context strings per purpose so one root secret yields independent subkeys.

**Randomness.** Tokens, session IDs, nonces, salts, keys: OS CSPRNG (`secrets`/`os.urandom`, `crypto.randomBytes`/`crypto.getRandomValues`, `SecureRandom`, `crypto/rand`). Flag seeded or general-purpose PRNGs. Check token length (128 bits of entropy is a common floor for unguessable tokens).

**Comparison.** MAC tags, tokens, and password hashes compared with `==` can leak through timing; use `hmac.compare_digest`, `crypto.timingSafeEqual`, `subtle.ConstantTimeCompare`, or `MessageDigest.isEqual`. Mark as a finding only where the attacker can measure and retry.

**TLS and certificates.** Search for disabled verification (`verify=False`, `InsecureSkipVerify: true`, `rejectUnauthorized: false`, `CERT_NONE`, custom trust-all managers). Any such setting reachable in production configuration is a finding; in tests it needs a guard against shipping.

**Signatures and JWT-like tokens.** Verification must enforce the expected algorithm rather than trusting the token header; reject `none`; check issuer/audience/expiry (see `oauth-jwt-auth`). A verify call whose boolean result is ignored is a finding.

## Worked example

```python
import os
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

NONCE = b"0" * 12                      # constant nonce

def seal(key: bytes, data: bytes) -> bytes:
    return AESGCM(key).encrypt(NONCE, data, None)
```
Finding: GCM nonce reused for every message under the same key (CWE-323/CWE-1204 class). An attacker who sees two ciphertexts learns the XOR of plaintexts and, with enough pairs, can forge tags. Evidence: constant at module level, no per-call generation. Severity depends on who sees ciphertexts and whether keys are long-lived; confidence high. Minimal fix:

```python
def seal(key: bytes, data: bytes, aad: bytes) -> bytes:
    nonce = os.urandom(12)
    return nonce + AESGCM(key).encrypt(nonce, data, aad)
```
with decrypt splitting the first 12 bytes, and key rotation before 2^32 messages per key. (The fixed snippet was syntax-checked only; the `cryptography` package was not installed in the authoring environment, so it was not executed.)

## Anti-patterns in reviews

- Flagging SHA-256 itself as "weak" when it is used for file integrity or inside HMAC; the issue is context.
- Demanding a specific algorithm fashion without an attacker model.
- Accepting "we encrypt it" as evidence of confidentiality when keys sit beside the data.
- Recommending custom schemes ("XOR with a hash", "double encrypt") instead of a vetted high-level API.
- Quoting iteration counts or key sizes from memory instead of the current standard.

## Verification checklist

- [ ] All crypto touchpoints inventoried and classified by purpose
- [ ] Mode is authenticated; nonce/IV source and uniqueness traced
- [ ] All security-relevant randomness comes from a CSPRNG
- [ ] Password storage uses a password KDF with current parameters, salt, upgrade path
- [ ] Keys: source, storage, separation by purpose, rotation; none hard-coded
- [ ] Verification results enforced; comparisons constant-time where attacker-measurable
- [ ] TLS verification on in production paths
- [ ] Each finding names attacker model, evidence, CWE, and a vetted-library fix

## References

- [references/checklist.md](references/checklist.md): language-specific API cues and finding templates
- [references/scenarios.md](references/scenarios.md): activation and evaluation scenarios
- [references/sources.md](references/sources.md): sources and provenance
