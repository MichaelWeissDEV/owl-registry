---
name: python-development
description: >
  Develop, review, test, and refactor idiomatic Python applications following
  PEP 8, strict type hints, and modern ecosystem standards. Use when writing
  Python modules, designing clean object and functional architectures, configuring
  Ruff/Mypy/pytest, implementing Asyncio, structuring pyproject.toml and uv projects,
  or improving maintainability and performance. Do not use for data-science notebooks
  workflows, Django/Flask framework specifics, or packaging/publishing to PyPI release
  operations that need account credentials.
compatibility: >
  Agent Skills-compatible coding agents working on Python 3.11+ codebases (3.10
  reached end of life on 2026-10-01; 3.9 earlier). Ruff, mypy (or another type
  checker), and pytest are needed for executable checks. Version facts checked on
  devguide.python.org and docs.python.org in October 2026.
metadata:
  author: michaelweissdev
  version: "1.1.0"
  tags: "python, ruff, mypy, pytest, typing, asyncio, best-practices"
  topics: "programming-languages, software-development"
---

# Idiomatic Python Development

Write maintainable, robust, and performant Python code following modern standards (Python 3.11+; check the supported-versions table before choosing a floor). Emphasize explicit typing, structured error handling, composition over complex inheritance, and clean boundary separation.

Detailed technical guidelines and deep dives are available in the bundled references:
- [Code Conventions & Tooling](references/conventions.md)
- [Modern Type Annotations](references/typing.md)
- [Asyncio Patterns & Pitfalls](references/asyncio-patterns.md)
- [Common Anti-Patterns](references/common-mistakes.md)
- [Versions, pyproject.toml, uv, and dependency groups](references/versions-and-packaging.md)
- [Canonical Module Template](assets/module_template.py)

---

## Core Rules

1. **Explicit is better than implicit**: Favor explicit types, clean argument signatures, and clear variable names.
2. **Never swallow exceptions silently**: Avoid bare `except:` or `except Exception: pass`. Catch specific errors and log or re-raise with `from err`.
3. **Never use mutable default arguments**: Use `None` and initialize inside the function (`arg: list[str] | None = None`).
4. **Enforce static types at module boundaries**: Annotate all public functions, classes, and exported constants.
5. **Use context managers for resources**: Always manage files, database connections, and locks with `with` or `async with`.
6. **Validate with standard tooling**: Verify changes with Ruff (lint/format), Mypy (strict typing), and pytest.

---

## 1. Project and Module Architecture

Adopt modern standard layouts (src-layout):

```text
my-project/
├── pyproject.toml
├── src/
│   └── my_project/
│       ├── __init__.py
│       ├── core.py
│       ├── py.typed          # Signals inline type annotations
│       └── utils.py
└── tests/
    ├── conftest.py
    └── test_core.py
```

### Clean Module Imports
Sort imports logically into three groups (enforced by Ruff/isort):
```python
# 1. Standard library
import logging
from collections.abc import Sequence
from pathlib import Path

# 2. Third-party dependencies
import pydantic
import httpx

# 3. Local application imports
from my_project.core import Engine
from my_project.models import Config
```

---

## 2. Idiomatic Class Design: Dataclasses & Protocols

### Modern Data Containers
Use `dataclasses` with `slots=True` and `frozen=True` where immutability is desired:

```python
from dataclasses import dataclass, field
from datetime import datetime, timezone

@dataclass(slots=True, frozen=True)
class EventRecord:
    event_id: str
    payload: dict[str, str]
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
```

### Decoupling with `typing.Protocol` (Structural Subtyping)
Avoid deep inheritance hierarchies. Use structural subtyping (duck typing with static verification):

```python
from typing import Protocol, runtime_checkable

@runtime_checkable
class Notifier(Protocol):
    def send(self, recipient: str, message: str) -> bool:
        """Send notification. Return True on success."""
        ...

# Any class implementing `send(...)` matches Notifier automatically
class SlackClient:
    def send(self, recipient: str, message: str) -> bool:
        # Implementation...
        return True
```

---

## 3. Exception Handling at Boundaries

1. Define a clear hierarchy of project-specific domain exceptions.
2. Chain underlying exceptions to preserve stack traces (`raise CustomError(...) from original_err`).

```python
class ProjectError(Exception):
    """Base exception for all errors in this package."""

class ConfigurationError(ProjectError):
    """Raised when configuration is invalid or missing."""

class NetworkTimeoutError(ProjectError):
    """Raised when an external API call times out."""

def fetch_data(url: str, timeout: float = 5.0) -> bytes:
    try:
        response = httpx.get(url, timeout=timeout)
        response.raise_for_status()
        return response.content
    except httpx.TimeoutException as exc:
        raise NetworkTimeoutError(f"Request to {url} timed out after {timeout}s") from exc
    except httpx.HTTPStatusError as exc:
        raise ProjectError(f"HTTP error {exc.response.status_code} received from {url}") from exc
```

---

## 4. Common Anti-Patterns

| Anti-Pattern | Bug / Risk | Correct Idiom |
| :--- | :--- | :--- |
| `def append(item, seq=[])` | Sequence is shared across all function calls | `def append(item, seq=None): if seq is None: seq = []` |
| `except Exception: pass` | Hides real bugs and failures (bare `except:` additionally catches `KeyboardInterrupt` and `SystemExit`) | Catch specific errors: `except (KeyError, ValueError):` |
| `type(x) == int` | Breaks with subclasses | Use `isinstance(x, int)` |
| `open('file.txt').read()` | File descriptor leak on uncollected garbage | Use `with open('file.txt', 'r', encoding='utf-8') as f:` |
| String concatenation in loops | O(N^2) memory allocation | Use `''.join(chunks)` or `io.StringIO` |

---

## 5. Standard Tooling Commands

```bash
# Format and lint code with Ruff
ruff format .
ruff check . --fix

# Static type check
mypy src/ tests/

# Run test suite with coverage
pytest --cov=my_project tests/
```

---

## 6. Security Defaults

- Never `eval`/`exec` untrusted text; never `pickle.load` or `yaml.load` untrusted data (use `yaml.safe_load`, JSON).
- `subprocess.run([...], check=True)` with an argument list; avoid `shell=True` with interpolated input.
- Give every network call a timeout (`httpx`/`requests` do not time out by default in requests).
- Use `secrets` for tokens, `hmac.compare_digest` for secret comparison, `pathlib` plus containment checks for user paths, parameterized SQL.
- Pin and hash dependencies for deployable apps (lock file); install from trusted indexes only.

## 7. Verification Checklist

- [ ] All public functions, arguments, and return types are annotated.
- [ ] No bare `except:` or broad `except Exception:` without re-raise/logging.
- [ ] Context managers are used for file, connection, and lock lifecycles.
- [ ] `ruff check .` and `ruff format --check .` exit with 0 errors.
- [ ] `mypy` passes with 0 type errors under `--strict`.
- [ ] Test coverage covers both happy path and failure/boundary branches.
