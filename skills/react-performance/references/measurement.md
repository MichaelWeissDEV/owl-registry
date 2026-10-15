# Measurement reference

## Core Web Vitals thresholds (assessed at the 75th percentile of field data)

| Metric | Good | Poor |
|---|---|---|
| LCP (Largest Contentful Paint) | <= 2.5 s | > 4 s |
| INP (Interaction to Next Paint) | <= 200 ms | > 500 ms |
| CLS (Cumulative Layout Shift) | <= 0.1 | > 0.25 |

INP replaced FID as a Core Web Vital in March 2024. Lab tools (Lighthouse, DevTools) approximate; field data (CrUX, or RUM via the `web-vitals` library) is the ground truth.

## Tools and what they answer

- React DevTools Profiler: which components rendered, why, and how long.
- Chrome DevTools Performance panel: main-thread breakdown, long tasks, layout and paint, interactions, CPU/network throttling.
- Lighthouse: lab audit with opportunities; run in a clean profile without extensions.
- Bundle analyzers: what is in the JavaScript you ship.
- Memory panel: heap snapshots and allocation timelines for leaks.

## Rules of thumb

- Throttle the CPU (for example 4x slowdown) when profiling on a fast laptop.
- A long task is over 50 ms on the main thread; break up or defer it.
- Re-render count is not a goal; user-visible latency is.
- Compare like with like: same build mode, data size, device, and several runs.
