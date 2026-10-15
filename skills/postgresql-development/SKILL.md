---
name: postgresql-development
description: >
  Design, optimize, and migrate production PostgreSQL databases using advanced
  PostgreSQL features. Use when indexing JSONB columns with GIN, diagnosing query
  plans with EXPLAIN (ANALYZE, BUFFERS), writing zero-downtime migrations with
  CREATE INDEX CONCURRENTLY, configuring Row-Level Security (RLS), or tuning
  transaction isolation levels.
compatibility: >
  Agent Skills-compatible coding agents administering or writing queries for
  PostgreSQL 14+ databases.
metadata:
  author: michaelweissdev
  version: "1.0.0"
  tags: "postgresql, postgres, jsonb, explain, gin, rls, migrations, sql"
  topics: "databases, software-development"
---

# PostgreSQL Advanced Development & Optimization

PostgreSQL is an advanced open-source object-relational database. Beyond standard SQL, PostgreSQL offers specialized indexing strategies (GIN, GiST, BRIN), rich native data types (`JSONB`, `UUID`, `ARRAY`, ranges), Row-Level Security (RLS), and comprehensive query plan diagnostics (`EXPLAIN ANALYZE`).

## Core Rules

1. **Always use `CREATE INDEX CONCURRENTLY` in production**: Standard `CREATE INDEX` takes an `EXCLUSIVE LOCK`, blocking all concurrent writes to the table.
2. **Never store JSON as plain `TEXT`**: Use `JSONB` for indexed, binary-decomposed JSON operations.
3. **Use `EXPLAIN (ANALYZE, BUFFERS)` to diagnose queries**: Do not guess performance from execution time alone. Inspect buffer cache hits vs physical disk reads.
4. **Be vigilant about table locks during migrations**: Adding a column with a default value without `NOT NULL` is instantaneous in modern Postgres (v11+), but adding constraints or altering column types may rewrite tables and block traffic.
5. **Always use parameterized queries**: Protect against SQL injection and enable query plan caching.
6. **Set query statement timeouts**: Prevent runaway queries from consuming database connections (`SET statement_timeout = '5s'`).

---

## 1. Advanced Data Types: JSONB and GIN Indexing

`JSONB` supports indexed containment (`@>`), key existence (`?`), and field extraction:

```sql
CREATE TABLE audit_events (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    event_type VARCHAR(64) NOT NULL,
    metadata JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Fast containment and key existence indexing with GIN
CREATE INDEX idx_audit_events_metadata_gin ON audit_events USING gin (metadata);

-- Querying using JSON containment operator (@>)
SELECT id, event_type, metadata->>'user_id' AS user_id
FROM audit_events
WHERE metadata @> '{"tenant_id": "cust_441", "status": "failed"}';
```

---

## 2. Diagnosing Queries with `EXPLAIN (ANALYZE, BUFFERS)`

Always analyze query execution plans:

```sql
EXPLAIN (ANALYZE, BUFFERS, VERBOSE, SETTINGS)
SELECT u.id, u.email, COUNT(o.id)
FROM users u
JOIN orders o ON o.user_id = u.id
WHERE u.created_at >= '2026-01-01'
GROUP BY u.id, u.email;
```

Key metrics to evaluate:
- **`Buffers: shared hit=... read=...`**: `hit` means read from RAM cache; `read` means read from slow disk.
- **`Seq Scan vs Index Scan`**: Sequential scans on tables with > 10,000 rows indicate missing or unusable indexes.
- **Estimated Rows vs Actual Rows**: A large discrepancy (e.g. estimated 1 row, actual 500,000 rows) indicates stale table statistics. Run `ANALYZE <table_name>;`.

---

## 3. Zero-Downtime Safe Migrations

### Creating Indexes Without Blocking Writes
```sql
-- Safe: executes without locking reads or writes
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_orders_customer_date
ON orders (customer_id, ordered_at DESC);
```
*(Note: `CONCURRENTLY` cannot be executed inside a multi-statement transaction block `BEGIN...COMMIT`.)*

### Adding Foreign Keys Safely
Adding a foreign key with validation can lock a massive table for minutes:
```sql
-- Step 1: Add constraint without validating existing rows (instant metadata lock)
ALTER TABLE orders
ADD CONSTRAINT fk_orders_customer_id
FOREIGN KEY (customer_id) REFERENCES customers(id) NOT VALID;

-- Step 2: Validate existing rows concurrently (does not block writes)
ALTER TABLE orders VALIDATE CONSTRAINT fk_orders_customer_id;
```

---

## 4. Multi-Tenant Security: Row-Level Security (RLS)

Enforce data isolation directly in PostgreSQL rather than trusting application code:

```sql
-- Enable RLS on the table
ALTER TABLE documents ENABLE ROW LEVEL SECURITY;

-- Force RLS even for table owners
ALTER TABLE documents FORCE ROW LEVEL SECURITY;

-- Policy: Users can only see documents belonging to their tenant
CREATE POLICY tenant_isolation_policy ON documents
    FOR ALL
    USING (tenant_id = current_setting('app.current_tenant_id', true)::uuid);
```

Application sets context before query:
```sql
BEGIN;
SET LOCAL app.current_tenant_id = '9a8b7c6d-0000-0000-0000-000000000000';
SELECT * FROM documents; -- Automatically filters out other tenants!
COMMIT;
```

---

## 5. Common Mistakes and Anti-Patterns

| Anti-Pattern | Performance / Downtime Risk | Correct Practice |
| :--- | :--- | :--- |
| `CREATE INDEX` without `CONCURRENTLY` | Blocks all table writes during index build | Always use `CREATE INDEX CONCURRENTLY` in production |
| Using `COUNT(*)` without WHERE on huge tables | Full table sequential scan every time | Use cached counts or approximate stats (`reltuples`) |
| Storing UUIDs as `VARCHAR(36)` | Wastes 20 bytes per row + slow index comparisons | Use native `UUID` type (16 bytes) |
| Using `OFFSET 10000` for pagination | Database scans and discards 10,000 rows | Use keyset/cursor pagination (`WHERE id > last_seen_id`) |
| Unbounded `IN (...)` with thousands of IDs | Plan explosion and memory exhaustion | Use `WHERE id = ANY($1::bigint[])` |

---

## 6. Verification Checklist

- [ ] New production indexes created with `CONCURRENTLY`.
- [ ] Queries analyzed with `EXPLAIN (ANALYZE, BUFFERS)` to verify index usage.
- [ ] UUIDs, IP addresses, and JSON payloads use native Postgres types (`UUID`, `CIDR`, `JSONB`).
- [ ] Tables analyzed after large bulk inserts (`ANALYZE table_name;`).
- [ ] Foreign keys have matching indexes on child tables.
