# Sources and provenance: fuzz-testing

Consulted 2026-10-15 (read-only):

- Rust Fuzz book, cargo-fuzz tutorial, https://rust-fuzz.github.io/book/cargo-fuzz/tutorial.html : `cargo fuzz init|list|run`, `fuzz_target!`, artifacts under `fuzz/artifacts/`.
- Rust Fuzz book, structure-aware fuzzing, https://rust-fuzz.github.io/book/cargo-fuzz/structure-aware-fuzzing.html : `Arbitrary` derive with `fuzz_target!(|x: T| ...)`.
- Atheris README, https://github.com/google/atheris/blob/master/README.md : `Setup`, `Fuzz`, `instrument_imports`, `FuzzedDataProvider`, supported Python versions (3.11 to 3.14 in current source), native extensions guide pointer.
- AFL++ fuzzing in depth, https://aflplus.plus/docs/fuzzing_in_depth/ : afl-cc builds, `AFL_USE_ASAN`, `afl-cmin`/`afl-tmin`, `afl-fuzz -i -o -- @@`, `-x` dictionary, `-M`/`-S`, `afl-system-config`.

Not confirmed from fetched pages (from author knowledge, flagged in text): `cargo fuzz cmin`/`tmin`/`coverage` flag details (the corpus page returned 404), libFuzzer flag list (`-max_len`, `-runs`, `-max_total_time`, `-timeout`, `-rss_limit_mb`, `-dict`, `-merge=1`, `-fork`). Verify with `--help` before relying on them. No fuzzer was run in producing this skill; the workflow example is illustrative.

Provenance: all text is original; no external skill repositories (anthropics/skills, obra/superpowers, trailofbits/skills, vercel-labs/agent-skills, huggingface/skills, supabase/agent-skills) were consulted, so no license decision was needed.
