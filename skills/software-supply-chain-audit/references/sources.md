# Sources and provenance: software-supply-chain-audit

## Official sources consulted

| Source | Used for |
| --- | --- |
| https://slsa.dev/spec/v1.0/levels (fetched during authoring; page notes the current spec is v1.2 and v1.0 is retired) | Build track L0-L3 definitions; the skill cites v1.2 |
| https://spdx.dev/ and https://cyclonedx.org/ | SBOM formats (SPDX 2.3/3.0, CycloneDX 1.6, ECMA-424) and VEX; cited from knowledge, not re-fetched |
| https://docs.npmjs.com/ (npm ci, audit signatures, provenance) | Command behavior; cited from knowledge, not re-fetched; confirm with `npm help` |
| https://docs.github.com/en/actions/security-guides/using-artifact-attestations-to-establish-provenance-for-builds | `gh attestation verify`; cited from knowledge |
| https://github.com/ossf/scorecard and https://google.github.io/osv-scanner/ | Scorecard CLI and osv-scanner v2 syntax; cited from knowledge |
| https://cwe.mitre.org/data/definitions/427.html | Uncontrolled search path element (dependency confusion class) |

Command flags in `references/commands.md` were not executed during authoring; verify with each tool's `--help`.

## External repositories (ideas only)

| Repository | License | Decision |
| --- | --- | --- |
| trailofbits/skills (supply-chain-risk-auditor) | CC-BY-SA-4.0 (per repository README) | Ideas only (audit dependencies as trust decisions). Only the README listing was viewed; nothing copied. |

## Provenance

All text is original work written for this registry.
