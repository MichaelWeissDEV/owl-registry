# Fuzzing troubleshooting

| Symptom | Likely cause | What to do |
|---|---|---|
| Coverage plateaus in seconds | Early validation (magic, checksum, length) rejects mutations | Fuzz the inner function, recompute checksum in harness, derive structured input, add dictionary |
| exec/s very low | Slow setup per call, logging, large inputs, disk IO | Move init out of the per-input function (static/lazy init), remove printing, lower `-max_len`, profile |
| Crash does not reproduce | Harness nondeterminism (hash seeds, threads, time, global state) | Remove randomness, reset state per call, run the single artifact repeatedly |
| Same bug reported thousands of times | No dedupe | libFuzzer `-fork=N -ignore_crashes=1` or fix first then rerun; dedupe by top frames |
| OOM/timeouts reported | Algorithmic complexity or unbounded allocation | Real findings: add limits or fix complexity; tune `-rss_limit_mb`/`-timeout` only if the limit is unrealistic |
| Sanitizer complaints from a dependency | Third-party bug or false positive | Isolate by reproducing outside the fuzzer; suppress narrowly and record why |
| Rust: cargo-fuzz will not build | Needs nightly toolchain and sanitizer-capable target | Install nightly (`rustup toolchain install nightly`) and rerun; check the cargo-fuzz README for platform notes |
| Atheris finds nothing in native code | Extension not instrumented | Follow Atheris native-extension guide; build extension with coverage/sanitizer flags |
| AFL++ refuses to start | core_pattern/CPU governor checks | Run `afl-system-config` as root, or set the documented `AFL_*` bypass variables knowingly |

## Measuring a campaign

Record: run duration, execs/s, corpus size, coverage counters (libFuzzer prints `cov:` edges and `ft:` features), number of unique crashes. Use `cargo fuzz coverage` or LLVM source-based coverage to find unreached functions, then add seeds or dictionary entries for them.

## Writing a regression after a fix

Keep the minimized crash file (a few bytes) in a `regressions/` directory, replay it in a normal unit test via `include_bytes!` or a pytest parametrize over files, so the bug stays covered without running the fuzzer.
