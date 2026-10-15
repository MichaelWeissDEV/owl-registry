# Common Python Anti-Patterns and Traps

## 1. Late Binding in Closures
Python closures bind variables by reference, not value at definition time.

```python
# BUG: All functions in `funcs` will return 9!
funcs = [lambda: i for i in range(10)]

# FIX: Bind variable as default argument:
funcs = [lambda i=i: i for i in range(10)]
```

---

## 2. Mutating a Collection While Iterating Over It

```python
# BUG: Skipping elements or RuntimeError: Set/Dict changed size during iteration
for item in active_users:
    if item.is_expired():
        active_users.remove(item)

# FIX: Iterate over a copy or list comprehension
expired = [u for u in active_users if u.is_expired()]
for u in expired:
    active_users.remove(u)
```

---

## 3. Using `is` Instead of `==` for Value Comparison

`is` checks memory identity (same object address), while `==` checks value equality.
Python caches small integers and interned short strings in CPython, creating deceptive passes that fail in production:

```python
# BUG: the result depends on interpreter details (constant folding, caching),
# so `a is b` may be True in one context and False in another
a = int("1000")
b = int("1000")
a is b # False in CPython

# FIX:
a == b # True!
```
Use `is` ONLY for singletons like `None`, `True`, `False`, or custom sentinel objects (`if x is None:`).

---

## 4. Uncaught Generator / Resource Leaks

```python
# BUG: File handle remains open until GC cycle
lines = open("large.log").readlines()

# FIX:
with open("large.log", "r", encoding="utf-8") as f:
    lines = f.readlines()
```
