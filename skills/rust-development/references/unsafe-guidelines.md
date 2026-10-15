# Unsafe Rust Guidelines and Invariants

`unsafe` in Rust does not disable the borrow checker or type system; it grants access to 5 superpowers:
1. Dereferencing a raw pointer (`*const T`, `*mut T`).
2. Calling an `unsafe` function or method.
3. Implementing an `unsafe` trait.
4. Mutating a mutable static variable.
5. Accessing fields of a `union`.

## 1. When is `unsafe` Legitimate?
- **FFI**: Interfacing with C libraries or OS system calls.
- **Hardware registers / low-level memory operations**: Embedded programming or OS kernels.
- **Core data structures**: Implementing specialized collections (like `Vec` or `BTreeMap`) where the compiler cannot verify internal memory bounds.

## 2. Invariants and the Safety Contract
Every `unsafe` block MUST be accompanied by a `// SAFETY:` comment explaining why the operation is safe and what invariants are guaranteed:

```rust
// SAFETY: We verified `index < self.len` above, so reading at `index`
// is within the allocated bounds of the buffer and aligned.
unsafe {
    *self.ptr.add(index)
}
```

## 3. Tooling: Miri
Always test `unsafe` code with **Miri** (the Rust interpreter for detecting Undefined Behavior):

```bash
cargo +nightly miri test
```
Miri detects:
- Out-of-bounds memory accesses and use-after-free.
- Violations of the Aliasing rules (Stacked Borrows / Tree Borrows).
- Unaligned memory accesses.
- Uninitialized memory reads.
