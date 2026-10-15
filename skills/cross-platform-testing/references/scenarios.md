# Scenarios: cross-platform-testing

All scenarios: Status: written, not executed. (The sample portable test and the YAML structure were checked locally on one OS: the test passed under pytest and the YAML parsed; no CI run occurred.)

## 1. Positive activation

Status: written, not executed.

Prompt: "Our Python CLI tests are green on Linux CI but users on Windows report file errors. Set up CI so we catch this, and keep the cost reasonable."

Expected: skill activates; writes a support statement, proposes a reduced matrix (full versions on Linux, latest version across OS/arch), `fail-fast: false`, pinned runner labels, portable-test fixes, and diagnoses likely Windows file-handle/newline issues.

## 2. Negative activation

Status: written, not executed.

Prompt: "Write a GitHub Actions workflow that builds a Docker image and pushes it." (ci-github-actions) and "Harden our workflows against injection." (github-actions-security). Skill should not activate.

## 3. Execution evaluation

Status: written, not executed.

Task: Given a library supporting Python 3.11 to 3.14 on Linux, macOS, Windows, produce a CI matrix and fix a test that hardcodes `"/tmp/out.txt"` and compares CRLF-sensitive output.

Pass rubric:
- Matrix derived from stated support policy; not a blind full cross-product (or cost justified)
- `fail-fast: false`, `timeout-minutes`, `permissions: contents: read`
- Explicit runner labels (e.g. `ubuntu-24.04`, `windows-2025`, `macos-26`) and a non-blocking prerelease/latest leg via `continue-on-error: ${{ matrix.experimental }}`
- Test uses `tmp_path`, explicit encoding/newline; `.gitattributes` considered
- Any skip carries a reason; no assertion loosening
- Does not claim a CI run happened

Fail: hardcoded `/tmp`; `sys.platform` skips without reasons; matrix with 50 legs and no rationale; secrets exposed to fork PRs.

## 4. Edge: arm64

Status: written, not executed.

Task: native extension passes on x64 but float output differs on arm64. Pass: adds an arm64 leg, compares with tolerance only where justified, investigates FMA/SIMD differences instead of blanket-skipping.
