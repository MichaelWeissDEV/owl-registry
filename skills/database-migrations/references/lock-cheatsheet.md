# Lock cheat sheet

## PostgreSQL (verified against the PostgreSQL 18 ALTER TABLE / CREATE INDEX manuals, 2026-10-15)

| Operation | Lock | Blocks writes? | Notes |
|---|---|---|---|
| `ALTER TABLE` default forms | ACCESS EXCLUSIVE | reads and writes | Strictest subcommand wins |
| `ADD COLUMN` (non-volatile default) | ACCESS EXCLUSIVE, brief | momentarily | No rewrite |
| `ADD COLUMN` volatile default / identity / stored generated | ACCESS EXCLUSIVE, long | yes, for the rewrite | Full table and index rewrite |
| `ALTER COLUMN TYPE` (needs conversion) | ACCESS EXCLUSIVE, long | yes | Rewrite, up to 2x disk |
| `ADD CONSTRAINT CHECK ... NOT VALID` | ACCESS EXCLUSIVE, brief | momentarily | No scan; new writes are checked |
| `ADD FOREIGN KEY` (validating) | SHARE ROW EXCLUSIVE on both tables | writes | Scans; use NOT VALID |
| `ADD FOREIGN KEY ... NOT VALID` | SHARE ROW EXCLUSIVE | brief | No scan |
| `VALIDATE CONSTRAINT` | SHARE UPDATE EXCLUSIVE (+ROW SHARE on referenced table for FK) | no | Concurrent DML continues |
| `SET NOT NULL` | ACCESS EXCLUSIVE | yes while scanning | Skips scan if a valid CHECK proves it |
| `CREATE INDEX` | SHARE | writes | Reads allowed |
| `CREATE INDEX CONCURRENTLY` | SHARE UPDATE EXCLUSIVE (per the explicit-locking chapter) | no | Two scans, waits for old transactions, not in a transaction block |
| `REINDEX CONCURRENTLY` | SHARE UPDATE EXCLUSIVE | no | Builds new index then swaps |
| `ATTACH PARTITION` | SHARE UPDATE EXCLUSIVE on parent; ACCESS EXCLUSIVE on child and default partition | no on parent | Add matching CHECK first to skip scan |
| `DETACH PARTITION CONCURRENTLY` | SHARE UPDATE EXCLUSIVE then ACCESS EXCLUSIVE on partition | brief | Not in a transaction; `FINALIZE` completes an interrupted one |
| `SET (fillfactor, autovacuum_*, ...)` | SHARE UPDATE EXCLUSIVE | no | |
| `DROP COLUMN` | ACCESS EXCLUSIVE | brief | Fast, but breaks readers |
| `RENAME` | ACCESS EXCLUSIVE | brief | Breaks any code using the old name |

The SHARE UPDATE EXCLUSIVE level of CREATE INDEX CONCURRENTLY is from the Explicit Locking chapter; the CREATE INDEX page itself says only that it takes no locks that prevent concurrent inserts, updates or deletes.

### Queue effect
A lock request that cannot be granted waits in a queue, and later requests (even plain SELECTs) queue behind it if they conflict with the waiting request. A single ACCESS EXCLUSIVE `ALTER` stuck behind a long-running transaction can therefore stall all traffic on the table. Mitigation: `SET lock_timeout`, check for long transactions first, retry.

### Useful checks
```sql
-- invalid indexes left by a failed CONCURRENTLY build
SELECT indexrelid::regclass AS index, indrelid::regclass AS tbl
FROM pg_index WHERE NOT indisvalid;

-- long-running transactions that would block DDL
SELECT pid, state, now() - xact_start AS age, left(query, 80) AS query
FROM pg_stat_activity WHERE xact_start IS NOT NULL ORDER BY xact_start LIMIT 10;
```

## MySQL / InnoDB (general guidance; confirm with the manual for your exact version)
- Many `ALTER TABLE` operations support `ALGORITHM=INPLACE` or `INSTANT` and `LOCK=NONE`; specify them explicitly so the statement errors rather than silently falling back to a copying, blocking operation.
- Which operations are instant or in-place varies by version (for example instant `ADD COLUMN` arrived in 8.0). Check the Online DDL operations table for the deployed version.
- Large changes are often done with an external online schema change tool (shadow table plus triggers or binlog). Evaluate replication lag and foreign-key limitations per tool.

## Other engines
SQLite: most alterations rebuild the table; use the documented 12-step recreate procedure. SQL Server / Oracle: online options are edition-dependent. Treat these as "look up the lock behaviour first" and do not assume PostgreSQL rules.
