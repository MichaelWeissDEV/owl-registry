# Sources and Provenance

## Official sources consulted (2026-10-15)

| URL | Used for |
|---|---|
| https://developer.hashicorp.com/terraform/language/manage-sensitive-data | `sensitive` only hides values in CLI/UI and still stores them in state and plan files; ephemeral values (1.10+), write-only arguments (1.11+), `sensitive` 0.15+; recommendations to encrypt and restrict state. |
| https://github.com/aquasecurity/tfsec | Notice that tfsec is now part of Trivy, migration encouraged, same scanning engine. |
| https://trivy.dev/latest/docs/scanner/misconfiguration/ | `trivy config <dir>`, auto type detection, internet needed for checks bundle. |
| https://trivy.dev/latest/docs/coverage/iac/terraform/ | HCL/JSON/plan/plan-JSON inputs, `--tf-vars`, `--tf-exclude-downloaded-modules`, plan limitation for for_each/count. |
| https://github.com/bridgecrewio/checkov | Maintained by Prisma Cloud, Apache-2.0; plan scanning workflow (`terraform show -json`, `checkov -f`), line-0 note. |

## Not verified

- Terraform behavior of `init -backend=false`, `data "external"` executing at plan time and provider evaluation: standard documented Terraform behavior, not re-fetched; terraform is not installed locally so no command was run.
- OpenTofu equivalence is assumed for the described workflow; check differences on versions in use.
- Trivy and Checkov flags should be confirmed with `--help` on the installed version; no scanner was executed.
- The S3 snippet in SKILL.md was not run through `terraform validate`.

## Provenance

All text is original. External skill repositories (anthropics/skills, obra/superpowers, trailofbits/skills, vercel-labs/agent-skills, huggingface/skills, supabase/agent-skills) were not consulted; nothing copied.
