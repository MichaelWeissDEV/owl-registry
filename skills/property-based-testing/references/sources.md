# Sources and provenance: property-based-testing

Consulted 2026-10-15 (read-only):

- Hypothesis API reference, https://hypothesis.readthedocs.io/en/latest/reference/api.html : settings defaults (max_examples 100, deadline 200 ms, derandomize, database, suppress_health_check), profiles and the built-in `ci` profile, `@example` semantics (runs first, not shrunk, not counted), `assume`/`note`/`event`, stateful API, health-check names. Only the first 100k characters of the page were read.
- Hypothesis installed locally from PyPI into a scratch venv: version 6.168.5; examples in SKILL.md and references/examples.md were run under pytest 9.1.1. The shrunk counterexample `'0'` was observed locally.
- proptest book, https://proptest-rs.github.io/proptest/proptest/getting-started.html : `proptest!` syntax, `prop_assert_eq!`, `proptest-regressions` persistence and advice to commit it, shrinking. `ProptestConfig`, `PROPTEST_CASES`, `prop_compose!` details come from the author's prior knowledge and were not confirmed on the fetched page; the Rust snippets were not compiled.

Provenance: all text is original. No text copied from anthropics/skills, obra/superpowers, trailofbits/skills, vercel-labs/agent-skills, huggingface/skills, or supabase/agent-skills; none were consulted for this skill, so no license decision was needed.
