# Python Conventions, Standards & Tooling

## PEP 8 & PEP 257 Standards

### Naming Conventions
- **Modules and Packages**: short, all-lowercase names, underscores allowed if necessary (`data_parser.py`).
- **Classes**: PascalCase (`HttpResponse`, `TokenValidator`).
- **Functions and Methods**: lowercase with words separated by underscores (`calculate_sha256()`).
- **Variables and Parameters**: lowercase with underscores (`timeout_seconds`).
- **Constants**: all-uppercase with underscores (`DEFAULT_RETRY_COUNT = 3`).
- **Private/Internal**: prefix with single underscore (`_internal_buffer`).

### Docstrings (PEP 257)
Docstrings use triple double-quotes (`"""`). The summary line is concise, begins with a capital letter, ends with a period, and uses imperative mood ("Compute the hash", not "Computes the hash").

```python
def parse_record(raw_line: str, delimiter: str = ",") -> dict[str, str]:
    """Parse a single delimited text line into a key-value record.

    Args:
        raw_line: Raw input string from data stream.
        delimiter: Separator character, defaults to comma.

    Returns:
        Mapping of parsed header keys to string values.

    Raises:
        ValueError: If line is empty or improperly formatted.
    """
```

---

## Tooling Configuration

### Ruff (`pyproject.toml`)
Ruff combines formatting and high-performance linting:

```toml
[tool.ruff]
line-length = 88
target-version = "py310"

[tool.ruff.lint]
select = [
    "E",   # pycodestyle errors
    "W",   # pycodestyle warnings
    "F",   # pyflakes
    "I",   # isort
    "B",   # flake8-bugbear
    "UP",  # pyupgrade (modernize syntax)
    "C4",  # flake8-comprehensions
]
ignore = ["E501"] # Let formatter handle line wraps

[tool.ruff.format]
quote-style = "double"
indent-style = "space"
```

### Mypy Configuration (`pyproject.toml`)
```toml
[tool.mypy]
python_version = "3.10"
strict = true
warn_unused_configs = true
warn_redundant_casts = true
warn_unused_ignores = true
disallow_untyped_defs = true
disallow_incomplete_defs = true
check_untyped_defs = true
```

### Pytest Configuration (`pyproject.toml`)
```toml
[tool.pytest.ini_options]
minversion = "7.0"
addopts = "-ra -q --strict-markers"
testpaths = ["tests"]
pythonpath = ["src"]
```
