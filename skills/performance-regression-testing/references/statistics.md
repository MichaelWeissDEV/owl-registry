# Statistics notes for benchmarks

## Why means mislead

Timing distributions are right-skewed with a hard floor (the fastest possible run) and a long upper tail from interrupts, GC, frequency scaling, cache effects. Mean and standard deviation are dragged by the tail; `min` and `median` track the code. Use min for CPU-bound deterministic code, median for code with real variance (IO, GC-heavy), and show IQR.

## Choosing a threshold

1. Benchmark the unchanged main branch against itself 20 or more times on the target runner class.
2. Take the spread of the central estimate (e.g. the 95th percentile of |change|).
3. Set the fail threshold at 2 to 3 times that value, never below ~3% on shared hosted runners.
4. Revisit quarterly or when runner hardware changes.

## Significance vs relevance

With enough samples, tiny differences become statistically significant but irrelevant. Gate on both: significant AND larger than the minimum effect you care about. Criterion exposes this as a significance level and a noise threshold (see `cargo bench -- --help` for the current flag names and defaults).

## Multiple comparisons

A suite of 200 benchmarks will show a few spurious "regressions" per run at a 5% significance level. Require a regression to appear in a repeat run, or gate on a small set of key benchmarks and report the rest.

## Complexity regressions

Run each benchmark at n, 2n, 4n (or 10x steps). The ratio between steps estimates the exponent. Alert when it changes more than expected, even if absolute time at the standard size is within noise.

## Deterministic proxies

Instruction counts (e.g. via valgrind-family tools or hardware counters where available), allocation counts, peak RSS, bytes processed, queries issued, and binary size are far more stable than wall time. Gate hard on these; treat wall time as advisory on shared runners.

## Interleaving

Order effects (thermal throttling, page cache warming) bias sequential A-then-B runs. Alternate ABAB..., or run both binaries inside one benchmark loop, and randomize order.

## Reporting template

| Benchmark | Base median | Head median | Change | Samples | Verdict |
|---|---|---|---|---|---|
| parse_1mb | 12.1 ms | 12.3 ms | +1.7% | 200 | within noise |
