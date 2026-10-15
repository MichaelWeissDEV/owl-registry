# Sources and provenance: mutation-testing

Consulted 2026-10-15 (read-only):

- Stryker JS configuration, https://stryker-mutator.io/docs/stryker-js/configuration/ : `mutate`, `testRunner`, `coverageAnalysis` (perTest default), `thresholds` (80/60/null), `incremental`, `ignoreStatic`, `concurrency`, `reporters`.
- cargo-mutants, https://mutants.rs/ , /in-diff.html , /shards.html : `--in-diff`, `--shard k/n`, `--baseline=skip`, CI sharding with `fail-fast: false`, archive of `mutants.out`. `--list`, `--timeout`, `#[mutants::skip]` and outcome names come from author knowledge (home page did not list them) and should be checked with `cargo mutants --help`.
- mutmut docs, https://mutmut.readthedocs.io/en/latest/ : commands `run`, `browse`, `apply`; config in `pyproject.toml` `[tool.mutmut]` or `setup.cfg`; `also_copy`, `do_not_mutate`, `source_paths`; pragma `# pragma: no mutate`. The fetched page did not document a results/show command; the skill defers to `mutmut --help`.
- PIT Maven quickstart, https://pitest.org/quickstart/maven/ : `mutationCoverage` goal, `targetClasses`, `targetTests`, `mutationThreshold`, `withHistory`, `timeoutConstant` 4000 / `timeoutFactor` 1.25, report location.
- cosmic-ray commands (`init`, `exec`, `cr-report`) are from author knowledge, not fetched.

No mutation tool was run while producing this skill; the discount example arithmetic was checked by hand.

Provenance: all text is original; no external skill repositories were consulted, so no license decision was needed.
