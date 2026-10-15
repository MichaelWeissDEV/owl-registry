---
name: test-driven-development
description: >
  Apply the disciplined Red-Green-Refactor Test-Driven Development (TDD) cycle
  to design clean, testable, and minimal code. Use when developing new features
  from specifications, discovering API interfaces through tests, incrementally
  building business logic, or preventing premature optimization and dead code.
compatibility: >
  Agent Skills-compatible coding agents developing software using test-first practices.
metadata:
  author: michaelweissdev
  version: "1.0.0"
  tags: "tdd, testing, red-green-refactor, design, agile, unit-testing"
  topics: "testing, software-development"
---

# Test-Driven Development (TDD)

Test-Driven Development is a software design technique where tests are written **before** production code. By alternating rapidly through the **Red-Green-Refactor** cycle, developers clarify requirements, discover clean API interfaces, produce minimal implementations without bloat, and maintain a comprehensive regression safety net from day one.

## Core Rules

1. **Write no production code without a failing test**: You are not allowed to write any production code unless it is to make a failing unit test pass.
2. **Red**: Write a single small test that expresses a requirement. Verify that it **fails for the expected reason** (not due to a compilation/syntax typo).
3. **Green**: Write the **minimal** amount of production code necessary to make the test pass. Do not write ahead of the tests.
4. **Refactor**: Clean up duplication, improve naming, extract helper methods, and optimize data structures while keeping tests green.
5. **Incremental progression**: Start with the simplest possible case (empty input, zero, default state), then proceed to basic cases, boundary conditions, and finally complex business logic.

---

## 1. The Red-Green-Refactor Cycle

```
      ┌────────────────────────────────────────────────────────┐
      ▼                                                        │
┌───────────┐         ┌───────────┐         ┌────────────┐     │
│   RED     │ ──────> │   GREEN   │ ──────> │  REFACTOR  │ ────┘
│ Write     │         │ Minimal   │         │ Clean code │
│ failing   │         │ code to   │         │ while      │
│ test      │         │ pass test │         │ all green  │
└───────────┘         └───────────┘         └────────────┘
```

---

## 2. Realistic TDD Walkthrough: A String Calculator

### Step 1: Simplest Case (Empty String Returns Zero)

**1. RED: Write failing test**
```python
# test_calculator.py
from calculator import add

def test_empty_string_returns_zero():
    assert add("") == 0
```
Run test: `FAILED: ImportError: cannot import name 'add' from 'calculator'` (Expected failure).

**2. GREEN: Minimal code to pass**
```python
# calculator.py
def add(numbers: str) -> int:
    return 0
```
Run test: `PASSED` (1 passed).

---

### Step 2: Single Number Returns Its Value

**1. RED: Write next failing test**
```python
def test_single_number_returns_value():
    assert add("5") == 5
```
Run test: `FAILED: assert 0 == 5`.

**2. GREEN: Minimal code to pass**
```python
def add(numbers: str) -> int:
    if not numbers:
        return 0
    return int(numbers)
```
Run test: `PASSED` (2 passed).

---

### Step 3: Two Comma-Separated Numbers

**1. RED: Write failing test**
```python
def test_two_comma_delimited_numbers():
    assert add("1,2") == 3
```
Run test: `FAILED: ValueError: invalid literal for int() with base 10: '1,2'`.

**2. GREEN: Minimal code to pass**
```python
def add(numbers: str) -> int:
    if not numbers:
        return 0
    parts = numbers.split(",")
    return sum(int(p) for p in parts)
```
Run test: `PASSED` (3 passed).

---

### Step 4: REFACTOR Phase

Now that tests are 100% green, improve the design without changing behavior:
```python
def add(numbers: str) -> int:
    """Calculate sum of comma-delimited numbers string."""
    if not numbers:
        return 0
    return sum(map(int, numbers.split(",")))
```
Run test: `PASSED` (3 passed). Design is clean, robust, and fully verified.

---

## 3. Common Mistakes and Anti-Patterns

| Anti-Pattern | Risk | Correct Practice |
| :--- | :--- | :--- |
| Writing 10 tests before writing any code | Overwhelming red state, hard to isolate failures | Write one test, make it pass, repeat |
| Writing more production code than needed to pass | Introduces untested logic and speculative features | Write ONLY enough to satisfy the current test |
| Skipping the Refactor step | Accumulates messy code and duplicate logic | Refactor as soon as the test is green |
| "Testing the Test" (tautological tests) | `assert calculate(x) == calculate(x)` always passes | Assert against concrete expected constants: `assert calculate(2) == 4` |
| Not seeing the test fail | Test might pass trivially or not actually test the code | Always verify the test fails in RED phase |

---

## 4. Verification Checklist

- [ ] New test was observed failing before implementing code.
- [ ] Failure message in RED phase accurately identified the missing feature.
- [ ] Production code is the minimal necessary implementation.
- [ ] All previous tests continue to pass in GREEN phase.
- [ ] Code was refactored for clarity and conciseness while tests stayed green.
