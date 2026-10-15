# Recovery Playbook

Decision tables for common "I lost it" incidents. Every row starts read-only. Commands marked **(mutates)** need the user's go-ahead when they can lose data; creating a new branch or tag is not destructive.

## Incident table

| Symptom | First read-only check | Likely recovery | Risk to avoid |
|---|---|---|---|
| Commits gone after `reset --hard` | `git reflog` (look for `reset: moving to`) | `git branch recovered/x HEAD@{n}` | Running more resets before recording the sha |
| Commits gone after rebase | `git reflog show <branch>`; `ORIG_HEAD` right after the rebase | Branch from the pre-rebase entry; `git range-diff` old vs new | Assuming `ORIG_HEAD` survives (next rebase/merge overwrites it) |
| Deleted branch (local) | `git reflog` for `checkout: moving from <branch>`; `git fsck --no-reflogs --unreachable` | `git branch <name> <sha>` | `gc --prune=now` |
| Deleted branch (remote, force-push) | `git reflog show origin/<branch>`; teammates' clones | Push recovered branch under a new name | Force-pushing over what others based work on |
| Dropped stash | `git fsck --unreachable --no-reflogs` and look for `WIP on` | `git stash apply <sha>` | `stash pop` (drops again on conflict-free apply) |
| Merge went wrong, not yet pushed | `git reflog`; `git log --merges -n 3` | `git reset --merge ORIG_HEAD` **(mutates, only if tree clean or user agrees)** | Resetting with uncommitted changes you need |
| Bad merge already pushed | `git log --first-parent` | `git revert -m 1 <merge>` (new commit, preserves history) | Rewriting shared history |
| File deleted in some past commit | `git log --diff-filter=D -- <path>` | `git show <sha>^:<path> > recovered_file` | Overwriting an existing file |
| Corrupt object | `git fsck --full` | Copy the repo, fetch from a good remote into the copy | Deleting object files in place |

## Expiry arithmetic

Defaults from current git-gc documentation (verify local config first with `git config --get-regexp '^gc\.'`):

| Setting | Default | Meaning |
|---|---|---|
| `gc.reflogExpire` | 90 days | Reflog entries older than this are expired |
| `gc.reflogExpireUnreachable` | 30 days | Entries not reachable from the ref tip expire sooner |
| `gc.pruneExpire` | 2 weeks | Unreachable loose objects older than this are deleted |
| `gc.auto` | 6700 | Loose-object threshold that triggers `gc --auto`; `0` disables auto gc |

Worst case for an amended/rebased-away commit is roughly 30 days of reflog plus the 2-week object grace, but explicit `git gc --prune=now` or a hosted server's own gc policy can shorten that to zero. Hosting platforms run their own gc; do not assume a server still has an object.

## Preserve step (copy before experimenting)

```bash
# from the directory that contains the repository
cp -a myrepo myrepo.forensic-copy
git -C myrepo config gc.auto 0       # stop automatic gc in the original while investigating
```

Undo later with `git -C myrepo config --unset gc.auto`.

## When history rewriting is genuinely requested

Only after the user explicitly authorizes it, and only after: (1) credentials involved are rotated, (2) a mirror backup exists (`git clone --mirror`), (3) all collaborators are told to re-clone, and (4) the tool and exact command are shown for approval. `git filter-repo` is the upstream-recommended tool over `filter-branch`; it is a separate install and rewrites every commit hash. Even then, forks, caches and pull-request refs on the host may retain old objects.
