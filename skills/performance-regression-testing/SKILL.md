---
name: performance-regression-testing
description: >
  Detect performance regressions reliably in CI and local review: design benchmarks, control noise,
  take enough samples, compare against a stored baseline with statistics instead of eyeballing,
  and choose thresholds that avoid both flaky failures and missed slowdowns. Covers hyperfine
  (CLI commands), pytest-benchmark (Python), Criterion (Rust), warmup, outliers, baseline storage,
  A/B interleaving, deterministic proxies (instruction counts, allocations), and shared-runner
  noise. Use when adding perf gates, investigating "did this PR make it slower", or building
  benchmark suites. Do NOT use to find WHY something is slow or to optimize hot paths (use
  performance-profiling), for load/capacity testing of services, or for correctness tests.
compatibility: >
  Agent Skills-compatible coding agents. Tools: hyperfine, pytest-benchmark (verified 5.3.0),
  Criterion.rs, GitHub Actions. Benchmark numbers are machine-specific; baselines must be taken
  on comparable hardware.
metadata:
  author: michaelweissdev
  version: "1.0.0"
  tags: "benchmarking, performance, regression, hyperfine, pytest-benchmark, criterion, ci, statistics"
  topics: "software-development, testing, performance"
---

# Performance Regression Testing

The question is comparative and statistical: "is version B slower than version A, by more than noise, for a workload that matters?" Profiling answers *why*; this skill answers *whether*, and gates on it.

Boundaries: finding hotspots and fixing them is `performance-profiling`; CI plumbing is `ci-github-actions`; test-strength is [mutation-testing](../mutation-testing/SKILL.md); matrix over OS/hardware is [cross-platform-testing](../cross-platform-testing/SKILL.md).

## Non-negotiable rules

1. Never conclude from a single run or from the mean alone. Collect many samples, look at median/min and spread, and compare distributions.
2. Same workload, same machine class, same build flags, same inputs for baseline and candidate. Release/optimized builds only; benchmark what ships.
3. Benchmarks must be hermetic: no network, no production data or services, fixed seeded inputs, temp dirs for IO. Do not benchmark against live systems.
4. Do not tune thresholds after seeing a failure just to make CI green. Investigate; if the change is intended (accepted tradeoff), update the baseline in a reviewed commit with a justification.
5. Do not commit machine-specific absolute numbers as pass/fail limits for shared CI. Compare relative to a baseline measured in the same job or on the same runner class.
6. A benchmark that gates merges needs an owner and a documented flake policy (rerun once, then investigate).

## Workflow

### 1. Define what to measure

- Pick user-visible or SLO-relevant operations: request handler p50 in-process, parse of a representative 1 MB file, CLI cold start, algorithm on realistic n. Microbenchmarks of tiny functions are cheap and noisy; pair them with a few end-to-end ones.
- Fix input size and shape; include at least two sizes to catch complexity regressions (O(n) to O(n^2) shows as a slope change, not a constant factor).
- Decide the metric: wall time, CPU time, allocations/peak memory, instruction count, binary size, or throughput. Memory and instruction counts are far less noisy than time.

### 2. Make the measurement trustworthy

- Warmup: discard first iterations (JIT, caches, lazy init). hyperfine: `--warmup N`. pytest-benchmark and Criterion warm up automatically; tune only if needed.
- Samples: enough that the noise floor is known. hyperfine runs at least 10 by default (`--runs N` or `--min-runs`); Criterion defaults are tunable (`--sample-size`, `--measurement-time`; see `cargo bench -- --help`); pytest-benchmark `--benchmark-min-rounds` (default 5; raise it).
- Cold vs warm: decide on purpose. For disk or cache effects use hyperfine `--prepare '<cmd>'` before each run (e.g. to clear a cache you own) and say so. Use `--setup` for one-time work outside measurement.
- Measure the work, not the harness: avoid printing in the timed region; with hyperfine on tiny commands use `-N` (no shell) to avoid shell startup dominating (hyperfine warns about commands under a few ms).
- Control the environment: idle machine, pinned CPU frequency/performance governor where possible, no other heavy processes, consistent power mode (laptops), same OS and runtime versions.
- Python: avoid measuring import time unless intended; use `benchmark.pedantic(func, setup=..., rounds=..., iterations=...)` when setup per round is required.

### 3. Compare statistically

- Report median, min (best-case, least noisy for CPU-bound code), spread (IQR or stddev), and sample count. Outliers are common (scheduler, GC): examine, don't silently drop. The max is a poor statistic (one scheduler hiccup sets it), and mean and median can still agree while the tail is ugly, so look at the spread, not just the center.
- Prefer a significance test plus an effect-size threshold: change is "real" only if statistically distinguishable *and* larger than a minimum relevant effect (e.g. 5%). Criterion does this: compares to the saved baseline with a significance level and a noise threshold, and reports "regressed/improved/no change"; hyperfine prints mean ± sigma and relative speed between commands; pytest-benchmark compares to saved runs.
- For A/B decisions, interleave runs (A B A B ...) or run both in the same job; sequential blocks confound with drift (thermal throttling, noisy neighbors).
- Repeat a suspicious regression 2 to 3 times and on a second machine before blocking a merge.

### 4. Store and compare baselines

| Tool | Save | Compare | Gate |
|---|---|---|---|
| pytest-benchmark | `--benchmark-save=NAME` or `--benchmark-autosave` (storage `.benchmarks` by default; `--benchmark-storage` to change) | `--benchmark-compare` (latest, or a run id) | `--benchmark-compare-fail=mean:10%` or `min:5%` (repeatable) |
| Criterion | `cargo bench -- --save-baseline main` | `cargo bench -- --baseline main` (compares without overwriting) | Read report/`change` estimates in CI scripts; Criterion itself does not fail the run |
| hyperfine | `--export-json out.json` (also CSV/markdown) | compare two JSON files with a script, or run both commands in one invocation (first is the reference) | script checks median/relative ratio |

Verified locally (pytest-benchmark 5.3.0): `--benchmark-only --benchmark-save=base --benchmark-storage=file://./bm`, then rerun with `--benchmark-compare --benchmark-compare-fail=mean:10%` produced a comparison table of NOW versus 0001_base and exit 0.

Where do baselines live? Best: measure the base commit and the PR commit in the same CI job on the same runner (checkout base, build, bench; checkout head, build, bench), so hardware noise cancels. Second: stored artifacts per runner class. Worst: numbers hardcoded in the repo.

### 5. Run it in CI

- Shared hosted runners are noisy neighbors; absolute timings vary run to run. Use same-job A/B, generous thresholds (e.g. 10 to 15% for time), median-of-N, and consider reporting-only for time while hard-gating deterministic metrics (instruction counts via tooling such as valgrind-based counters, allocation counts, binary size).
- Self-hosted dedicated runners give lower noise: label them and pin one job per machine.
- Trigger: on PRs touching hot paths (path filters) and nightly on main for trend lines; do not run heavy suites on every push.
- Output: post a PR comment or job summary table (before, after, % change, samples); store raw JSON as an artifact.
- Failing policy: warn at ~5%, fail at ~10% (tune to your measured noise: threshold should exceed 2 to 3 times the run-to-run variation of the unchanged code; measure that by benchmarking main against itself 20 times).

Minimal GitHub Actions sketch (same-job A/B for a CLI; unexecuted, adapt before use):

```yaml
on:
  pull_request:
    paths: ["src/**", "Makefile"]
jobs:
  bench:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4   # pin to a commit SHA per your policy
        with: { fetch-depth: 0 }
      - name: install hyperfine
        run: sudo apt-get update && sudo apt-get install -y hyperfine jq
      - name: build base and head
        run: |
          git worktree add ../base ${{ github.event.pull_request.base.sha }}
          (cd ../base && make release && cp target/release/tool /tmp/tool-base)
          make release && cp target/release/tool /tmp/tool-head
      - name: benchmark
        run: hyperfine --warmup 3 --runs 30 --export-json bench.json '/tmp/tool-base data.bin' '/tmp/tool-head data.bin'
      - name: gate on median ratio
        run: |
          python3 - <<'PY'
          import json, sys
          r = json.load(open("bench.json"))["results"]
          base, head = r[0]["median"], r[1]["median"]
          ratio = head / base
          print(f"median base={base:.4f}s head={head:.4f}s ratio={ratio:.3f}")
          if ratio > 1.10:
              sys.exit(1)
          PY
      - uses: actions/upload-artifact@v4
        if: always()
        with: { name: bench, path: bench.json }
```

(Illustrative and not executed here; the hyperfine JSON `median` field is per its export format, but check it against your installed version. Adapt build commands and pin action versions per your policy; see `github-actions-security`.)

### 6. When a regression is flagged

1. Rerun to rule out noise (3 times, same job).
2. Bisect: `git bisect run` with the benchmark script and a threshold check.
3. Profile the offending commit (hand off to `performance-profiling`).
4. Decide: fix, accept with justification and updated baseline, or revert.

## Worked example: Python parser

`bench_parse.py` with pytest-benchmark: `def test_parse_1mb(benchmark, sample_1mb): benchmark(parse, sample_1mb)`; fixed seeded `sample_1mb`. On main: `pytest bench_parse.py --benchmark-only --benchmark-save=main`. On the PR branch: `pytest bench_parse.py --benchmark-only --benchmark-compare --benchmark-compare-fail=median:10%`. Gate on the median (robust to a few outliers, still sensitive to typical-case slowdowns) and, where you can, on a deterministic proxy such as instruction or allocation counts. `min` is less noisy but has a blind spot: a regression that only affects typical or tail runs (extra allocation, cache misses, occasional slow path) can leave the best run unchanged, so treat `min` as advisory, not as the gate. Add a 10 MB variant to detect scaling regressions; if time ratio between 1 MB and 10 MB grows from 10x to 40x, the change introduced super-linear behavior even if the 1 MB number is within noise.

## Anti-patterns

- One run, one number, one conclusion; mean-only comparisons with heavy tails.
- Benchmarking debug builds, or with different flags between base and head.
- Letting the compiler optimize away the work (use `black_box`/Criterion `iter` or return values the harness consumes).
- Comparing runs from different days/machines/runners.
- Gating on tiny microbenchmarks at 1% thresholds on shared runners.
- Ignoring warmup, then "discovering" a regression that is just cold start.
- Raising thresholds until the gate never fires.
- Benchmark measures the mock instead of the code.

## Verification checklist

- [ ] Metric, workload, and input sizes defined; inputs seeded and hermetic
- [ ] Release build, warmup, enough samples; spread reported alongside the central estimate
- [ ] Baseline measured on equal footing (same job or same runner class)
- [ ] Threshold justified by measured run-to-run variation of unchanged code
- [ ] Flag handling documented (rerun, bisect, accept via reviewed baseline update)
- [ ] Raw results stored as artifacts

## References

- [Statistics notes: noise, effect size, thresholds](references/statistics.md)
- [Scenarios for evaluating this skill](references/scenarios.md)
- [Sources and provenance](references/sources.md)
