# Agent Skills Specification & OWL Standards

This document summarizes the official Agent Skills specification ([agentskills.io](https://agentskills.io/specification)) and OWL Registry extensions.

## 1. Skill Frontmatter Attributes

| Field | Required? | Max Length | Format / Description |
| :--- | :---: | :---: | :--- |
| `name` | **Yes** | 64 chars | `^[a-z0-9]+(-[a-z0-9]+)*$` |
| `description` | **Yes** | 1024 chars | Clear string detailing what the skill does and when to activate it. |
| `compatibility`| No | 500 chars | Tooling and environment requirements. |
| `metadata` | No | N/A | Key-value mapping containing `author`, `version`, `tags`, and `topics`. |

---

## 2. Taxonomy & Topics in OWL

Use standard canonical topics:
- `version-control`
- `software-development`
- `programming-languages`
- `operating-systems`
- `devtools`
- `testing`
- `documentation`
- `office`
- `databases`
- `security`
- `devops`
- `ai-agents`

Tags should represent specific search keywords (`python`, `rust`, `git`, `docker`, `pdf`, `markdown`, etc.).

---

## 3. Principles of Progressive Disclosure

- **L0 (Index/Discovery)**: The agent discovers skills via name, description, and tags. Keep descriptions high-signal so the agent selects the right skill.
- **L1 (Core Instruction)**: The agent loads `SKILL.md`. This file should provide the mental model, guardrails, and primary workflow (< 500 lines).
- **L2 (Deep Reference)**: The agent reads files in `references/` when encountering specialized sub-problems (e.g. `references/typing.md`).
- **L3 (Assets/Templates)**: Static boilerplate files in `assets/` loaded on demand.
