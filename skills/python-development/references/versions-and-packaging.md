# Python Versions, pyproject.toml, uv, Dependency Groups

Checked October 2026 against devguide.python.org/versions, docs.python.org/3.15/whatsnew, packaging.python.org (dependency groups), and PyPI metadata.

## Supported versions (decision input)

| Version | Status (Oct 2026) | End of life |
| :--- | :--- | :--- |
| 3.15 | released 2026-10-09 | 2031-10 |
| 3.14 | bugfix | 2030-10 |
| 3.13 | security | 2029-10 |
| 3.12 | security | 2028-10 |
| 3.11 | security | 2027-10 |
| 3.10 | end of life 2026-10-01 | - |

Rule: set the floor to the oldest version still receiving security fixes that your users need; libraries usually support several versions, applications pin one. Do not add a floor lower than a supported version without a reason.

## Notable features by version (use only if your floor allows)

- 3.11: `asyncio.TaskGroup`, `asyncio.timeout`, `ExceptionGroup`/`except*`, `tomllib`, `datetime.UTC`.
- 3.12: PEP 695 generics and `type` statement; f-string grammar relaxed.
- 3.13: new interactive REPL; experimental free-threaded build and JIT.
- 3.14: lazily evaluated annotations (PEP 649/749); template strings (PEP 750); free-threaded build officially supported (PEP 779); `compression.zstd`; multiple interpreters in the stdlib (`concurrent.interpreters`).
- 3.15: explicit lazy imports (PEP 810, `lazy` keyword), `frozendict`, `sentinel`, unpacking in comprehensions (PEP 798), UTF-8 default encoding (PEP 686; set `PYTHONUTF8=0` to restore old behavior), `profiling` package; `profile` module deprecated.

Behavior-changing defaults deserve a test run on the new version before raising the floor: encoding defaults, annotation evaluation, removed deprecated APIs.

## pyproject.toml skeleton (PEP 621 metadata, PEP 639 license, PEP 735 groups)

```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "my-project"
version = "0.1.0"
description = "One-line description"
readme = "README.md"
requires-python = ">=3.11"
license = "MIT"                 # SPDX expression (PEP 639)
license-files = ["LICENSE"]
dependencies = ["httpx>=0.27"]

[project.optional-dependencies]  # extras: part of published metadata
yaml = ["pyyaml>=6"]

[dependency-groups]              # PEP 735: dev-only, not published
dev = ["pytest>=8", "ruff", "mypy", { include-group = "docs" }]
docs = ["sphinx"]
```

- `[project.optional-dependencies]` (extras) ship with the package; `[dependency-groups]` do not. Do not give a group the same name as an extra.
- The `license = "MIT"` SPDX string form needs a build backend that supports PEP 639; older backends expect the table form. Check the backend's docs.
- Choose the build backend deliberately (hatchling, setuptools, flit-core, uv_build, others); the table above is one valid example.

## uv workflow (uv 0.x; check `uv --version` and docs for flags)

```bash
uv init --package my-project      # scaffold with src layout
uv add httpx                      # runtime dependency, updates pyproject.toml and uv.lock
uv add --dev pytest ruff mypy     # adds to the dev dependency group
uv sync                           # create/refresh .venv from uv.lock (dev group included by default)
uv run pytest                     # run inside the project environment
uv lock --upgrade-package httpx   # targeted upgrade
```

Commit `uv.lock` for applications. Run `uv sync --locked` (or `--frozen`) in CI so the lock file is not silently rewritten. pip can install groups with `pip install --group dev` on recent pip versions (pip 25.1+; verify with `pip --version`).

## Common version and packaging pitfalls

| Symptom | Cause | Fix |
| :--- | :--- | :--- |
| `ModuleNotFoundError` for your own package in tests | Importing from a flat layout without install | Use src layout and `uv sync` / `pip install -e .`; do not hack `sys.path` |
| Works locally, fails in CI on older Python | Using newer syntax than `requires-python` | Run CI on the floor version; set Ruff `target-version` to the floor |
| Type checker accepts code that fails at runtime on floor | Checker `python_version` higher than floor | Set it to the floor |
| Different results between machines | No lock file | Commit a lock file for applications |
| Deprecation warnings become errors after upgrade | Removed APIs | Run tests with `-W error::DeprecationWarning` before upgrading |
| Garbled text on Windows or CI | Implicit locale encoding before 3.15 | Always pass `encoding="utf-8"` |
