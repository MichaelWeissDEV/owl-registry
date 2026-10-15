# PostgreSQL Troubleshooting (read-only diagnostics)

All queries below only read catalog or statistics views. They need appropriate privileges (`pg_monitor` role is enough for most).

## Who is blocking whom

```sql
SELECT pid,
       pg_blocking_pids(pid) AS blocked_by,
       state, wait_event_type, wait_event,
       now() - xact_start AS xact_age,
       left(query, 120) AS query
FROM pg_stat_activity
WHERE cardinality(pg_blocking_pids(pid)) > 0;
```

Then inspect the blocker's `state`. `idle in transaction` with an old `xact_start` is the classic cause: fix the application (close transactions), do not just terminate sessions in production without approval.

## Long-running and idle-in-transaction sessions

```sql
SELECT pid, usename, state, now() - xact_start AS xact_age, left(query, 100) AS query
FROM pg_stat_activity
WHERE xact_start IS NOT NULL
ORDER BY xact_start
LIMIT 20;
```

## Invalid indexes left by a failed CONCURRENTLY build

```sql
SELECT indexrelid::regclass AS index, indrelid::regclass AS table
FROM pg_index WHERE NOT indisvalid;
```

Drop with `DROP INDEX CONCURRENTLY` (after confirming it is not in use by a build in progress) and rebuild.

## Slow query triage

1. Capture the actual statement with real parameter values (`pg_stat_statements` if installed shows normalized text and timing).
2. Run `EXPLAIN (ANALYZE, BUFFERS)` (inside a rolled-back transaction for writes).
3. Compare estimated vs actual rows. Big gap: `ANALYZE`, raise the column statistics target, or `CREATE STATISTICS` for correlated columns.
4. Check the filter shape: function on the column, implicit cast, `LIKE '%x'`, or composite index with the wrong leading column prevent index use.
5. Check that autovacuum keeps up: `n_dead_tup` and `last_autovacuum` in `pg_stat_user_tables`.
6. Change one thing, re-measure, keep the before/after plans.

## Table and index bloat signals

High `n_dead_tup` relative to `n_live_tup`, table size growing while row count is flat, or sequential scans slowing over time. Remedies: tune autovacuum per table, fix long transactions that hold back cleanup. `VACUUM FULL` locks the table exclusively and rewrites it; avoid in production without approval.

## Connection exhaustion

`FATAL: sorry, too many clients already` or pool timeouts: count sessions by state in `pg_stat_activity`, look for leaked `idle in transaction` sessions, and use a pooler sized to CPU count rather than raising `max_connections` blindly.

## Deadlocks (SQLSTATE 40P01) and serialization failures (40001)

Both are retryable. Deadlocks: make all code paths take row locks in the same order. Serialization failures: retry the whole transaction with bounded attempts and jitter.

## RLS "returns no rows" or "returns other tenants' rows"

- No rows: the tenant setting is unset or empty, or the role lacks table privileges. Check `SELECT current_setting('app.current_tenant_id', true)` in the same transaction.
- Other tenants' rows: the session role is a superuser, owner without `FORCE`, or has `BYPASSRLS`; or the query goes through a view without `security_invoker`. Confirm with `SELECT rolsuper, rolbypassrls FROM pg_roles WHERE rolname = current_user;`.
