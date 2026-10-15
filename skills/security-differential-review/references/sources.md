# Sources and provenance: security-differential-review

## Official sources consulted

| Source | Used for |
| --- | --- |
| https://owasp.org/www-project-code-review-guide/ (OWASP Code Review Guide) | General review practice: trust boundaries, risk-prioritized reading |
| https://cwe.mitre.org/data/definitions/862.html and /639.html | CWE-862 Missing Authorization, CWE-639 Authorization Bypass Through User-Controlled Key (used in the worked example) |
| https://git-scm.com/docs/git-diff, git-log, git-blame | Three-dot diff semantics, `-S` pickaxe, `--diff-filter`, `blame -w -C` |

## External repositories (ideas only)

| Repository | License | Decision |
| --- | --- | --- |
| trailofbits/skills (differential-review) | CC-BY-SA-4.0 (per repository README) | Ideas only (risk-first triage, reading removals, caller search). No text copied; all content original. |

## Provenance

All text is original work written for this registry. The OWASP and MITRE pages were referenced from existing knowledge of their content and not re-fetched during authoring; verify links before citing in a report.
