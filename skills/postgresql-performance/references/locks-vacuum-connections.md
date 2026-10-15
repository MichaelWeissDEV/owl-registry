# Locks, vacuum, bloat and connections: read-only diagnostics

All queries below only read catalog/statistics views. Acting on the results (terminating sessions, vacuuming, changing settings) needs explicit user authorization.

## Who is waiting and who blocks them

```sql
SELECT a.pid, a.state, a.wait_event_type, a.wait_event,
       now() - a.xact_start AS xact_age,
       pg_blocking_pids(a.pid) AS blocked_by,
       left(a.query, 100) AS query
FROM pg_stat_activity a
WHERE a.datname = current_database()
  AND cardinality(pg_blocking_pids(a.pid)) > 0;
```

Then inspect each blocker pid: `SELECT pid, state, xact_start, query FROM pg_stat_activity WHERE pid = <blocker>;`. A blocker in state `idle in transaction` usually means an application forgot to commit; the fix is in the application (and `idle_in_transaction_session_timeout` as a guard-rail, set deliberately).

Enable `log_lock_waits` (logs waits longer than `deadlock_timeout`, default 1 s) to catch intermittent cases. Table-level lock modes and their conflicts are in the "Explicit Locking" chapter of the manual.

## Long transactions that hold back vacuum

```sql
SELECT pid, state, now() - xact_start AS age, backend_xmin, left(query, 80) AS query
FROM pg_stat_activity
WHERE xact_start IS NOT NULL
ORDER BY xact_start
LIMIT 10;
```
Also check replication slots (`pg_replication_slots`, `xmin`/`catalog_xmin`, `restart_lsn`) and prepared transactions (`pg_prepared_xacts`); an abandoned one pins the xmin horizon and bloats every table.

## Dead tuples and autovacuum

```sql
SELECT relname, n_live_tup, n_dead_tup,
       round(100.0 * n_dead_tup / nullif(n_live_tup + n_dead_tup, 0), 1) AS dead_pct,
       last_autovacuum, last_autoanalyze
FROM pg_stat_user_tables
ORDER BY n_dead_tup DESC
LIMIT 15;
```
- Default `autovacuum_vacuum_scale_factor` is 0.2: on a 500M-row table that is 100M dead rows before vacuum triggers. Set per-table storage parameters (`ALTER TABLE t SET (autovacuum_vacuum_scale_factor = 0.01, autovacuum_vacuum_threshold = 10000);`) - this takes a `SHARE UPDATE EXCLUSIVE` lock and does not block normal traffic.
- `n_dead_tup` is an estimate. For precise bloat use the `pgstattuple` extension on a replica or off-peak; it reads the table.
- `VACUUM FULL` and `CLUSTER` rewrite the table under `ACCESS EXCLUSIVE`; propose `pg_repack`-style online alternatives or partition rotation, and let the user decide.

## Connections

```sql
SELECT state, count(*) FROM pg_stat_activity WHERE backend_type = 'client backend' GROUP BY state ORDER BY 2 DESC;
SHOW max_connections;
```
Many `active` sessions beyond roughly a small multiple of CPU cores means contention; many `idle` is memory cost, not CPU. Use a transaction-mode pooler with awareness of session state (SET, advisory locks, LISTEN, session-level prepared statements behave differently).

## Temp files and work_mem spills

```sql
SELECT datname, temp_files, pg_size_pretty(temp_bytes) AS temp_bytes
FROM pg_stat_database WHERE datname = current_database();
```
Set `log_temp_files = 0` temporarily (or a size threshold) to log which statements spill. Prefer raising `work_mem` per role or session for known heavy reports; remember a single query can use `work_mem` several times (per sort/hash node, per parallel worker).

## Checkpoints and WAL

On PG 17+ use `pg_stat_checkpointer`; on 16 and earlier checkpoint counters are in `pg_stat_bgwriter`. A high ratio of requested to timed checkpoints suggests `max_wal_size` is too small for the write rate. `EXPLAIN (WAL)` (PG 13+) and `pg_stat_statements.wal_bytes` identify which statements generate WAL.
