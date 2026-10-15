# Sources and provenance: semgrep-rule-authoring

## Official sources consulted

| Source | Used for |
| --- | --- |
| https://docs.semgrep.dev/writing-rules/rule-syntax | Required fields, severity values (LOW/MEDIUM/HIGH/CRITICAL, legacy INFO/WARNING/ERROR), pattern operators, `fix`, `metadata` |
| https://docs.semgrep.dev/writing-rules/testing-rules | `ruleid`/`ok`/`todoruleid`/`todook` annotations, test file naming, `semgrep --test`, `--validate` |
| Local Semgrep CLI 1.174.0 | Validated every rule and test in `examples.md`; `--dump-ast` confirmed to exist |

The docs page fetched for rule syntax did not describe `mode: taint` keys; those were confirmed by running the rules locally, not from the page.

## External repositories (ideas only)

| Repository | License | Decision |
| --- | --- | --- |
| trailofbits/skills (semgrep-rule-creator, semgrep-rule-variant-creator) | CC-BY-SA-4.0 (per repository README) | Ideas only (test-first rule writing, variant generalization). No text copied; all prose and rules are original. ShareAlike terms therefore not triggered. |

## Provenance

All text and rules in this skill are original work, written for this registry.
