# Sources and provenance: database-migrations

Consulted 2026-10-15. All text is original.

## Official sources
- https://www.postgresql.org/docs/current/sql-altertable.html (PostgreSQL 18) - lock levels, rewrite rules, NOT VALID/VALIDATE, SET NOT NULL scan skip, partition attach/detach, PG 18 NOT ENFORCED and NOT NULL NOT VALID.
- https://www.postgresql.org/docs/current/sql-createindex.html - CONCURRENTLY phases, restrictions, invalid-index recovery.
- PostgreSQL Explicit Locking chapter (lock-mode names, SHARE UPDATE EXCLUSIVE for CONCURRENTLY) - from prior knowledge, not re-fetched in this session.
- MySQL Online DDL: general statement only; not fetched. Marked as "confirm with your version's manual".
- Tool-specific transaction opt-outs (goose NO TRANSACTION, Flyway executeInTransaction, Alembic autocommit_block) are from prior knowledge and not re-verified; the skill tells the reader to check current tool docs.

## External repositories (ideas only)
- supabase/agent-skills - license MIT (GitHub API). Topic list only (schema design, locking). No text copied.

## Not executed
No SQL in this skill was run against a database (no psql locally).
