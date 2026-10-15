# Contributing a skill

A skill is a directory below `skills/`:

```text
skills/<name>/
  SKILL.md        required: YAML frontmatter + instructions
  skill.json      optional: extra metadata (author, version, tags, topics, license, ...)
  scripts/ references/ assets/    optional bundled files
```

## Rules

- The directory name **must equal** the skill `name`. There is no author directory – put the author
  into the metadata.
- `SKILL.md` needs `name` and `description` (at most 1024 characters) in its frontmatter.
- Names are unique in this registry.
- No symlinks, no absolute or `..` paths, files at most 5 MiB, a skill at most 20 MiB.
- Skills are data: CI never executes anything from a skill, and neither should the registry.

## Workflow

1. Fork and create a branch.
2. `owl registry publish ./my-skill --dir .` (or copy the directory by hand).
3. `owl validate ./skills/my-skill` and `owl registry check .` – fix everything they report.
4. Open a pull request. CI repeats the check with read-only permissions.
5. After the merge CI updates `index.json`, `stats.json`, `INDEX.md` and `STATS.md`. Do not edit these files.

Quality expectations are in {doc}`skill-authoring`. External submissions are audited for prompt
injection and malicious payloads (see the `skill-security-audit` skill).
