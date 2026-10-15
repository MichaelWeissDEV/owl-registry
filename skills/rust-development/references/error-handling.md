# Robust Error Handling in Rust

Rust represents recoverable errors using `Result<T, E>` and optionality using `Option<T>`.

## 1. Ergonomic Combinators

Avoid nested `match` statements where functional combinators express intent more concisely:

```rust
// map and and_then
let user_email: Option<String> = find_user(user_id)
    .and_then(|u| u.contact_info)
    .map(|c| c.email.to_lowercase());

// ok_or_else to convert Option to Result
let required_token = config.api_token
    .ok_or_else(|| AppError::MissingConfiguration("api_token".into()))?;
```

---

## 2. Converting Error Types with `?` and `From`

The `?` operator automatically calls `From::from` on the error value to convert it into the return error type of the enclosing function:

```rust
impl From<std::io::Error> for MyError {
    fn from(err: std::io::Error) -> Self {
        MyError::Io(err)
    }
}
```

Libraries using `thiserror` generate these `From` implementations automatically via the `#[from]` attribute.

---

## 3. Libraries vs Applications

- **In Libraries**: Define exhaustive, strongly typed error enums (`thiserror`). Callers must be able to inspect error variants programmatically and decide how to recover.
- **In Applications/CLIs**: Use `anyhow::Result<T>`. Application errors typically need rich context for human operators (`.context("Failed to load settings file")`) rather than programmatic pattern matching.
