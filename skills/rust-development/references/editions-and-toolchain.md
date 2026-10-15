# Rust Editions, Toolchain, and Dependency Hygiene

Checked against the Rust release notes (stable 1.99.0 released 2026-10-01) and the Edition Guide, October 2026. Confirm exact details in the Edition Guide before migrating.

## Edition 2024 (Rust 1.85+) changes that affect code review

- `unsafe_op_in_unsafe_fn` warns by default: even inside an `unsafe fn`, each unsafe operation needs its own `unsafe { }` block with a `// SAFETY:` comment.
- `extern` blocks must be written `unsafe extern "C" { ... }`; individual items may be marked `safe` or `unsafe`.
- References to `static mut` are denied by lint; prefer atomics, `Mutex`/`OnceLock`, or `UnsafeCell` wrappers.
- `gen` is a reserved keyword. Use `r#gen` for identifiers named `gen`.
- Cargo: `resolver = "3"` is the default for edition 2024 (MSRV-aware dependency resolution when `rust-version` is set).
- Tail-expression temporaries drop earlier and `if let` scrutinee temporaries drop before the `else` block; this can change lock-guard and `Drop` timing. Review code that relies on drop order.
- Let chains (`if let Some(x) = a && x > 0`) are available in edition 2024 on recent stable releases (stabilized in 1.88); check your MSRV.

## Other language and library features worth knowing

- Async closures (`async || {}`) and the `AsyncFn*` traits stabilized in 1.85.
- `std::sync::LazyLock` / `OnceLock` replace most `lazy_static`/`once_cell` use for statics.
- Recent releases keep stabilizing library APIs (for example 1.99 stabilized `Vec::into_parts` and `std::fs::set_times`). Treat the release notes, not memory, as the source before using a new API, and gate it behind your MSRV.

## Migration procedure

1. Start from a clean, passing build on the current edition.
2. `cargo fix --edition` (applies mechanical fixes), review the diff.
3. Set `edition = "2024"` and `rust-version`, build, run `cargo clippy --all-targets --all-features -- -D warnings` and the full test suite.
4. Check for behavior changes from drop order and `static mut` replacements; add tests where locks or destructors matter.
5. Merge separately from feature work.

## Toolchain files

```toml
# rust-toolchain.toml
[toolchain]
channel = "stable"      # or an exact version for reproducible builds
components = ["rustfmt", "clippy"]
```

```toml
# Cargo.toml
[package]
name = "my-crate"
version = "0.1.0"
edition = "2024"
rust-version = "1.85"

[lints.clippy]
unwrap_used = "warn"
dbg_macro = "warn"
```

## Dependency hygiene

- `cargo tree -d` shows duplicate versions; `cargo update -p <crate>` updates one dependency.
- `cargo audit` checks the RustSec advisory database; `cargo deny check` enforces license, source, and ban policies. Install them first (`cargo install --locked cargo-audit cargo-deny`) and treat them as network-using tools.
- Prefer crates with active maintenance; review `build.rs` and proc-macro crates as code that runs on your machine at build time.
- Commit `Cargo.lock` for binaries; for libraries it is optional but useful for CI reproducibility.

## Troubleshooting common build failures

| Symptom | Likely cause | Action |
| :--- | :--- | :--- |
| `edition 2024 is unstable` / feature required | Toolchain older than 1.85 | Update the toolchain or lower the edition |
| New warnings about `static mut` or `unsafe_op_in_unsafe_fn` after migration | Edition 2024 lints | Replace statics with safe synchronization; add inner `unsafe {}` blocks with SAFETY comments |
| Dependency requires newer `rust-version` than you | MSRV-aware resolver or upstream bump | Pin an older compatible version or raise MSRV deliberately |
| Borrow checker error you want to "fix" with `.clone()` | Ownership design problem | Restructure to borrow, split struct borrows, or pass ownership explicitly |
| Miri reports UB | Aliasing or uninitialized memory | Fix the invariant; do not silence Miri |
