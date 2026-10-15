# Modern Python Type Annotations (Python 3.10+; 3.11+ recommended)

Modern Python features clean, first-class type expressions without needing verbose legacy imports from `typing`.

## 1. Built-in Generic Types (PEP 585) & Union Operators (PEP 604)

Use standard built-ins instead of uppercase equivalents:
- Prefer `list[str]` over `typing.List[str]`.
- Prefer `dict[str, int]` over `typing.Dict[str, int]`.
- Prefer `set[int]` over `typing.Set[int]`.
- Prefer `tuple[int, ...]` over `typing.Tuple[int, ...]`.
- Prefer `str | None` over `typing.Optional[str]`.
- Prefer `int | float` over `typing.Union[int, float]`.

---

## 2. Generics and Type Variables

### Python 3.12+ Syntax (PEP 695)
```python
# New syntax in Python 3.12+:
def first_item[T](items: list[T]) -> T | None:
    return items[0] if items else None
```

### Python 3.10 - 3.11 Syntax
```python
from typing import TypeVar

T = TypeVar("T")

def first_item(items: list[T]) -> T | None:
    return items[0] if items else None
```

---

## 3. Abstract Collections vs Concrete Types

In function signatures, **be liberal in what you accept and conservative in what you return**:
- Accept abstract collections (`collections.abc.Sequence`, `collections.abc.Mapping`, `collections.abc.Iterable`).
- Return concrete types (`list`, `dict`, `set`) so callers know what methods are available.

```python
from collections.abc import Mapping, Sequence

def process_scores(student_scores: Mapping[str, Sequence[float]]) -> dict[str, float]:
    results: dict[str, float] = {}
    for name, scores in student_scores.items():
        results[name] = sum(scores) / len(scores) if scores else 0.0
    return results
```

---

## 4. TypedDict for Structured Dictionaries

When interfacing with JSON payloads where defining a full class is unnecessary:

```python
from typing import TypedDict, NotRequired

class UserPayload(TypedDict):
    id: int
    username: str
    email: str
    is_active: NotRequired[bool]
```

---

## 5. Type Narrowing (TypeGuard & isinstance)

```python
from typing import TypeGuard

def is_string_list(val: list[object]) -> TypeGuard[list[str]]:
    return all(isinstance(x, str) for x in val)
```

## Version notes

- 3.12: `type X = ...` statement and `def f[T](x: T)` generics (PEP 695); 3.13: TypeVar defaults (PEP 696), `warnings.deprecated` (PEP 702).
- 3.14: annotations are evaluated lazily (PEP 649/749), so forward references usually need no quotes or `from __future__ import annotations`; use `annotationlib` to inspect them. Libraries that read `__annotations__` directly (Pydantic, dataclass tools) should be on versions that support this.
- 3.15: `TypedDict` extra items (PEP 728) and TypeForm (PEP 747) are listed in the release notes; check your type checker supports them before use.
