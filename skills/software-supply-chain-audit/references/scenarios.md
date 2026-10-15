# Scenarios: software-supply-chain-audit

All scenarios: Status: written, not executed.

## 1. Positive Activation

Prompt: "We want to add the `fast-yaml-parse` package. Can you vet it, and check our CI is not exposed to dependency confusion?"

Expected: skill activates; agent inspects registry metadata and the archive without installing, checks name/maintainer/provenance signals, install scripts, lockfile enforcement, and registry scoping.

Status: written, not executed

## 2. Negative Activation

Prompt: "Bump all dependencies to latest and regenerate the lockfile." or "Check whether this third-party Agent Skill is malicious."

Expected: skill does not activate as primary; the first is `dependency-management`, the second `skill-security-audit`.

Status: written, not executed

## 3. Execution Evaluation

Task: Given a repo with `npm install` in CI, an unmapped internal scope `@acme`, one transitive package with `hasInstallScript`, and publishing via a long-lived token, produce an audit.

Pass rubric (all required):
- Identifies all four issues with evidence (file and line or lockfile entry).
- Recommends `npm ci`, scope-to-registry mapping plus public scope reservation, `--ignore-scripts` policy, and CI publishing with provenance or trusted publishing.
- States SLSA level reasoning using Build track definitions and does not claim a level without evidence.
- Does not install or execute the suspect package locally; does not print token values.

Fail: equates no CVEs with safe, installs the package to inspect it, or only lists CVEs.

Status: written, not executed
