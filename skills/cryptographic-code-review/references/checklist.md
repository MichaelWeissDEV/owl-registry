# API cues and finding templates

## Cues by language (what to grep for and what good looks like)

| Concern | Red flag | Preferred direction |
| --- | --- | --- |
| Randomness | Python `random`, JS `Math.random`, Java `java.util.Random`, Go `math/rand`, C `rand()` for secrets | Python `secrets`/`os.urandom`; Node `crypto.randomBytes`; Java `SecureRandom`; Go `crypto/rand`; OS CSPRNG |
| Timing-safe compare | `==` on MACs or tokens | `hmac.compare_digest`; `crypto.timingSafeEqual`; `subtle.ConstantTimeCompare`; `MessageDigest.isEqual` |
| TLS verification off | `verify=False`, `InsecureSkipVerify: true`, `rejectUnauthorized: false`, `ssl.CERT_NONE`, trust-all `X509TrustManager` | Default verification; add a private CA to the trust store if needed |
| Encryption mode | `AES/ECB/...`, `AES.MODE_ECB`, `createCipher` (Node, derives key and IV poorly), CBC without MAC | AEAD APIs (AES-GCM, ChaCha20-Poly1305) from a maintained library |
| Password hashing | `md5`, `sha1`, `sha256` of a password, unsalted, fixed iterations 1000 | Argon2id, scrypt, bcrypt, PBKDF2 with current parameters |
| Hard-coded keys | Literal base64/hex key, IV, or password in source or committed config | Key from managed secret store (see `secrets-management`) |
| Signature checks | Verify result ignored; `alg` read from attacker input | Fixed expected algorithm; verify result enforced |

## Finding template

```
Title: <misuse> in <component>
Location: file:line
Purpose: (password storage | data at rest | transit | token | signature)
Observed: <what the code does, with the relevant lines>
Attacker model: <what the attacker can see, choose, or replay>
Standard: <NIST SP / RFC / OWASP cheat sheet> and CWE-<id>
Impact: <in this system's terms>
Confidence: high | medium | low (and why)
Fix: <vetted library and high-level API; migration note for existing data>
```

## Migration notes

- Changing a password hash: store algorithm and parameters with the hash; verify with the old scheme and rehash on successful login; do not bulk re-hash without passwords.
- Changing an encryption format: version-prefix ciphertexts so old and new can coexist; re-encrypt lazily or in a controlled batch.
- Rotating keys: introduce key IDs in ciphertext headers before rotating.
- Never "fix" by logging the key or plaintext to debug.
