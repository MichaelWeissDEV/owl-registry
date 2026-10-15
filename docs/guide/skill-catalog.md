# OWL Registry Skill Catalog

This editorial catalog provides an overview of the curated skills available in the OWL Registry organized by technical domain.

For the auto-generated, machine-readable index with exact commit revisions, hashes, and timestamps, see [`INDEX.md`](https://github.com/MichaelWeissDEV/owl-registry/blob/main/INDEX.md) and [`index.json`](https://github.com/MichaelWeissDEV/owl-registry/blob/main/index.json).

---

## Category A — Git, Versioning and Releases
- [`conventional-commits`](https://github.com/MichaelWeissDEV/owl-registry/blob/main/skills/conventional-commits/SKILL.md) — Conventional Commits 1.0.0 specification and commit message authoring.
- [`git-workflow`](https://github.com/MichaelWeissDEV/owl-registry/blob/main/skills/git-workflow/SKILL.md) — Git status, diff inspection, staging boundaries, and clean commits.
- [`git-branching-worktrees`](https://github.com/MichaelWeissDEV/owl-registry/blob/main/skills/git-branching-worktrees/SKILL.md) — Feature branches, branch lifecycles, and isolated Git worktrees.
- [`git-merge-conflicts`](https://github.com/MichaelWeissDEV/owl-registry/blob/main/skills/git-merge-conflicts/SKILL.md) — Three-way merge conflict detection and safe resolution without data loss.
- [`semantic-versioning`](https://github.com/MichaelWeissDEV/owl-registry/blob/main/skills/semantic-versioning/SKILL.md) — SemVer 2.0.0, evaluating breaking changes and version bump rules.
- [`changelog-writing`](https://github.com/MichaelWeissDEV/owl-registry/blob/main/skills/changelog-writing/SKILL.md) — Keep a Changelog 1.1.0 conventions and release notes curation.
- [`release-engineering`](https://github.com/MichaelWeissDEV/owl-registry/blob/main/skills/release-engineering/SKILL.md) — Pre-release verification checklists, artifact validation, and rollbacks.
- [`github-issues-prs`](https://github.com/MichaelWeissDEV/owl-registry/blob/main/skills/github-issues-prs/SKILL.md) — Reproducible bug reports, PR descriptions, and code review discussions.

## Category B — Operating Systems & Shell
- [`linux-cli`](https://github.com/MichaelWeissDEV/owl-registry/blob/main/skills/linux-cli/SKILL.md) — GNU/Linux pipes, redirection, text processing (grep, sed, awk), and processes.
- [`bash-scripting`](https://github.com/MichaelWeissDEV/owl-registry/blob/main/skills/bash-scripting/SKILL.md) — Defensive Bash 4+ scripts with strict error modes, traps, and shellcheck.
- [`linux-filesystems`](https://github.com/MichaelWeissDEV/owl-registry/blob/main/skills/linux-filesystems/SKILL.md) — FHS hierarchy, ext4/XFS, inodes, hardlinks, symlinks, and mounts.
- [`linux-permissions`](https://github.com/MichaelWeissDEV/owl-registry/blob/main/skills/linux-permissions/SKILL.md) — POSIX permissions, SUID/SGID/Sticky bits, ACLs, and capabilities.
- [`linux-processes-systemd`](https://github.com/MichaelWeissDEV/owl-registry/blob/main/skills/linux-processes-systemd/SKILL.md) — Processes, systemd services, timers, journald, and cgroup limits.
- [`linux-networking`](https://github.com/MichaelWeissDEV/owl-registry/blob/main/skills/linux-networking/SKILL.md) — IP routing, DNS, sockets (ss), curl diagnostics, and firewalls.
- [`linux-troubleshooting`](https://github.com/MichaelWeissDEV/owl-registry/blob/main/skills/linux-troubleshooting/SKILL.md) — Systematic diagnosis of OOM crashes, disk exhaustion, high load, and services.
- [`macos-cli`](https://github.com/MichaelWeissDEV/owl-registry/blob/main/skills/macos-cli/SKILL.md) — macOS Darwin/BSD toolchain differences, Homebrew, launchd, and Gatekeeper.

## Category C — Programming Languages & Frameworks
- [`python-development`](https://github.com/MichaelWeissDEV/owl-registry/blob/main/skills/python-development/SKILL.md) — Idiomatic Python 3.10+, PEP 8/257, type hints, dataclasses, and asyncio.
- [`python-packaging`](https://github.com/MichaelWeissDEV/owl-registry/blob/main/skills/python-packaging/SKILL.md) — pyproject.toml, wheels, sdists, uv, build backends, and publishing.
- [`rust-development`](https://github.com/MichaelWeissDEV/owl-registry/blob/main/skills/rust-development/SKILL.md) — Ownership, borrowing, lifetimes, Result/Option, traits, and safe Rust.
- [`rust-cargo`](https://github.com/MichaelWeissDEV/owl-registry/blob/main/skills/rust-cargo/SKILL.md) — Multi-crate Cargo workspaces, additive features, dependencies, and publishing.
- [`c-development`](https://github.com/MichaelWeissDEV/owl-registry/blob/main/skills/c-development/SKILL.md) — C11/C17 memory safety, pointers, buffer bounds, UB prevention, and sanitizers.
- [`cpp-development`](https://github.com/MichaelWeissDEV/owl-registry/blob/main/skills/cpp-development/SKILL.md) — Modern C++ (C++17/20/23), RAII, smart pointers, Rule of Zero, and CMake.
- [`go-development`](https://github.com/MichaelWeissDEV/owl-registry/blob/main/skills/go-development/SKILL.md) — Go modules, consumer interfaces, error wrapping, goroutines, and context.
- [`javascript-development`](https://github.com/MichaelWeissDEV/owl-registry/blob/main/skills/javascript-development/SKILL.md) — Modern ECMAScript (ES2022+), ES Modules, Promises, async/await, and event loop.
- [`typescript-development`](https://github.com/MichaelWeissDEV/owl-registry/blob/main/skills/typescript-development/SKILL.md) — Strict TypeScript, discriminated unions, type narrowing, and tsconfig.
- [`nodejs-development`](https://github.com/MichaelWeissDEV/owl-registry/blob/main/skills/nodejs-development/SKILL.md) — Node.js 18+ runtime, stream pipelines, graceful shutdown, and CLI tools.
- [`java-development`](https://github.com/MichaelWeissDEV/owl-registry/blob/main/skills/java-development/SKILL.md) — Modern Java 17/21 LTS, Records, pattern matching, sealed classes, and JUnit 5.
- [`kotlin-development`](https://github.com/MichaelWeissDEV/owl-registry/blob/main/skills/kotlin-development/SKILL.md) — Null safety, data classes, sealed interfaces, coroutines, and Flow.
- [`swift-development`](https://github.com/MichaelWeissDEV/owl-registry/blob/main/skills/swift-development/SKILL.md) — Swift API Design Guidelines, value types, actors, Swift Concurrency, and SPM.
- [`sql-development`](https://github.com/MichaelWeissDEV/owl-registry/blob/main/skills/sql-development/SKILL.md) — Relational SQL, JOIN semantics, CTEs, constraints, and ACID transactions.
- [`postgresql-development`](https://github.com/MichaelWeissDEV/owl-registry/blob/main/skills/postgresql-development/SKILL.md) — JSONB, GIN indexes, EXPLAIN ANALYZE, zero-downtime migrations, and RLS.
- [`mongodb-development`](https://github.com/MichaelWeissDEV/owl-registry/blob/main/skills/mongodb-development/SKILL.md) — Document modeling, compound indexes (ESR rule), aggregations, and ACID transactions.
- [`redis-caching`](https://github.com/MichaelWeissDEV/owl-registry/blob/main/skills/redis-caching/SKILL.md) — In-memory caching, TTL strategies, Redlock distributed locking, and stampede mitigation.
- [`elasticsearch-search`](https://github.com/MichaelWeissDEV/owl-registry/blob/main/skills/elasticsearch-search/SKILL.md) — Search indices, mappings, text analyzers, Query DSL, aggregations, and ILM.
- [`kafka-streaming`](https://github.com/MichaelWeissDEV/owl-registry/blob/main/skills/kafka-streaming/SKILL.md) — Distributed event streaming, partition ordering, consumer groups, and exact-once semantics.
- [`graphql-development`](https://github.com/MichaelWeissDEV/owl-registry/blob/main/skills/graphql-development/SKILL.md) — GraphQL SDL schemas, resolvers, DataLoader N+1 mitigation, and cursor pagination.
- [`grpc-protobuf`](https://github.com/MichaelWeissDEV/owl-registry/blob/main/skills/grpc-protobuf/SKILL.md) — Protocol Buffers v3, streaming RPCs, deadlines, backward compatibility, and buf linting.
- [`web-html-css`](https://github.com/MichaelWeissDEV/owl-registry/blob/main/skills/web-html-css/SKILL.md) — Semantic HTML5, CSS Grid, Flexbox, custom properties, and WCAG AA accessibility.

## Category D — Code Quality & Engineering Methods
- [`code-comments`](https://github.com/MichaelWeissDEV/owl-registry/blob/main/skills/code-comments/SKILL.md) — Multi-language guide for meaningful comments and docstrings.
- [`code-review`](https://github.com/MichaelWeissDEV/owl-registry/blob/main/skills/code-review/SKILL.md) — Structured code reviews prioritizing correctness, security, and maintainability.
- [`debugging-workflow`](https://github.com/MichaelWeissDEV/owl-registry/blob/main/skills/debugging-workflow/SKILL.md) — Hypothesis-driven debugging, reproduction cases, and git bisect.
- [`unit-testing`](https://github.com/MichaelWeissDEV/owl-registry/blob/main/skills/unit-testing/SKILL.md) — Isolated, fast, deterministic unit tests following the AAA pattern.
- [`integration-testing`](https://github.com/MichaelWeissDEV/owl-registry/blob/main/skills/integration-testing/SKILL.md) — Multi-service testing with ephemeral databases, Testcontainers, and HTTP mocks.
- [`test-driven-development`](https://github.com/MichaelWeissDEV/owl-registry/blob/main/skills/test-driven-development/SKILL.md) — Red-Green-Refactor cycle and incremental feature development.
- [`refactoring`](https://github.com/MichaelWeissDEV/owl-registry/blob/main/skills/refactoring/SKILL.md) — Safe structural refactorings preserving behavior and API contracts.
- [`error-handling`](https://github.com/MichaelWeissDEV/owl-registry/blob/main/skills/error-handling/SKILL.md) — Transient vs permanent faults, exponential backoff with jitter, and error boundaries.
- [`api-design`](https://github.com/MichaelWeissDEV/owl-registry/blob/main/skills/api-design/SKILL.md) — RESTful conventions, resource modeling, OpenAPI, and backward compatibility.
- [`system-architecture-design`](https://github.com/MichaelWeissDEV/owl-registry/blob/main/skills/system-architecture-design/SKILL.md) — Architecture Decision Records (ADRs), C4 models, DDD bounded contexts, and scalability.
- [`performance-profiling`](https://github.com/MichaelWeissDEV/owl-registry/blob/main/skills/performance-profiling/SKILL.md) — CPU profiling, flamegraphs, memory heap analysis, pprof, py-spy, and latency percentiles.
- [`playwright-testing`](https://github.com/MichaelWeissDEV/owl-registry/blob/main/skills/playwright-testing/SKILL.md) — Page Object Model, resilient locators, auto-waiting, trace viewers, and end-to-end tests.
- [`logging-observability`](https://github.com/MichaelWeissDEV/owl-registry/blob/main/skills/logging-observability/SKILL.md) — Structured JSON logging, correlation IDs, log levels, and PII redaction.

## Category E — Documentation & Document Formats
- [`markdown-writing`](https://github.com/MichaelWeissDEV/owl-registry/blob/main/skills/markdown-writing/SKILL.md) — CommonMark and GitHub Flavored Markdown standards and linting.
- [`technical-writing`](https://github.com/MichaelWeissDEV/owl-registry/blob/main/skills/technical-writing/SKILL.md) — Clear technical explanations, active voice, and procedural guides.
- [`readme-authoring`](https://github.com/MichaelWeissDEV/owl-registry/blob/main/skills/readme-authoring/SKILL.md) — High-impact repository READMEs with 60-second quickstarts.
- [`pdf-processing`](https://github.com/MichaelWeissDEV/owl-registry/blob/main/skills/pdf-processing/SKILL.md) — Native text and table extraction, scanned OCR, merging, and generation.
- [`docx-processing`](https://github.com/MichaelWeissDEV/owl-registry/blob/main/skills/docx-processing/SKILL.md) — Programmatic Microsoft Word (.docx) generation, styling, and inspection.
- [`xlsx-processing`](https://github.com/MichaelWeissDEV/owl-registry/blob/main/skills/xlsx-processing/SKILL.md) — Programmatic Microsoft Excel (.xlsx) workbooks, formulas, and styles.
- [`pptx-processing`](https://github.com/MichaelWeissDEV/owl-registry/blob/main/skills/pptx-processing/SKILL.md) — Widescreen 16:9 presentation generation, shapes, and speaker notes.
- [`latex-authoring`](https://github.com/MichaelWeissDEV/owl-registry/blob/main/skills/latex-authoring/SKILL.md) — Scientific papers, mathematical typesetting, booktabs, and compilation.
- [`csv-data-processing`](https://github.com/MichaelWeissDEV/owl-registry/blob/main/skills/csv-data-processing/SKILL.md) — RFC 4180 parsing, delimiter sniffing, streaming, and formula injection defense.
- [`sphinx-documentation`](https://github.com/MichaelWeissDEV/owl-registry/blob/main/skills/sphinx-documentation/SKILL.md) — Sphinx sites, autodoc, toctrees, MyST, and Read the Docs hosting.
- [`diagrams-mermaid`](https://github.com/MichaelWeissDEV/owl-registry/blob/main/skills/diagrams-mermaid/SKILL.md) — Flowcharts, sequence diagrams, state machines, and ER diagrams.

## Category F — Security, DevOps & Infrastructure
- [`secure-coding`](https://github.com/MichaelWeissDEV/owl-registry/blob/main/skills/secure-coding/SKILL.md) — OWASP Top 10 / CWE Top 25 defenses, parameterization, and XSS/SSRF prevention.
- [`security-code-review`](https://github.com/MichaelWeissDEV/owl-registry/blob/main/skills/security-code-review/SKILL.md) — Source-to-sink vulnerability auditing, trust boundaries, and CWE mapping.
- [`threat-modeling`](https://github.com/MichaelWeissDEV/owl-registry/blob/main/skills/threat-modeling/SKILL.md) — Architectural STRIDE threat modeling and mitigation prioritization.
- [`secrets-management`](https://github.com/MichaelWeissDEV/owl-registry/blob/main/skills/secrets-management/SKILL.md) — Zero-knowledge repository hygiene, Gitleaks, and secret rotation.
- [`oauth-jwt-auth`](https://github.com/MichaelWeissDEV/owl-registry/blob/main/skills/oauth-jwt-auth/SKILL.md) — OAuth 2.0 / OIDC flows, PKCE, JWKS signature validation, and secure cookie storage.
- [`docker-development`](https://github.com/MichaelWeissDEV/owl-registry/blob/main/skills/docker-development/SKILL.md) — Multi-stage Dockerfiles, layer caching, non-root users, and Docker Compose.
- [`container-security`](https://github.com/MichaelWeissDEV/owl-registry/blob/main/skills/container-security/SKILL.md) — Distroless images, capability dropping, read-only roots, and Trivy scanning.
- [`kubernetes-manifests`](https://github.com/MichaelWeissDEV/owl-registry/blob/main/skills/kubernetes-manifests/SKILL.md) — Hardened Kubernetes resource manifests, NetworkPolicies, Helm charts, and kubeconform.
- [`terraform-iac`](https://github.com/MichaelWeissDEV/owl-registry/blob/main/skills/terraform-iac/SKILL.md) — Reusable modules, remote state locking with S3/DynamoDB, two-phase plan/apply, and tflint.
- [`ansible-automation`](https://github.com/MichaelWeissDEV/owl-registry/blob/main/skills/ansible-automation/SKILL.md) — Idempotent playbooks, roles, handlers, Ansible Vault encryption, and error recovery.
- [`aws-cloud-architecture`](https://github.com/MichaelWeissDEV/owl-registry/blob/main/skills/aws-cloud-architecture/SKILL.md) — Multi-AZ 3-tier VPC architecture, IAM least privilege, S3 hardening, and Well-Architected baselines.
- [`ci-github-actions`](https://github.com/MichaelWeissDEV/owl-registry/blob/main/skills/ci-github-actions/SKILL.md) — Least-privilege workflows, action commit pinning, and OIDC authentication.
- [`github-actions-security`](https://github.com/MichaelWeissDEV/owl-registry/blob/main/skills/github-actions-security/SKILL.md) — Action SHA pinning, script injection defense, OIDC token minting, and zizmor auditing.
- [`dependency-management`](https://github.com/MichaelWeissDEV/owl-registry/blob/main/skills/dependency-management/SKILL.md) — Lockfiles, SBOM generation, dependency audits, and automated updates.
- [`linux-hardening`](https://github.com/MichaelWeissDEV/owl-registry/blob/main/skills/linux-hardening/SKILL.md) — SSH hardening, UFW firewall, systemd sandboxing, and CIS baselines.

## Category G — AI Agents & Skill Infrastructure
- [`agent-skill-authoring`](https://github.com/MichaelWeissDEV/owl-registry/blob/main/skills/agent-skill-authoring/SKILL.md) — Meta-skill for designing, structuring, and validating new Agent Skills.
- [`skill-security-audit`](https://github.com/MichaelWeissDEV/owl-registry/blob/main/skills/skill-security-audit/SKILL.md) — Security auditing of third-party skills for prompt injection and exfiltration.
- [`mcp-server-development`](https://github.com/MichaelWeissDEV/owl-registry/blob/main/skills/mcp-server-development/SKILL.md) — Model Context Protocol servers, tools, resources, stdio/SSE, and schema validation.
