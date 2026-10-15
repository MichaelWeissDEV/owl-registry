# Reading EXPLAIN output

Applies to PostgreSQL 14-18; version-specific lines are labelled.

## Anatomy of a node

```
Index Scan using orders_cust_idx on orders  (cost=0.43..8.45 rows=1 width=64) (actual time=0.021..0.022 rows=1 loops=1)
  Index Cond: (customer_id = 42)
  Buffers: shared hit=4
```

- `cost=startup..total` and `rows` are the planner's estimates in arbitrary cost units, not milliseconds.
- `actual time=first..last` is **per loop**, in milliseconds. Multiply `last` by `loops` for total node time (for parallel nodes, loops counts workers plus leader and times are averages; read the Gather docs before computing).
- A node's time includes its children. Exclusive time = node time minus child time.
- `Buffers: shared hit` came from cache, `read` from the OS/disk, `dirtied/written` are write effects. `temp read/written` means a spill. In PG 17 and earlier, `BUFFERS` must be requested; in PG 18 it is on with `ANALYZE`.

## Node signals

| Node / line | Meaning | Check |
|---|---|---|
| Seq Scan with big `Rows Removed by Filter` | Reads whole table | Is a selective index possible? Is the predicate sargable (no function on the column)? |
| Index Scan with big `Rows Removed by Filter` | Index only partly matches predicate | Composite or partial index covering the filter |
| Index Only Scan with `Heap Fetches` high | Visibility map not set | Vacuum frequency; long transactions |
| Bitmap Heap Scan `Recheck Cond`, `Heap Blocks: lossy` | Bitmap exceeded `work_mem` | Increase work_mem for the query, or narrow the predicate |
| Nested Loop, inner Seq Scan, large loops | Missing index on join key, or bad estimate chose nested loop | Index on the inner join column; fix estimates |
| Hash Join `Batches: N > 1` | Hash spilled | work_mem, or reduce build side |
| Sort `Sort Method: external merge Disk:` | Sort spilled | work_mem, or provide ordered index |
| Gather / `Workers Launched` < `Planned` | Parallelism starved | `max_parallel_workers`, concurrency |
| `Planning Time` large | Many partitions/joins, or generic plan issues | Partition pruning, prepared statements |
| `JIT:` block with big timing | JIT overhead exceeded benefit | `jit` off for OLTP queries; tune `jit_above_cost` |
| `Index Searches: N` (PG 18) | Number of index descents | Large N for a single scan suggests an `IN`/array shape; PG 18 can use skip scan on btree |

## Estimate vs actual

Compare `rows=` with `actual ... rows=` at every node, remembering actual is per loop.

- 10x or greater error at a scan: stale stats (`ANALYZE`), low `statistics_target`, skewed distribution (extended MCV statistics).
- Error appears after a join: correlated columns. `CREATE STATISTICS name (dependencies, ndistinct, mcv) ON a, b FROM t;` then `ANALYZE t`.
- Error from functions/expressions on columns: planner has no stats; use an expression index (which also collects stats) or rewrite.
- Estimates correct but the plan is slow: cost parameters mismatch the hardware (`random_page_cost` for SSD is a common tuning discussion; change per session first and test).

## Generic vs custom plans

`EXPLAIN (GENERIC_PLAN)` (PG 16+) shows the plan for parameter placeholders without values. If a prepared statement is fast with literals but slow in the application, compare custom and generic plans, and consider `plan_cache_mode` for the session. Application-side: ORMs and drivers may switch to a generic plan after several executions.

## What EXPLAIN ANALYZE does not tell you

- Lock waiting time before execution starts. Check `pg_stat_activity` wait events and `log_lock_waits`.
- Client network and deserialisation. PG 17 `SERIALIZE` measures the server-side conversion of output; client time remains outside.
- Cache temperature. Run twice and report both, or use `Buffers` to reason about it.
- Timing overhead. `TIMING ON` adds per-node clock cost; for very fast nodes with many loops use `TIMING OFF` to see row counts without distortion.

## auto_explain

`auto_explain` (contrib module) logs plans for statements slower than `auto_explain.log_min_duration`. Settings such as `log_analyze` and `log_buffers` add overhead; `log_analyze` instruments every statement. Enable in a session first (`LOAD 'auto_explain'`, superuser) or with a conservative threshold, and treat logs as sensitive because plans may contain literal values.
