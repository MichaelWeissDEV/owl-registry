# Quickstart

You need the [OWL CLI](https://owl-skills.readthedocs.io/en/latest/getting-started/installation.html).
The registry is preconfigured as `owl` on fresh installs; to add it yourself:

```console
$ owl registry add owl-registry https://github.com/MichaelWeissDEV/owl-registry.git
```

Search and discover:

```console
$ owl search python -r owl-registry          # full text
$ owl search --topic security -r owl-registry
$ owl search --tag concurrency -r owl-registry
```

Install – globally or into the current project, for your tool of choice:

```console
$ owl install python-development -r owl-registry                    # Claude Code (default)
$ owl install python-development -r owl-registry --target opencode  # OpenCode, Codex, Cursor, ...
$ owl install --all -r owl-registry                                 # everything
$ owl install rust-development -r owl-registry --project            # only this project
```

The registry is read-only for you: `owl` never writes to it. To change a skill, open a pull request
({doc}`/guide/contributing`).
