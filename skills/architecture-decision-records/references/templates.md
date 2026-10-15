# ADR templates

Both templates below are original wordings of the well-known structures. Use the project's own template if one exists.

## Minimal (Nygard-style sections)

Michael Nygard's 2011 proposal uses these sections: Title, Context, Decision, Status, Consequences.

```markdown
# NNNN. <Decision title>

Status: Proposed | Accepted | Deprecated | Superseded by NNNN
Date: YYYY-MM-DD

## Context
<The forces at play: requirements, constraints, facts. Neutral language.>

## Decision
We will <do X> for <scope>.

## Consequences
<Resulting context: easier, harder, new risks, follow-up work, revisit triggers.>
```

## Fuller (MADR-style sections)

The MADR project (https://adr.github.io/madr/) defines a template with sections: Context and Problem Statement, Decision Drivers (optional), Considered Options, Decision Outcome (with Consequences and Confirmation), Pros and Cons of the Options (optional), More Information (optional), plus optional front matter (status, date, decision-makers, consulted, informed). MADR 4.0.0 (2024-09-17) was the latest release seen when this skill was written; check the project for newer versions.

```markdown
---
status: proposed
date: YYYY-MM-DD
decision-makers: <names/roles>
---

# <Short title: problem solved and solution chosen>

## Context and Problem Statement
<2-4 sentences or a question.>

## Decision Drivers
- <driver>

## Considered Options
- <option A>
- <option B>

## Decision Outcome
Chosen option: "<option>", because <justification tied to drivers>.

### Consequences
- Good: <...>
- Bad: <...>

### Confirmation
<How compliance or success will be checked: test, review check, metric.>

## Pros and Cons of the Options
### <option A>
- Good: <...>
- Bad: <...>

## More Information
<Links, related ADRs, revisit date.>
```

## Naming and layout

- Directory: follow the project (`docs/adr/` is common). Do not invent a second location.
- File: `NNNN-kebab-case-title.md`, zero-padded, never renumbered.
- Index: optional `README.md` listing number, title, status.

## Superseding a record

1. Create the new ADR; in its Context mention the old one and what changed.
2. In the old ADR, change only the status to `Superseded by NNNN` and add the link.
3. Do both edits in one commit.

## Reconstructing an undocumented past decision

Label it: "Reconstructed on <date> from <commit/issue/interview>". List what is known and what is unknown. Do not invent alternatives that were not discussed; write "alternatives not recorded".
