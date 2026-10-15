# Skill Authoring & Quality Guidelines

This guide defines the standards, structure, and validation rules for authoring skills in the OWL Registry.

## 1. Skill Philosophy

An Agent Skill is a structured instruction package that equips AI coding assistants (Claude Code, OpenCode, Codex, Gemini CLI, Cursor, etc.) with professional engineering practices.

A skill must:
- **Direct agent behavior**: Provide unambiguous rules, step-by-step procedures, and concrete code patterns.
- **Enforce quality standards**: Rely on official ecosystem specifications (PEP 8/257, Rust API Guidelines, SemVer, Keep a Changelog, OWASP).
- **Be non-destructive**: Read-only exploration first; require explicit confirmation before mutating state.
- **Be self-contained and passive**: Skills are data. No scripts are ever executed automatically during installation or discovery.

---

## 2. Directory Layout & File Rules

Each skill resides directly under `skills/<skill-name>/`:

```text
skills/<skill-name>/
├── SKILL.md              # Mandatory: YAML frontmatter + instructions (< 500 lines)
├── skill.json            # Optional: metadata overlay
├── references/           # In-depth technical guides, language rules, deep dives
└── assets/               # Reusable code skeletons, templates, or mock files
```

- **Flat layout**: No author subdirectories in `skills/`.
- **Directory naming**: Directory name must exactly match frontmatter `name:` (lowercase letters, digits, single hyphens, <= 64 chars).
- **Progressive disclosure**: Keep `SKILL.md` under 500 lines. Place detailed references in `references/` and static templates in `assets/`.
- **Link paths**: All links to bundled files must be relative to the skill folder (e.g. `[Typing Guide](references/typing.md)`).

---

## 3. Frontmatter & Metadata

Use YAML frontmatter adhering to the Agent Skills specification:

```yaml
---
name: python-development
description: >
  Develop, review, and refactor idiomatic Python applications.
  Use when implementing Python modules, designing Python APIs,
  reviewing Python code, or improving maintainability and correctness.
compatibility: >
  Agent Skills-compatible coding agents with access to Python
  source code. Python tooling is required only for executable checks.
metadata:
  author: michaelweissdev
  version: "1.0.0"
  tags: "python, programming, coding, best-practices"
  topics: "software-development"
---
```

### Frontmatter Fields
- `name` (required): Unique skill identifier matching the folder name.
- `description` (required): Max 1024 characters. Must define both **what** the skill does and **when** it should activate.
- `compatibility` (optional): Max 500 characters. Environment or toolchain requirements.
- `metadata.author`: Author handle (e.g. `michaelweissdev`).
- `metadata.version`: SemVer string (`1.0.0`).
- `metadata.tags`: Comma-separated search keywords.
- `metadata.topics`: High-level taxonomy topics.

---

## 4. Registry Taxonomy

### Standard Topics
- `version-control`: Git, branching, worktrees, conflicts, releases, semver.
- `operating-systems`: Linux CLI, filesystems, permissions, systemd, macOS.
- `programming-languages`: Python, Rust, C, C++, Go, JavaScript, TypeScript, Java, Kotlin, Swift, Web.
- `software-development`: Architecture, refactoring, error handling, API design, code comments.
- `testing`: Unit testing, integration testing, TDD, debugging workflows.
- `documentation`: Markdown, technical writing, READMEs, Sphinx, Mermaid diagrams.
- `office`: PDF, Word (.docx), Excel (.xlsx), PowerPoint (.pptx), LaTeX, CSV.
- `databases`: SQL, PostgreSQL, relational modeling.
- `security`: Secure coding, security review, threat modeling, secrets, container security, hardening.
- `devops`: Docker, GitHub Actions, dependency management, release engineering.
- `ai-agents`: Agent skill authoring, skill security audit, MCP server development.
- `devtools`: Command-line tools, linters, formatters, and utilities.

---

## 5. Local Validation Workflow

Before submitting a pull request, validate your skill with the OWL CLI:

```bash
# Validate individual skill directory
owl validate ./skills/my-new-skill

# Check full registry consistency
owl registry check .

# Search for the skill
owl search my-new-skill
```
