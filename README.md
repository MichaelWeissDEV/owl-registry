<p align="center">
  <img src="assets/owl.png" alt="OWL" width="120">
</p>

<h1 align="center">owl-registry</h1>

<p align="center">The default OWL skill registry — curated, high-quality foundation skills for AI coding agents and assistants.</p>

<p align="center">
  <img alt="Development status: alpha" src="https://img.shields.io/badge/status-alpha-orange">
  <a href="https://github.com/MichaelWeissDEV/OWL"><img alt="Served by OWL" src="https://img.shields.io/badge/served%20by-OWL-8b5a2b"></a>
  <a href="https://github.com/MichaelWeissDEV/owl-registry/blob/main/INDEX.md"><img alt="Skills" src="https://img.shields.io/badge/dynamic/json?url=https://raw.githubusercontent.com/MichaelWeissDEV/owl-registry/main/index.json&query=%24.count&label=skills&color=blue"></a>
  <a href="https://github.com/MichaelWeissDEV/owl-registry/actions/workflows/registry.yml"><img alt="Validation" src="https://github.com/MichaelWeissDEV/owl-registry/actions/workflows/registry.yml/badge.svg"></a>
  <a href="https://github.com/MichaelWeissDEV/owl-registry"><img alt="Registry" src="https://img.shields.io/badge/registry-owl--registry-green"></a>
</p>

> **Alpha:** This registry is served by [OWL](https://github.com/MichaelWeissDEV/OWL), which is under active development; the registry layout and index format may still change.

---

## What is the OWL Registry?

The **OWL Registry** provides a comprehensive, production-grade foundation library of **80 curated Agent Skills** designed for AI coding assistants—including Claude Code, OpenCode, Codex, Gemini CLI, Cursor, and any system compatible with the [Agent Skills standard](https://agentskills.io/specification).

Rather than generic prompt snippets, each skill in this registry provides:
- **Strict technical guardrails** that prevent improvisation and hallucinated flags.
- **Progressive disclosure** with in-depth language and tool guides in `references/` and templates in `assets/`.
- **Reproducible, safe workflows** prioritizing read-only inspection before state mutation.
- **Verification checklists** to ensure software changes are proven correct before task completion.

Documentation: **<https://owl-registry.readthedocs.io>** (sources in [`docs/`](docs/index.md)). Browse the editorial [Skill Catalog](docs/guide/skill-catalog.md) for domain overviews, [`INDEX.md`](INDEX.md) for the generated index, [`STATS.md`](STATS.md) for metrics, or read [`index.json`](index.json) directly from automated tooling.

---

## Skill Categories at a Glance

| Category | Skills | Focus Areas |
| :--- | :---: | :--- |
| **Git & Releases** | 8 | Conventional Commits, branch workflows, worktrees, merge conflicts, SemVer, changelogs, release engineering, GitHub PRs |
| **Operating Systems & Shell** | 8 | Linux CLI, defensive Bash scripting, filesystems, permissions & ACLs, systemd & journald, networking, troubleshooting, macOS/BSD |
| **Languages & Web** | 22 | Python, Rust, C, C++, Go, JavaScript, TypeScript, Node.js, Java, Kotlin, Swift, SQL, PostgreSQL, MongoDB, Redis, Elasticsearch, Kafka, GraphQL, gRPC, HTML5/CSS3 |
| **Quality & Methods** | 13 | Cross-language code comments, code reviews, debugging workflows, unit testing, integration testing, TDD, refactoring, error handling, API design, system architecture, profiling, Playwright, observability |
| **Document Formats** | 11 | Markdown, technical writing, READMEs, PDF, Word (.docx), Excel (.xlsx), PowerPoint (.pptx), LaTeX, CSV, Sphinx, Mermaid diagrams |
| **Security & DevOps** | 15 | Secure coding (OWASP), security code reviews, threat modeling, secrets, OAuth/JWT, Docker, container security, Kubernetes, Terraform, Ansible, AWS, GitHub Actions, dependency management, Linux hardening |
| **AI Agents & Tools** | 3 | Agent skill authoring (meta-skill), skill security auditing, Model Context Protocol (MCP) server development |

---

## How to Use It

### 1. Add the Registry to OWL
```console
$ owl registry add owl-registry https://github.com/MichaelWeissDEV/owl-registry.git
```

### 2. Search and Discover Skills
Search by text keywords, tags, or high-level topics:
```console
# Full-text search across names, descriptions, and content
$ owl search python -r owl-registry

# Filter by specific topic
$ owl search --topic security -r owl-registry

# Filter by specific tags
$ owl search --tag concurrency -r owl-registry
```

### 3. Install Skills
Install globally or into the current project:
```console
# Install a single skill for Claude Code (default)
$ owl install python-development -r owl-registry

# Install for a specific tool (e.g. OpenCode, Codex, Cursor)
$ owl install python-development -r owl-registry --target opencode

# Install all skills in the registry
$ owl install --all -r owl-registry

# Install project-locally (saves to ./.claude/skills or target directory)
$ owl install rust-development -r owl-registry --project
```

---

## Architecture & Passive Data Model

- **Flat Layout**: All skills live under `skills/<name>/SKILL.md`. Author attribution is stored as metadata (`author: michaelweissdev`).
- **Passive Data**: Skills are purely declarative instructions. Nothing from a skill is ever executed during discovery, indexing, or installation.
- **Progressive Disclosure**: Primary instructions reside in `SKILL.md` (< 500 lines). Deep technical documentation resides in `references/` and templates in `assets/`.
- **Generated Metadata**: `index.json`, `stats.json`, `INDEX.md`, and `STATS.md` are generated automatically by CI after merge. They must never be edited manually.

---

## Contributing New Skills

We welcome community contributions! Please review [`CONTRIBUTING.md`](CONTRIBUTING.md) and [`docs/skill-authoring.md`](docs/guide/skill-authoring.md) before submitting a pull request.

1. Create a branch: `git checkout -b feat/add-my-skill`.
2. Add your skill directory: `skills/<my-skill>/SKILL.md`.
3. Validate locally:
   ```bash
   owl validate ./skills/my-skill
   owl registry check .
   ```
4. Open a pull request. GitHub Actions validates all changes with read-only permissions.
5. After merge, CI automatically updates the registry index and statistics.

---

## Security & Trust Boundaries

Agent skills operate within the local environment of the user. To maintain trust:
- No background network telemetry or hidden tracking.
- No automatic execution of third-party shell scripts.
- No harvesting or access to credentials (`~/.ssh`, `~/.aws`, `.env`).
- All external skill submissions are audited for prompt injection and malicious payloads using [`skill-security-audit`](skills/skill-security-audit/SKILL.md).

---

## License

No license has been chosen yet. Until the owner decides, all rights remain with the author. Skills may
carry their own `license` in their metadata. See the [documentation](docs/index.md).
