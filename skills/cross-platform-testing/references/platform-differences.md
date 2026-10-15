# Platform differences and debugging recipes

## Case-sensitivity probe

```python
import tempfile, pathlib

def fs_is_case_sensitive() -> bool:
    with tempfile.TemporaryDirectory() as d:
        a = pathlib.Path(d, "probe.txt")
        a.write_text("x")
        return not pathlib.Path(d, "PROBE.TXT").exists()
```

Use probes (capability checks) in skip conditions rather than `sys.platform` when the real question is a filesystem property: macOS can be case-sensitive, Linux can mount case-insensitive volumes.

## Line endings

- Add `.gitattributes`: `* text=auto` and `*.golden text eol=lf` (or `-text` for binary fixtures).
- Never open text fixtures in tests with default newline translation if you compare bytes.
- If your program emits platform-specific newlines on purpose, test both conventions explicitly.

## Windows specifics

- Cannot delete or rename an open file; antivirus/indexers can briefly hold handles, so cleanup helpers may need bounded retries.
- Path length: long-path support depends on OS setting and manifest; test with a deep path if you create nested temp dirs.
- Reserved device names (`CON`, `PRN`, `AUX`, `NUL`, `COM1`...) and trailing dots/spaces in filenames are invalid.
- Default shell in GitHub Actions on Windows is PowerShell (`pwsh`); on Linux/macOS it is bash. Set `defaults.run.shell: bash` if you want one syntax in `run:` steps (Git Bash is available on hosted Windows runners).
- Console encoding may not be UTF-8; set `PYTHONUTF8=1` or equivalent only if that is your policy, and test both.

## macOS specifics

- Default filesystem is case-insensitive but case-preserving; names may arrive as NFD (HFS+ normalized to NFD; APFS preserves the bytes it is given, but APIs and tools such as older volumes, archives or Finder can still produce NFD), so compare normalized forms.
- Apple silicon is arm64; Intel legs use `-intel` labels. Universal binaries and Rosetta change which code path runs.
- Sandbox/privacy prompts can block tests that touch Documents, camera, etc.; keep such tests out of CI.

## Linux specifics

- glibc vs musl (Alpine) differences: DNS, locale, threads stack size, `iconv`. If you ship a musl wheel or static binary, test inside an Alpine container.
- Container user IDs, read-only root filesystems, and `/tmp` size limits.

## Architecture

- Endianness matters only for raw binary formats; use explicit byte order. Most CI hosts are little-endian; for big-endian coverage use emulation (QEMU) on a scheduled job and say it is slow.
- 32-bit builds expose `int`/pointer width assumptions.
- arm64 vs x64: floating point results can differ in last digits when fused multiply-add is used; compare with tolerance; SIMD intrinsics and inline assembly need per-arch tests.

## Debug recipe: leg-only failure

1. Download logs and artifacts from the failing leg; compare against the passing leg line by line.
2. Print environment facts in a temporary step: OS version, architecture, default encoding, locale, `TZ`, cwd, free disk, tool versions.
3. Minimize: re-run with only the failing test selected (`pytest path::test -x -vv`).
4. If it is timing-dependent, run the test 50 times on the leg (`pytest --count` from the pytest-repeat plugin, or a shell loop) to measure flake rate before changing code.
5. Fix at the right layer (code, test helper, or CI config), add the regression test, remove diagnostics.

## Matrix design heuristics

- Pairwise thinking: most failures involve one or two dimensions interacting (OS x language version), rarely three. A reduced matrix that covers every pair at least once catches most of them.
- Ownership: assign each leg an owner; an unowned leg rots.
- Cost: measure minutes per leg; macOS and Windows runners are typically more expensive or slower than Linux on hosted plans (check current billing multipliers on GitHub's pricing page).
