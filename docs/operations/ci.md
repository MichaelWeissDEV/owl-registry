# CI workflow

`.github/workflows/registry.yml` (managed by OWL: `owl registry init` / `owl registry upgrade`) has two jobs.

| Job | When | Permissions | What it does |
| --- | --- | --- | --- |
| `validate` | pull requests and pushes touching `skills/**` or `registry.json` | `contents: read` | `owl registry check .` – structure, names, frontmatter, paths, sizes, index consistency |
| `index` | after a successful validation on a push to `main` | `contents: write` | `owl registry index .`, then commits `index.json`, `stats.json`, `INDEX.md`, `STATS.md` if they changed |

Pull requests – also from forks – never get write access. Skill scripts are never executed. The `index`
job needs the full git history (`fetch-depth: 0`) because update times and revisions come from git.
