# Repository layout

```text
registry.json          format, name, description
skills/<name>/         one directory per skill (SKILL.md, skill.json, bundled files)
index.json  INDEX.md   generated: machine and human readable index
stats.json  STATS.md   generated: totals and breakdowns
docs/                  this documentation
.github/workflows/     registry.yml: validation and index update
```

`registry.json`:

```json
{
  "format": 1,
  "name": "owl-registry",
  "description": "The default OWL skill registry - curated skills that 'owl install' can fetch."
}
```

`format` is the registry layout version. Registries created by older OWL versions with
`skills/<author>/<name>/` are still readable; `owl registry migrate` converts them.
