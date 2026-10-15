# owl-registry

The default OWL skill registry - curated skills that 'owl install' can fetch.

A skill registry for [OWL](https://github.com/MichaelWeissDEV/OWL). Browse [`INDEX.md`](INDEX.md) for a quick overview or read
[`index.json`](index.json) from tools.

## Use it

```console
$ owl registry add owl-registry https://github.com/MichaelWeissDEV/owl-registry.git
$ owl search <words> -r owl-registry
$ owl install <author>/<skill> -r owl-registry          # one skill
$ owl install --all -r owl-registry                     # everything
$ owl install --all -r owl-registry --target opencode   # for OpenCode instead of Claude Code
```

## Contribute

Add a skill directory below `skills/<author>/<name>/` (`SKILL.md` with `name` and `description`
frontmatter) and open a pull request. CI validates it; after the merge CI regenerates
`index.json` and `INDEX.md` - never edit those by hand.

Locally: `owl registry publish ./my-skill --dir .` copies a skill in and updates the index.
