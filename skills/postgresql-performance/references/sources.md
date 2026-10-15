# Sources and provenance: postgresql-performance

Consulted 2026-10-15. All text in this skill is original.

## Official sources
- https://www.postgresql.org/docs/current/sql-explain.html (PostgreSQL 18 manual) - EXPLAIN options, defaults, BUFFERS automatic with ANALYZE in 18, MEMORY, SERIALIZE, GENERIC_PLAN restrictions. Introduction versions of individual options (SETTINGS 12, WAL 13, GENERIC_PLAN 16, SERIALIZE 17, MEMORY 17) come from release history knowledge, not from that page; verify against release notes if exactness matters.
- https://www.postgresql.org/docs/current/pgstatstatements.html - column names, parameters, reset function signature, queryid caveats.
- https://www.postgresql.org/docs/current/sql-createindex.html - CONCURRENTLY behaviour and invalid-index recovery.
- Explicit Locking, monitoring statistics, routine vacuuming, and auto_explain chapters of the PostgreSQL manual (from prior knowledge; not re-fetched this session, so the diagnostic queries are standard catalog queries that were not executed against a live server here - no psql was available locally).

## External repositories (ideas only)
- supabase/agent-skills - license MIT (checked via GitHub API). Looked at the topic list of its Postgres best-practices skill (query performance, connections, locking, monitoring) to check coverage. No text copied.
- huggingface/skills - not relevant to this skill.

## Not verified
- Diagnostic SQL was not run against a database. Syntax follows documented catalog views.
