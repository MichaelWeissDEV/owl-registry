# Rust Trait Design & API Patterns

## 1. Implement Standard Traits
Users expect idiomatic types to implement standard library traits whenever logically sound:
- `Debug`: Implement on virtually every public type (`#[derive(Debug)]`).
- `Clone` / `Copy`: Derive `Clone` when inexpensive; derive `Copy` only for small POD types (e.g. coordinates, IDs).
- `PartialEq`, `Eq`: For value types compared in tests or maps.
- `Default`: Provide sensible zero/empty defaults.
- `Display`: For types that have a natural user-facing string representation.

---

## 2. Builder Pattern for Complex Structs

When a struct has many configuration options, use the Builder pattern:

```rust
#[derive(Debug, Clone)]
pub struct HttpClient {
    timeout: std::time::Duration,
    retries: u32,
    follow_redirects: bool,
}

pub struct HttpClientBuilder {
    timeout: std::time::Duration,
    retries: u32,
    follow_redirects: bool,
}

impl HttpClientBuilder {
    pub fn new() -> Self {
        Self {
            timeout: std::time::Duration::from_secs(30),
            retries: 3,
            follow_redirects: true,
        }
    }

    pub fn timeout(mut self, timeout: std::time::Duration) -> Self {
        self.timeout = timeout;
        self
    }

    pub fn build(self) -> HttpClient {
        HttpClient {
            timeout: self.timeout,
            retries: self.retries,
            follow_redirects: self.follow_redirects,
        }
    }
}
```

---

## 3. Sealed Traits
When you want to define a public trait that users can use as a bound, but NOT implement for their own types:

```rust
mod private {
    pub trait Sealed {}
}

pub trait MyPlugin: private::Sealed {
    fn execute(&self);
}

// Only types in this crate can implement private::Sealed
```
