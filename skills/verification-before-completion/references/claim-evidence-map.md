# Claim-to-evidence map

What counts as sufficient evidence for common claims, and what does not. Commands are examples; use the project's own.

| Claim | Sufficient evidence | Insufficient on its own |
| --- | --- | --- |
| "Builds" | The documented build command exits 0 and produces the expected artifact | Editor shows no errors |
| "Tests pass" | Full relevant suite run after last edit; counts read; skips explained | One file's tests passed; exit code only |
| "Bug fixed" | Regression test fails on old code, passes on new; original repro no longer fails | Code reads correct; unrelated tests pass |
| "Feature works" | The feature exercised through its real entry point (CLI call, HTTP request, UI action) with observed output | Unit tests of internals only |
| "No regressions" | Existing suite passes plus a check of callers of changed code (`git grep` for usages) | Suite passes but changed code has no coverage |
| "Lint/format clean" | Linter run with project config shows zero findings | Formatter ran but linter did not |
| "Types check" | Type checker run in strict mode the project uses | Tests pass |
| "Dependency updated" | Lockfile diff shows the version; install and tests succeed | Manifest edited only |
| "Docs updated" | Rendered or link-checked docs; examples actually executed | Prose edited |
| "Config change applied" | Re-read the effective config or observe changed behavior | File was written |
| "Subagent finished X" | You inspected its diff or reran its check | Its summary message |
| "CI green" | CI run for the exact commit, read via read-only means | Local pass |
| "Performance improved" | Before/after measurement, same conditions, repeated | One timing, different machine state |
| "Security issue resolved" | Test or demonstration (in an authorized environment) that the vulnerable path is closed | Patch applied |

## Freshness rule of thumb

A check stays valid only for the files and inputs it exercised. Map each edit to the checks it could invalidate:

- Source edit: rerun tests that import it, plus build and type checks.
- Test edit: rerun that test and prove it can fail.
- Config/lockfile edit: rerun build, tests, and anything reading that config.
- Docs-only edit: link/example checks; no need to rerun the test suite unless doc examples are tested.

## Reading output skeptically

- Count line (`N passed, M skipped`): are N and M plausible for the area touched?
- Did warnings appear that mention deprecated or ignored configuration?
- Was the test selector specific enough to run something, but not so narrow it skipped the changed code?
- Does the run use the same interpreter, version, and environment variables as CI?
