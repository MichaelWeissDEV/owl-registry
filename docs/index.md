<p align="center"><img src="_static/owl.png" alt="OWL logo" width="160"></p>

# OWL Registry

**The default skill registry of [OWL](https://github.com/MichaelWeissDEV/OWL): 80 curated Agent Skills for AI coding assistants, in a plain git repository.**

```{admonition} Development status: Alpha
:class: warning

The registry is served by OWL, which is under active development; the registry layout and the index
format can still change. Contributions are welcome – see {doc}`guide/contributing`. The OWL command
line is documented at [owl-skills.readthedocs.io](https://owl-skills.readthedocs.io).
```

A registry is **just a git repository**: skills live under `skills/<name>/`, a CI job keeps a
machine-readable `index.json` (and a readable `INDEX.md`) up to date, and the OWL CLI reads it without
any server. Skills are passive data – nothing from a skill is ever executed during discovery,
indexing or installation.

```{mermaid}
flowchart LR
    C[contributor] -- pull request --> R[(owl-registry<br/>skills/&lt;name&gt;/SKILL.md)]
    R -- CI: owl registry check --> V{valid?}
    V -- merge --> I[CI: owl registry index<br/>index.json · INDEX.md · STATS.md]
    I --> R
    R -- owl install · owl search --> U[your agent<br/>Claude Code · OpenCode · Codex · ...]
```

::::{grid} 1 2 2 3
:gutter: 3

:::{grid-item-card} Getting started
:link: getting-started/index
:link-type: doc
Add the registry to OWL and install your first skill.
:::

:::{grid-item-card} Guide
:link: guide/index
:link-type: doc
Skill catalog, authoring guidelines and how to contribute a skill.
:::

:::{grid-item-card} Reference
:link: reference/index
:link-type: doc
The layout, `registry.json`, `index.json` and `stats.json`.
:::

:::{grid-item-card} Operations
:link: operations/index
:link-type: doc
The CI workflow, permissions and running your own registry.
:::

:::{grid-item-card} FAQ
:link: faq
:link-type: doc
Short answers to the usual questions.
:::

:::{grid-item-card} Changelog
:link: changelog
:link-type: doc
What changed in the registry.
:::
::::

```{toctree}
:maxdepth: 2
:caption: Documentation
:hidden:

getting-started/index
guide/index
reference/index
operations/index
faq
changelog
```
