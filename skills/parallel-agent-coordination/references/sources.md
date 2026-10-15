# Sources and provenance

## Consulted

- Agent Skills specification, https://agentskills.io/specification (fetched 2026-10-15): format only.
- Git documentation for `git worktree add` (`add` available since git 2.5; `remove` first appears in the 2.17.0 git-worktree documentation and is absent from 2.16.0, checked 2026-10-15): used for the command forms shown; commands are the standard documented forms `git worktree add <path> -b <branch>` and `git worktree remove <path>`. Verify against `git worktree --help` locally.
- obra/superpowers (https://github.com/obra/superpowers), license MIT (Copyright 2025 Jesse Vincent; confirmed from the raw LICENSE file). Consulted only for the general idea of dispatching independent work to subagents. No text copied. Decision: ideas only.

## Provenance

All text is original, derived from general concurrent-development practice (ownership partitioning, isolation, integration testing).
