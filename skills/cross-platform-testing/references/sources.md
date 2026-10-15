# Sources and provenance: cross-platform-testing

Consulted 2026-10-15 (read-only):

- actions/runner-images README, https://github.com/actions/runner-images/blob/main/README.md : runner labels and architectures (ubuntu-latest = 24.04 x64, ubuntu-24.04-arm, windows-latest = 2025, windows-11-arm, macos-latest = macOS 26 arm64, macos-15, macos-15-intel, macos-26-intel); `-latest` migrates gradually over 1 to 2 months; deprecated images noted.
- GitHub Docs, using a matrix for your jobs, https://docs.github.com/en/actions/using-jobs/using-a-matrix-for-your-jobs : `matrix`, `include`, `exclude`, `fail-fast`, `max-parallel`, `continue-on-error: ${{ matrix.experimental }}` pattern. The 256-job matrix limit could not be confirmed from the fetched text and is not asserted.
- GitHub Docs, workflow syntax (first 100k chars only): `concurrency` with `cancel-in-progress`, `defaults.run.shell` defaults (bash on Linux/macOS, pwsh on Windows).
- actions/setup-python README, https://github.com/actions/setup-python/blob/main/README.md : `@v7` in examples, `architecture` input, `cache: 'pip'`, `3.13t` free-threaded notation. `allow-prereleases` not described on the fetched page.
- `actions/checkout@v4` usage, Git Bash availability on Windows runners, and billing multipliers are from author knowledge, not fetched; check current docs. Python version status (3.14 stable, 3.15 pre-release, 3.10 EOL) is as of 2026-10-15 from author knowledge; re-check python.org.

Local checks: the portable pytest example passed locally (macOS, pytest 9.1.1); the workflow YAML parsed with PyYAML. No CI execution.

Provenance: all text is original; no external skill repositories were consulted, so no license decision was needed.
