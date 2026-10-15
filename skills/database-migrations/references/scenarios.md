# Scenarios: database-migrations

All scenarios: Status: written, not executed.

## 1. Positive activation
Status: written, not executed

- "Review this Alembic migration that adds a NOT NULL column with a default to our 200M-row events table."
- "How do I rename a column with zero downtime?"
- "Our `CREATE INDEX CONCURRENTLY` failed and queries got slower - what now?"
Expected: skill activates; lock/rewrite analysis, expand/contract, invalid-index recovery.

## 2. Negative activation
Status: written, not executed

- "Why is this SELECT slow?" -> postgresql-performance.
- "Model a many-to-many relation between users and teams." -> postgresql-development / sql-development.
- "Set up a GitHub Actions pipeline to deploy." -> ci-github-actions / release-engineering.

## 3. Execution evaluation
Status: written, not executed

Task: "Add `orders.currency` (NOT NULL, default 'USD') to a 300M-row PostgreSQL 16 table with live traffic, and add a foreign key to `currencies(code)`."

Pass:
- Notes a constant default is metadata-only (no rewrite) on PG 11+ and so ADD COLUMN is cheap; flags that the NOT NULL is satisfied by the default so no scan is needed for a new column with a default.
- FK added as `NOT VALID`, then `VALIDATE CONSTRAINT` in a separate step, with the correct lock reasoning (SHARE ROW EXCLUSIVE brief, then SHARE UPDATE EXCLUSIVE).
- Sets `lock_timeout` and describes retry.
- Separates any index (CONCURRENTLY, no transaction) and mentions INVALID index handling.
- Does not execute anything against a database; provides rollback/forward-fix notes and a verification query.

Fail: single `ALTER TABLE ... ADD FOREIGN KEY` on the hot table; CONCURRENTLY inside a transaction; no lock_timeout; one unbounded UPDATE backfill when none is needed; claims a rollback exists for lossy changes.
