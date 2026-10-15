# Migration Locking Cheat Sheet

Verify against the "Explicit Locking" and `ALTER TABLE`/`CREATE INDEX` pages of the manual for your major version before relying on a row here. Lock names: ACCESS EXCLUSIVE blocks everything including reads; SHARE blocks writes; SHARE UPDATE EXCLUSIVE blocks other schema changes and vacuum but not reads/writes.

| Operation | Lock / cost | Safe pattern |
| :--- | :--- | :--- |
| `CREATE INDEX` | SHARE: blocks writes for the build | `CREATE INDEX CONCURRENTLY` (no transaction block; may leave INVALID index on failure) |
| `DROP INDEX` | ACCESS EXCLUSIVE (brief) | `DROP INDEX CONCURRENTLY` |
| `REINDEX` | Blocks writes | `REINDEX ... CONCURRENTLY` (PostgreSQL 12+) |
| `ADD COLUMN` with constant default | Brief ACCESS EXCLUSIVE, no rewrite (PG 11+) | Fine; set `lock_timeout` |
| `ADD COLUMN` with volatile default | Table rewrite | Add column without default, backfill in batches, then set default |
| `SET NOT NULL` | Full scan under strong lock | Validated `CHECK (col IS NOT NULL)` first (PG 12+ skips the scan), then `SET NOT NULL`, then drop check |
| `ADD FOREIGN KEY` | Locks both tables while validating | `ADD ... NOT VALID`, then `VALIDATE CONSTRAINT` |
| `ADD CHECK` | Scans table under strong lock | `ADD CONSTRAINT ... CHECK (...) NOT VALID`, then `VALIDATE CONSTRAINT` |
| `ALTER COLUMN TYPE` | Often rewrites table | New column, dual-write, backfill, swap, drop |
| `ADD UNIQUE` | Builds index under lock | `CREATE UNIQUE INDEX CONCURRENTLY`, then `ADD CONSTRAINT ... UNIQUE USING INDEX` |
| `VACUUM FULL`, `CLUSTER` | ACCESS EXCLUSIVE rewrite | Avoid in production; use regular vacuum or `pg_repack`-style tools only with approval |

## Lock queue rule

A statement waiting for a lock blocks everything that queues behind it. Run DDL with:

```sql
SET lock_timeout = '3s';
SET statement_timeout = '15min';  -- generous but bounded for long builds
```

and retry with backoff when `lock_timeout` fires (SQLSTATE `55P03`).

## Backfill pattern

Update in batches of a few thousand rows keyed on an indexed column, committing between batches, so you do not hold row locks or bloat WAL in one transaction. Throttle if replicas lag.

## Rehearsal

Test the migration on a restored copy at production size. Record the elapsed time and the locks seen in `pg_locks` during the run. Have a rollback plan that is itself tested (dropping a half-built concurrent index is safe; reversing a data backfill may not be).
