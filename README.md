<p align="center">
  <img src="assets/owl.png" alt="OWL" width="120">
</p>

<h1 align="center">owl-registry</h1>

<p align="center">The default OWL skill registry - curated skills that 'owl install' can fetch.</p>

<p align="center">
  <img alt="Development status: alpha" src="https://img.shields.io/badge/status-alpha-orange">
  <a href="https://github.com/MichaelWeissDEV/OWL"><img alt="Served by OWL" src="https://img.shields.io/badge/served%20by-OWL-8b5a2b"></a>
  <a href="https://github.com/MichaelWeissDEV/owl-registry/blob/main/INDEX.md"><img alt="Skills" src="https://img.shields.io/badge/dynamic/json?url=https://raw.githubusercontent.com/MichaelWeissDEV/owl-registry/main/index.json&query=%24.count&label=skills&color=blue"></a>
  <a href="https://github.com/MichaelWeissDEV/owl-registry/actions/workflows/registry.yml"><img alt="Validation" src="https://github.com/MichaelWeissDEV/owl-registry/actions/workflows/registry.yml/badge.svg"></a>
  <a href="https://github.com/MichaelWeissDEV/owl-registry"><img alt="Registry" src="https://img.shields.io/badge/registry-owl--registry-green"></a>
</p>

> **Alpha:** this registry is served by [OWL](https://github.com/MichaelWeissDEV/OWL), which is under active development; the
> registry layout and index format may still change.

A skill registry for [OWL](https://github.com/MichaelWeissDEV/OWL). Browse [`INDEX.md`](INDEX.md) for a quick overview,
[`STATS.md`](STATS.md) for statistics, or read [`index.json`](index.json) from tools.

## Use it

```console
$ owl registry add owl-registry https://github.com/MichaelWeissDEV/owl-registry.git
$ owl search <words> -r owl-registry
$ owl install <skill> -r owl-registry                    # one skill
$ owl install --all -r owl-registry                      # everything
$ owl install --all -r owl-registry --target opencode    # for OpenCode instead of Claude Code
```

## Contribute

Add a skill directory `skills/<name>/` with a `SKILL.md` (`name` and `description` frontmatter) and
open a pull request - see [`CONTRIBUTING.md`](CONTRIBUTING.md). CI validates every pull request;
after a merge CI regenerates `index.json`, `stats.json`, `INDEX.md` and `STATS.md`. Never edit
the generated files by hand.

Locally: `owl registry publish ./my-skill --dir .` copies a skill in and updates the index.
