# Sources and provenance: performance-regression-testing

Consulted 2026-10-15 (read-only):

- hyperfine README, https://github.com/sharkdp/hyperfine/blob/master/README.md : `--warmup`, `--runs` (default at least 10 runs), `--prepare`, `--setup`, `-N`/no-shell behavior, parameter scan, multi-command comparison with first as reference, CSV/markdown export. `--export-json`, `--min-runs` exist per author knowledge but were not on the fetched README text.
- pytest-benchmark usage, https://pytest-benchmark.readthedocs.io/en/latest/usage.html : `--benchmark-save`, `--benchmark-autosave`, `--benchmark-compare`, `--benchmark-compare-fail`, `--benchmark-disable`, `--benchmark-only`, `--benchmark-min-rounds` (default 5), `--benchmark-storage`, `benchmark.pedantic`. Verified by running pytest-benchmark 5.3.0 locally.
- Criterion.rs CLI options, https://bheisler.github.io/criterion.rs/book/user_guide/command_line_options.html : `--save-baseline`, `--baseline`, `--noplot`. Significance level, noise threshold, sample-size flags were not on the page; the skill defers to `cargo bench -- --help`.
- GitHub Actions workflow syntax is covered by the sibling skill and cross-platform-testing sources.

Local experiments: pytest-benchmark 5.3.0 save/compare/compare-fail flow was exercised on a micro-benchmark (see SKILL.md section 4).

Provenance: all text is original; no external skill repositories were consulted, so no license decision was needed.
