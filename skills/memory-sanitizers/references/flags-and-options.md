# Flags, Options and Compatibility

## Compile and link flags

| Purpose | Flag | Notes |
|---|---|---|
| ASan | `-fsanitize=address` | Use `-O1` or higher, `-g`, `-fno-omit-frame-pointer`; link with the same flag via the compiler driver |
| UBSan | `-fsanitize=undefined` | Report-and-continue by default; add `-fno-sanitize-recover=undefined` to abort |
| Recover mode for others | `-fsanitize-recover=address` | Lets ASan continue after an error only together with `ASAN_OPTIONS=halt_on_error=0`; use rarely, it makes later reports unreliable |
| LSan standalone | `-fsanitize=leak` | Included in ASan on Linux; on macOS enable `ASAN_OPTIONS=detect_leaks=1` |
| TSan | `-fsanitize=thread` | Not combinable with ASan or LSan |
| MSan (Clang) | `-fsanitize=memory` | Add `-fsanitize-memory-track-origins=2` (or `=1` for allocation-site only, faster) |
| ASan use-after-return | `-fsanitize-address-use-after-return=(never\|runtime\|always)` | Default `runtime` |
| ASan use-after-scope | `-fsanitize-address-use-after-scope` | |
| Smaller ASan code | `-fsanitize-address-outline-instrumentation` | Costs runtime speed |
| Precise frames | `-fno-optimize-sibling-calls` | |

## Combination matrix

| | ASan | LSan | UBSan | TSan | MSan |
|---|---|---|---|---|---|
| ASan | - | ok (default inside ASan on Linux) | ok | rejected | do not combine (separate builds) |
| UBSan | ok | ok | - | ok in practice | ok in practice |
| TSan | rejected | rejected (GCC docs) | ok in practice | - | do not combine |

Evidence: GCC instrumentation docs (address vs thread/hwaddress; thread vs address/leak); local Apple clang 21 rejected `-fsanitize=address,thread`. The ASan+MSan row is the widely documented design restriction; Apple clang here could not test it because MSan is unsupported on that target. "ok in practice" means commonly combined, not guaranteed for every compiler version: if the driver errors, split the builds.

## Runtime options (environment variables)

| Variable | Examples | Notes |
|---|---|---|
| `ASAN_OPTIONS` | `detect_stack_use_after_return=1`, `detect_leaks=0`, `symbolize=0`, `help=1` | Colon-separated |
| `UBSAN_OPTIONS` | `print_stacktrace=1`, `halt_on_error=1` | Parsed separately from ASAN_OPTIONS |
| `LSAN_OPTIONS` | `suppressions=<file>` | Needs ptrace; may fail in locked-down containers |
| `TSAN_OPTIONS` | `halt_on_error=1`, `second_deadlock_stack=1` | |
| `MSAN_OPTIONS` | `poison_in_dtor=1` | |
| `*_SYMBOLIZER_PATH` | path to `llvm-symbolizer` | When reports show raw addresses |

Env vars override compile-time `__asan_default_options()`. List available options for your exact runtime with `help=1` rather than trusting any table (including this one).

## Platform notes

- ASan: Linux, macOS, iOS Simulator, Android, NetBSD, FreeBSD, Windows 8.1+ (Windows less thoroughly supported). macOS: run `dsymutil` for line info.
- MSan: Linux, FreeBSD, NetBSD (Clang only).
- GCC: ASan, UBSan, LSan, TSan; no MSan.

## Suppressions policy

A suppression file is a debt record: each line needs a comment with an issue link and owner. Prefer fixing; for third-party code you cannot rebuild, suppress the narrowest frame (function or library) rather than the whole module.
