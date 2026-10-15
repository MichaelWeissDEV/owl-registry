# Run your own registry

```console
$ owl registry init ./my-registry --name my-registry
$ cd my-registry && owl registry publish ../some-skill --dir .
$ owl registry check . && owl registry index .
$ git add -A && git commit -m "feat: first skill"
```

`owl registry init` creates the layout, the CI workflow and a README. Pushing to a remote is your
decision – OWL never pushes on its own. See the
[OWL documentation](https://owl-skills.readthedocs.io/en/latest/guide/registries.html) for private registries,
settings and merging registries.
