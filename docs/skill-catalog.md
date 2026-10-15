# OWL Registry Skill Catalog

This editorial catalog provides an overview of the curated skills available in the OWL Registry organized by technical domain.

For the auto-generated, machine-readable index with exact commit revisions, hashes, and timestamps, see [`INDEX.md`](../INDEX.md) and [`index.json`](../index.json).

---

## Category A — Git, Versioning and Releases
- [`conventional-commits`](../skills/conventional-commits/SKILL.md) — Conventional Commits 1.0.0 specification and commit message authoring.
- [`git-workflow`](../skills/git-workflow/SKILL.md) — Git status, diff inspection, staging boundaries, and clean commits.
- [`git-branching-worktrees`](../skills/git-branching-worktrees/SKILL.md) — Feature branches, branch lifecycles, and isolated Git worktrees.
- [`git-merge-conflicts`](../skills/git-merge-conflicts/SKILL.md) — Three-way merge conflict detection and safe resolution without data loss.
- [`semantic-versioning`](../skills/semantic-versioning/SKILL.md) — SemVer 2.0.0, evaluating breaking changes and version bump rules.
- [`changelog-writing`](../skills/changelog-writing/SKILL.md) — Keep a Changelog 1.1.0 conventions and release notes curation.
- [`release-engineering`](../skills/release-engineering/SKILL.md) — Pre-release verification checklists, artifact validation, and rollbacks.
- [`github-issues-prs`](../skills/github-issues-prs/SKILL.md) — Reproducible bug reports, PR descriptions, and code review discussions.

## Category B — Operating Systems & Shell
- [`linux-cli`](../skills/linux-cli/SKILL.md) — GNU/Linux pipes, redirection, text processing (grep, sed, awk), and processes.
- [`bash-scripting`](../skills/bash-scripting/SKILL.md) — Defensive Bash 4+ scripts with strict error modes, traps, and shellcheck.
- [`linux-filesystems`](../skills/linux-filesystems/SKILL.md) — FHS hierarchy, ext4/XFS, inodes, hardlinks, symlinks, and mounts.
- [`linux-permissions`](../skills/linux-permissions/SKILL.md) — POSIX permissions, SUID/SGID/Sticky bits, ACLs, and capabilities.
- [`linux-processes-systemd`](../skills/linux-processes-systemd/SKILL.md) — Processes, systemd services, timers, journald, and cgroup limits.
- [`linux-networking`](../skills/linux-networking/SKILL.md) — IP routing, DNS, sockets (ss), curl diagnostics, and firewalls.
- [`linux-troubleshooting`](../skills/linux-troubleshooting/SKILL.md) — Systematic diagnosis of OOM crashes, disk exhaustion, high load, and services.
- [`macos-cli`](../skills/macos-cli/SKILL.md) — macOS Darwin/BSD toolchain differences, Homebrew, launchd, and Gatekeeper.

## Category C — Programming Languages & Frameworks
- [`python-development`](../skills/python-development/SKILL.md) — Idiomatic Python 3.10+, PEP 8/257, type hints, dataclasses, and asyncio.
- [`python-packaging`](../skills/python-packaging/SKILL.md) — pyproject.toml, wheels, sdists, uv, build backends, and publishing.
- [`rust-development`](../skills/rust-development/SKILL.md) — Ownership, borrowing, lifetimes, Result/Option, traits, and safe Rust.
- [`rust-cargo`](../skills/rust-cargo/SKILL.md) — Multi-crate Cargo workspaces, additive features, dependencies, and publishing.
- [`c-development`](../skills/c-development/SKILL.md) — C11/C17 memory safety, pointers, buffer bounds, UB prevention, and sanitizers.
- [`cpp-development`](../skills/cpp-development/SKILL.md) — Modern C++ (C++17/20/23), RAII, smart pointers, Rule of Zero, and CMake.
- [`go-development`](../skills/go-development/SKILL.md) — Go modules, consumer interfaces, error wrapping, goroutines, and context.
- [`javascript-development`](../skills/javascript-development/SKILL.md) — Modern ECMAScript (ES2022+), ES Modules, Promises, async/await, and event loop.
- [`typescript-development`](../skills/typescript-development/SKILL.md) — Strict TypeScript, discriminated unions, type narrowing, and tsconfig.
- [`nodejs-development`](../skills/nodejs-development/SKILL.md) — Node.js 18+ runtime, stream pipelines, graceful shutdown, and CLI tools.
- [`java-development`](../skills/java-development/SKILL.md) — Modern Java 17/21 LTS, Records, pattern matching, sealed classes, and JUnit 5.
- [`kotlin-development`](../skills/kotlin-development/SKILL.md) — Null safety, data classes, sealed interfaces, coroutines, and Flow.
- [`swift-development`](../skills/swift-development/SKILL.md) — Swift API Design Guidelines, value types, actors, Swift Concurrency, and SPM.
- [`sql-development`](../skills/sql-development/SKILL.md) — Relational SQL, JOIN semantics, CTEs, constraints, and ACID transactions.
- [`postgresql-development`](../skills/postgresql-development/SKILL.md) — JSONB, GIN indexes, EXPLAIN ANALYZE, zero-downtime migrations, and RLS.
- [`web-html-css`](../skills/web-html-css/SKILL.md) — Semantic HTML5, CSS Grid, Flexbox, custom properties, and WCAG AA accessibility.

## Category D — Code Quality & Engineering Methods
- [`code-comments`](../skills/code-comments/SKILL.md) — Multi-language guide for meaningful comments and docstrings.
- [`code-review`](../skills/code-review/SKILL.md) — Structured code reviews prioritizing correctness, security, and maintainability.
- [`debugging-workflow`](../skills/debugging-workflow/SKILL.md) — Hypothesis-driven debugging, reproduction cases, and git bisect.
- [`unit-testing`](../skills/unit-testing/SKILL.md) — Isolated, fast, deterministic unit tests following the AAA pattern.
- [`integration-testing`](../skills/integration-testing/SKILL.md) — Multi-service testing with ephemeral databases, Testcontainers, and HTTP mocks.
- [`test-driven-development`](../skills/test-driven-development/SKILL.md) — Red-Green-Refactor cycle and incremental feature development.
- [`refactoring`](../skills/refactoring/SKILL.md) — Safe structural refactorings preserving behavior and API contracts.
- [`error-handling`](../skills/error-handling/SKILL.md) — Transient vs permanent faults, exponential backoff with jitter, and error boundaries.
- [`api-design`](../skills/api-design/SKILL.md) — RESTful conventions, resource modeling, OpenAPI, and backward compatibility.
- [`logging-observability`](../skills/logging-observability/SKILL.md) — Structured JSON logging, correlation IDs, log levels, and PII redaction.

## Category E — Documentation & Document Formats
- [`markdown-writing`](../skills/markdown-writing/SKILL.md) — CommonMark and GitHub Flavored Markdown standards and linting.
- [`technical-writing`](../skills/technical-writing/SKILL.md) — Clear technical explanations, active voice, and procedural guides.
- [`readme-authoring`](../skills/readme-authoring/SKILL.md) — High-impact repository READMEs with 60-second quickstarts.
- [`pdf-processing`](../skills/pdf-processing/SKILL.md) — Native text and table extraction, scanned OCR, merging, and generation.
- [`docx-processing`](../skills/docx-processing/SKILL.md) — Programmatic Microsoft Word (.docx) generation, styling, and inspection.
- [`xlsx-processing`](../skills/xlsx-processing/SKILL.md) — Programmatic Microsoft Excel (.xlsx) workbooks, formulas, and styles.
- [`pptx-processing`](../skills/pptx-processing/SKILL.md) — Widescreen 16:9 presentation generation, shapes, and speaker notes.
- [`latex-authoring`](../skills/latex-authoring/SKILL.md) — Scientific papers, mathematical typesetting, booktabs, and compilation.
- [`csv-data-processing`](../skills/csv-data-processing/SKILL.md) — RFC 4180 parsing, delimiter sniffing, streaming, and formula injection defense.
- [`sphinx-documentation`](../skills/sphinx-documentation/SKILL.md) — Sphinx sites, autodoc, toctrees, MyST, and Read the Docs hosting.
- [`diagrams-mermaid`](../skills/diagrams-mermaid/SKILL.md) — Flowcharts, sequence diagrams, state machines, and ER diagrams.

## Category F — Security, DevOps & Infrastructure
- [`secure-coding`](../skills/secure-coding/SKILL.md) — OWASP Top 10 / CWE Top 25 defenses, parameterization, and XSS/SSRF prevention.
- [`security-code-review`](../skills/security-code-review/SKILL.md) — Source-to-sink vulnerability auditing, trust boundaries, and CWE mapping.
- [`threat-modeling`](../skills/threat-modeling/SKILL.md) — Architectural STRIDE threat modeling and mitigation prioritization.
- [`secrets-management`](../skills/secrets-management/SKILL.md) — Zero-knowledge repository hygiene, Gitleaks, and secret rotation.
- [`docker-development`](../skills/docker-development/SKILL.md) — Multi-stage Dockerfiles, layer caching, non-root users, and Docker Compose.
- [`container-security`](../skills/container-security/SKILL.md) — Distroless images, capability dropping, read-only roots, and Trivy scanning.
- [`ci-github-actions`](../skills/ci-github-actions/SKILL.md) — Least-privilege workflows, action commit pinning, and OIDC authentication.
- [`dependency-management`](../skills/dependency-management/SKILL.md) — Lockfiles, SBOM generation, dependency audits, and automated updates.
- [`linux-hardening`](../skills/linux-hardening/SKILL.md) — SSH hardening, UFW firewall, systemd sandboxing, and CIS baselines.

## Category G — AI Agents & Skill Infrastructure
- [`agent-skill-authoring`](../skills/agent-skill-authoring/SKILL.md) — Meta-skill for designing, structuring, and validating new Agent Skills.
- [`skill-security-audit`](../skills/skill-security-audit/SKILL.md) — Security auditing of third-party skills for prompt injection and exfiltration.
- [`mcp-server-development`](../skills/mcp-server-development/SKILL.md) — Model Context Protocol servers, tools, resources, stdio/SSE, and schema validation.
