# Scenarios: postgresql-performance

All scenarios: Status: written, not executed.

## 1. Positive activation
Status: written, not executed

Prompt: "This query takes 3 seconds in prod, here's the EXPLAIN ANALYZE output. What's wrong?" (plan pasted, shows Seq Scan with Rows Removed by Filter).
Expected: skill activates; agent reads estimate vs actual, buffers, identifies lever, asks for version and data size if missing, proposes index with CONCURRENTLY and defers rollout details to database-migrations.

Prompt: "Which queries are using the most database time?" Expected: pg_stat_statements ranking by total_exec_time with column-name version note.

## 2. Negative activation
Status: written, not executed

Prompt: "Design a Postgres schema for a multi-tenant SaaS with row-level security." Expected: do not activate; postgresql-development applies.

Prompt: "Write a SQL query joining three tables with window functions." Expected: sql-development, not this skill.

Prompt: "Why is my Elasticsearch query slow?" Expected: elasticsearch-search.

## 3. Execution evaluation
Status: written, not executed

Task: Given a plan showing `Nested Loop` with an inner `Seq Scan on line_items (loops=48000)` and `Rows Removed by Filter: 2,000,000` per loop, produce a diagnosis and recommendation.

Pass:
- Identifies per-loop multiplication (time x loops) as the dominant cost.
- Recommends an index on the inner join key (e.g. `line_items(order_id)`) and states estimated write cost.
- Uses `CREATE INDEX CONCURRENTLY` and mentions that failure leaves an INVALID index.
- Requests after-measurement with the same EXPLAIN options and states version-dependent BUFFERS behaviour correctly.
- Does not run or suggest `enable_seqscan = off` as the fix.

Fail: recommends indexes on every filtered column, quotes cost units as milliseconds, runs EXPLAIN ANALYZE on a DELETE without a transaction and rollback, or resets statistics without authorization.
