# Sources and Provenance

## Official sources consulted

| URL | Used for |
|---|---|
| https://git-scm.com/docs/git-gc | Defaults for `gc.pruneExpire` (2 weeks), `gc.reflogExpire` (90 days), `gc.reflogExpireUnreachable` (30 days), `gc.auto` (6700); `--prune=now` risk with concurrent writers; pruning only removes unreachable objects. Fetched 2026-10-15. |
| https://git-scm.com/docs/git-bisect | Exit-code convention for `bisect run` (0 good, 125 skip, 1-127 bad, 128+ abort); from established Git documentation, not re-fetched in this session. |
| https://git-scm.com/docs/git-log, git-blame, git-fsck, git-reflog | Option semantics (`-S`, `-G`, `-L`, `--follow`, `blame -w -C`, `fsck --lost-found`, `--no-reflogs`); from established Git documentation, not re-fetched in this session. |

Items not re-fetched are standard long-stable Git behavior; the commands were not executed against a scratch repo for this skill version (see scenarios, all "written, not executed").

## Provenance

All text is original. External skill repositories (anthropics/skills, obra/superpowers, trailofbits/skills, vercel-labs/agent-skills, huggingface/skills, supabase/agent-skills) were not consulted and nothing was copied. No third-party licenses apply.
