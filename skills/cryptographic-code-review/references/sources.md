# Sources and provenance: cryptographic-code-review

## Official sources consulted

| Source | Used for |
| --- | --- |
| https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html (fetched during authoring) | Argon2id m=19 MiB/t=2/p=1 minimum, scrypt N=2^17/r=8/p=1, bcrypt cost >=10 and 72-byte limit, PBKDF2-HMAC-SHA256 600,000 iterations |
| NIST SP 800-38D (Galois/Counter Mode) | 96-bit IV default, IV uniqueness per key, 2^32 invocation limit with random IVs (cited from knowledge of the standard, not re-fetched) |
| NIST SP 800-132 (password-based key derivation) | PBKDF2 salt of at least 128 bits, iteration count as high as tolerable (cited from knowledge, not re-fetched) |
| NIST SP 800-108 (KDFs from a key-derivation key) and RFC 5869 (HKDF) | Distinction between password KDFs and key-based KDFs (cited from knowledge) |
| MITRE CWE: 323, 326, 327, 328, 330, 338, 295, 208, 916, 1204 | Weakness naming |

Verify the NIST items against the current publications before quoting them verbatim in a report.

## External repositories (ideas only)

| Repository | License | Decision |
| --- | --- | --- |
| trailofbits/skills (constant-time-analysis, zeroize-audit) | CC-BY-SA-4.0 (per repository README) | Ideas only (timing and key-zeroization concerns). Only the README listing was viewed; nothing copied. Zeroization and compiler-level constant-time analysis are out of scope for this skill. |

## Provenance

All text is original work written for this registry. The Python snippets were compile-checked; the `cryptography` package was not available locally, so they were not executed.
