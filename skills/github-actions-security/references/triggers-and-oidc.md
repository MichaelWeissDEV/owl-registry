# Privileged Triggers, Injection Sinks, and OIDC Troubleshooting

Sources: GitHub Docs "Secure use reference" and "Security hardening for GitHub Actions" (checked October 2026). Verify details there; GitHub changes these defaults.

## Which trigger runs with what

| Trigger | Runs workflow from | Secrets / write token for fork PRs | Safe use |
| :--- | :--- | :--- | :--- |
| `pull_request` | merge ref of the PR | No secrets, read-only token for forks | Build and test untrusted code |
| `pull_request_target` | base branch | Yes | Label, comment, triage. Do not check out or execute PR head code |
| `workflow_run` | default branch | Yes | Second stage that consumes artifacts of an untrusted run; treat artifacts as untrusted data |
| `issue_comment`, `issues` | default branch | Yes | Treat body and title as hostile strings |
| `push` to protected branch | that branch | Yes | Deploy after review |
| `workflow_dispatch` | selected ref | Yes | Inputs come from whoever can run it; still pass via `env:` |

## Safe two-workflow pattern for fork PRs that need a comment

1. Workflow A (`pull_request`, `permissions: contents: read`): build and test; upload only a small data artifact (for example a JSON of results). No secrets.
2. Workflow B (`workflow_run` on A, minimal write permission such as `pull-requests: write`): download the artifact, validate it strictly (schema, size, expected keys), and post the comment. Never execute anything from the artifact and never interpolate its contents into a shell.

## Injection sinks beyond `run:`

```yaml
# Vulnerable: untrusted value reaches a script as code
- uses: actions/github-script@<sha>
  with:
    script: |
      console.log("${{ github.event.issue.title }}")

# Safer: pass data through the environment, read it as data
- uses: actions/github-script@<sha>
  env:
    ISSUE_TITLE: ${{ github.event.issue.title }}
  with:
    script: |
      console.log(process.env.ISSUE_TITLE)
```

Also dangerous: `echo "x=${{ github.head_ref }}" >> "$GITHUB_ENV"` (a newline in a branch name can add variables), writing untrusted text to `GITHUB_OUTPUT` without a safe delimiter, and `eval` or `bash -c` on event data. Untrusted fields include PR title/body, branch names, commit messages, issue and comment bodies, author names and emails, and workflow_dispatch inputs.

## Cache and artifact poisoning

A cache entry or artifact written by a low-trust run (for example a PR from a fork or a branch anyone can push to) can be restored by a higher-trust run with the same key. Scope cache keys by trust level, do not restore caches in jobs that hold secrets from untrusted branches, and verify artifacts before use.

## Dependabot for action pins

```yaml
# .github/dependabot.yml
version: 2
updates:
  - package-ecosystem: "github-actions"
    directory: "/"
    schedule:
      interval: "weekly"
```

## OIDC `sub` claim cheat sheet

| Job configuration | `sub` presented |
| :--- | :--- |
| No environment, push to `main` | `repo:ORG/REPO:ref:refs/heads/main` |
| `environment: production` | `repo:ORG/REPO:environment:production` |
| `pull_request` event, no environment | `repo:ORG/REPO:pull_request` |
| Tag push | `repo:ORG/REPO:ref:refs/tags/TAG` |

Cloud trust policies should match the exact value you expect (and `aud`). GitHub can customize `sub` composition at the repository or organization level; if it was customized, the table does not apply, so check the repository's OIDC settings.

## OIDC failure diagnosis

| Symptom | Likely cause | Check |
| :--- | :--- | :--- |
| `Not authorized to perform sts:AssumeRoleWithWebIdentity` | Trust policy `sub` or `aud` mismatch (most often the job uses an environment, so `sub` has no ref) | Compare the policy condition with the table above |
| `Credentials could not be loaded` / token request fails | Job lacks `permissions: id-token: write` | Add it at job level only |
| Works on `main`, fails on PR | PR jobs present a different `sub` (`pull_request`), which the trust policy rightly rejects | Do deployments only from trusted refs; use a separate read-only role for PR jobs if needed |
| Works for one repository, fails after rename or transfer | `sub` contains the old repository name | Update the trust policy |

Do not print the OIDC JWT or cloud credentials in logs to debug; masked or not, they are bearer credentials.

## Self-hosted runner hygiene

Use ephemeral (just-in-time) runners, isolate them from internal networks, and do not attach them to public repositories. Persistent runners can be compromised by one malicious job and affect later jobs.
