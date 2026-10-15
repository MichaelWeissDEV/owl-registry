---
name: architecture-decision-records
description: >
  Create, review, and maintain Architecture Decision Records (ADRs): short, numbered,
  immutable documents capturing one significant decision with context, options,
  outcome, and consequences. Use when a technical choice is hard to reverse, has real
  alternatives, will puzzle future readers, or when setting up a docs/adr directory,
  superseding an old decision, or auditing a decision log. Covers Nygard-style and
  MADR templates, status lifecycle, and what not to record. Not for system design
  itself (see system-architecture-design) or task planning (see implementation-planning).
compatibility: >
  Any Agent Skills-compatible coding agent; plain Markdown files in a git repository.
  No tooling required.
metadata:
  author: michaelweissdev
  version: "1.0.0"
  tags: "adr, architecture, decisions, documentation, markdown, madr"
  topics: "software-development, documentation, ai-agents"
---

# Architecture Decision Records

An ADR captures **one** architecturally significant decision and the reasoning behind it, so that someone arriving later (including you in six months, or an agent with no memory) can tell *what was decided, why, and what it cost* without archaeology. The record is a log entry, not a design document.

Related skills: [system-architecture-design](../system-architecture-design/SKILL.md) (doing the design; it mentions ADRs, this skill is the full practice), [implementation-planning](../implementation-planning/SKILL.md), [technical-writing](../technical-writing/SKILL.md), [diagrams-mermaid](../diagrams-mermaid/SKILL.md), [markdown-writing](../markdown-writing/SKILL.md). Depth: [templates](references/templates.md), [scenarios](references/scenarios.md), [sources](references/sources.md).

## When to use

- A choice is costly to reverse (datastore, framework, protocol, auth model, deployment target).
- Real alternatives were considered and a reader would ask "why not X?".
- The decision constrains future work or teams.
- Setting up an ADR directory, or superseding or auditing existing records.

## When not to use

- Routine choices covered by existing conventions.
- Implementation task lists (implementation-planning) or how-to docs (technical-writing).
- Reversible, low-cost decisions where a code comment or PR description suffices.

## Non-negotiable rules

1. **One decision per record.** If you need "and also", write two ADRs.
2. **Never fabricate history.** Record only alternatives actually considered and facts you can support. If reconstructing a past decision, label it as reconstructed, state the evidence (commit, issue, person who confirmed), and mark unknowns as unknown.
3. **Do not decide for the humans.** An agent may draft a Proposed ADR and its analysis. Moving to Accepted requires the decision owner's explicit approval.
4. **Immutable once accepted.** Do not rewrite the reasoning of an accepted ADR. To change a decision, write a new ADR that supersedes the old one and update only the old one's status line and link. Fixing typos or broken links is fine.
5. **Consequences must include the downsides.** An ADR with only benefits is advocacy.
6. **No secrets or sensitive internals.** ADRs live in the repository; do not include credentials, customer data, or exploit details. Describe security decisions at the design level.
7. **Sequential, never reused numbers.** Do not renumber or delete.

## Workflow

### 1. Decide whether it deserves an ADR

Apply the "why not X?" test and the reversal-cost test. If both are low, skip.

### 2. Find the project's convention

Look for an existing directory (`docs/adr/`, `doc/adr/`, `docs/decisions/`) and template. Follow it. If none exists, propose `docs/adr/NNNN-short-title.md` with zero-padded numbers and ask before creating the directory in a repository you do not own.

```bash
ls docs/adr 2>/dev/null || ls doc/adr 2>/dev/null || ls docs/decisions 2>/dev/null
```

### 3. Gather the facts

State the problem and the forces (requirements, constraints, deadlines, team skills). List real alternatives with their honest costs. Pull evidence: benchmarks you ran, vendor limits from official docs (cite and date them), prior incidents.

### 4. Draft in the project's template

See [templates](references/templates.md) for a Nygard-style minimal form and a MADR-style fuller form. Keep it to one or two pages. Use plain language; link to deeper material rather than pasting it.

### 5. Write the decision as a sentence

"We will use X for Y." Active voice, unambiguous, with the scope. Then consequences: what becomes easier, what becomes harder, what new risks or follow-up work arise, and any condition that should trigger revisiting.

### 6. Set status and get approval

Statuses: **Proposed** while under review, **Accepted** once the decision owner agrees, **Deprecated** when no longer relevant, **Superseded by ADR-NNNN** when replaced. (Nygard's original describes proposed, accepted, deprecated, superseded.) Rejected options may be recorded as Rejected if the team uses that status.

### 7. Link and maintain

Add the ADR to an index file if the project keeps one. Reference the ADR from the code or docs it governs. When superseding, edit the old record's status and link both ways in the same change.

## Worked example

Situation: a small service needs background job processing.

```markdown
# 0007. Use PostgreSQL-backed job queue

Status: Proposed
Date: 2026-10-15

## Context
We need durable background jobs for ~50 jobs/minute. We already run
PostgreSQL; there is no message broker in production and the team of three
has not operated one. Jobs must survive restarts and be retryable.

## Considered options
1. Dedicated broker (e.g. RabbitMQ): purpose-built; adds a new service to run.
2. PostgreSQL table with row locking: no new infrastructure; throughput limited.
3. In-process queue: simplest; loses jobs on restart (fails durability).

## Decision
We will implement the queue as a PostgreSQL table, polled with
`SELECT ... FOR UPDATE SKIP LOCKED`, for the first release.

## Consequences
- Easier: no new operational surface; transactional enqueue with business writes.
- Harder: polling adds database load; throughput ceiling well below a broker.
- Revisit if sustained load exceeds ~1,000 jobs/minute or latency SLOs are missed.
```

Note the explicit revisit trigger and the rejected-option reason. The load figure is the team's own assumption, labelled as such, not a benchmark claim.

## Anti-patterns

- **Retroactive justification.** Writing the "analysis" to fit a decision already made, hiding that it was a preference.
- **Strawman alternatives.** Options listed only to be dismissed.
- **Novel-length ADR.** If it needs ten pages it is a design doc; link it.
- **Editing history.** Rewriting an accepted ADR instead of superseding it.
- **Decision by agent.** Marking Accepted without the owner's approval.
- **ADR for everything.** Noise hides the important records.
- **Missing consequences.** No downsides, no revisit condition.
- **Orphan records.** No index, no links from the code they govern.

## Verification checklist

- [ ] Exactly one decision; title names it.
- [ ] Context states forces and constraints, not just the solution.
- [ ] At least two real alternatives, honestly assessed.
- [ ] Decision stated as a clear sentence with scope.
- [ ] Consequences include downsides and a revisit trigger.
- [ ] Status is correct; Accepted only with owner approval.
- [ ] Number is next in sequence; file follows the project's naming.
- [ ] Superseded records updated and cross-linked.
- [ ] External facts cited with source and date; no secrets included.
