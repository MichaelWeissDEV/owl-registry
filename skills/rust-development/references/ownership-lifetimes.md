# Rust Ownership, Borrowing, and Lifetimes

Rust achieves memory safety without a garbage collector through compile-time ownership semantics.

## 1. The Core Ownership Rules
1. Each value in Rust has an owner (a variable binding).
2. There can only be one owner at a time.
3. When the owner goes out of scope, the value is dropped (`Drop::drop`).

## 2. Borrowing Rules
You may have:
- **One or more immutable references (`&T`)**, OR
- **Exactly one mutable reference (`&mut T`)** at any given time.
You can never have both concurrently within the same scope. This guarantees data-race freedom at compile time.

## 3. Lifetime Annotations (`'a`)
Lifetime annotations do not change how long a value lives; they describe the relationship between the lifetimes of multiple references so the borrow checker can verify safety.

### Lifetime Elision Rules
The compiler automatically infers lifetimes when:
1. Each elided lifetime in input arguments gets its own distinct lifetime parameter.
2. If there is exactly one input lifetime, that lifetime is assigned to all elided output lifetimes.
3. If there are multiple input lifetimes, but one of them is `&self` or `&mut self`, the lifetime of `self` is assigned to all output lifetimes.

### Explicit Annotations
When a function returns a reference derived from one of multiple input references:

```rust
// The returned reference will be valid as long as BOTH x and y are valid
pub fn longest<'a>(x: &'a str, y: &'a str) -> &'a str {
    if x.len() > y.len() {
        x
    } else {
        y
    }
}
```

## 4. Avoiding Cloning with Cow (Clone-on-Write)
When a function might need to modify a string or might return the borrowed slice unchanged, use `std::borrow::Cow`:

```rust
use std::borrow::Cow;

pub fn sanitize_input(input: &str) -> Cow<'_, str> {
    if input.contains('<') {
        // Needs modification: allocates a new String
        Cow::Owned(input.replace('<', "&lt;"))
    } else {
        // Safe: borrows the input without heap allocation
        Cow::Borrowed(input)
    }
}
```
