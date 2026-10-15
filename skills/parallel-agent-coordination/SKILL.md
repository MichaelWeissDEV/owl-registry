---
name: parallel-agent-coordination
description: >
  Split work across multiple concurrent AI agents or subagents safely: decide whether
  parallelism is worth it, partition work by file ownership, write self-contained
  briefs, isolate with git worktrees, merge results, and verify the integrated
  whole. Use when a task has independent parts, when delegating to subagents, when
  several agents share one repository, or when reconciling their outputs. Not for
  sequential or tightly coupled work, single-agent planning (see implementation-planning),
  or worktree command mechanics (see git-branching-worktrees).
compatibility: >
  Agent runtimes that can launch subagents or multiple sessions. Git worktree
  examples require git 2.17 or newer (`git worktree add` exists since 2.5, but `git worktree remove` arrived in 2.17).
metadata:
  author: michaelweissdev
  version: "1.0.0"
  tags: "multi-agent, subagents, parallelism, delegation, worktrees, coordination"
  topics: "ai-agents, software-development, devtools"
---

# Parallel Agent Coordination

Parallel agents multiply throughput only when their work is genuinely independent. Otherwise they multiply conflicts, duplicated effort, and unverified claims. This skill covers when to fan out, how to partition so agents cannot collide, how to brief them, and how to integrate and verify their results.

Related skills: [implementation-planning](../implementation-planning/SKILL.md) (find the independent steps first), [git-branching-worktrees](../git-branching-worktrees/SKILL.md) (commands for worktrees), [git-merge-conflicts](../git-merge-conflicts/SKILL.md) (when merges collide), [verification-before-completion](../verification-before-completion/SKILL.md) (never trust a subagent summary), [code-review](../code-review/SKILL.md). Depth: [brief template](references/brief-template.md), [scenarios](references/scenarios.md), [sources](references/sources.md).

## When to use

- A plan has two or more steps touching disjoint files or modules.
- Research, search, or analysis can be split by question or directory.
- Independent review or verification by a fresh agent adds value.

## When not to use

- Steps depend on each other's output or edit the same files.
- The task is small enough that briefing costs more than doing it.
- You cannot state the boundaries of each part. Plan first.

## Non-negotiable rules

1. **One owner per file.** No two agents write the same path. Shared files (lockfiles, indexes, generated artifacts, central registries) are owned by exactly one agent or by the coordinator, after the others finish.
2. **Isolate writers.** Give each writing agent its own worktree or branch so a mistake stays local. Read-only agents need no isolation.
3. **Briefs are self-contained.** A subagent has none of your context. State goal, boundaries, constraints, and expected output format explicitly.
4. **Bound authority.** Each brief lists forbidden actions. By default: no pushes, no force operations, no remote changes, no edits outside owned paths, no installing global software, no touching credentials. Pass these limits down; never widen them beyond what the user authorized.
5. **Subagent output is a claim.** The coordinator inspects diffs and re-runs checks before reporting anything as done.
6. **The coordinator owns integration.** Merging, conflict resolution, and the final full-suite verification are not delegated away without checking.
7. **Never delegate secrets.** Do not put tokens or private data in briefs; subagents inherit only what they need.

## Workflow

### 1. Test for independence

For each candidate part ask: Which files does it write? What does it read that another part writes? Could it finish with the others absent? If any answer is unclear, serialize those parts.

### 2. Partition by ownership

Produce a table: part, owned paths, read-only inputs, forbidden paths, deliverable. Assign shared files to the coordinator. Prefer partitioning by module or directory over by feature slice cutting across files.

### 3. Decide the count

More agents is not better. Stay near the number of truly independent parts, limited by what you can review. Reviewing each result costs coordinator attention; budget for it.

### 4. Isolate and brief

Create one worktree per writing agent (see [git-branching-worktrees](../git-branching-worktrees/SKILL.md)):

```bash
git worktree add ../task-a -b task-a-branch
git worktree add ../task-b -b task-b-branch
```

Write each brief from the [brief template](references/brief-template.md): goal, owned paths, constraints, checks to run, report format that separates verified facts from guesses.

### 5. Run, then collect

Wait for reports. If an agent reports a blocker outside its boundary, decide centrally: expand its ownership, defer the item, or handle it yourself. Do not let agents negotiate edits to each other's files.

### 6. Review each result independently

For each branch: read the diff (`git diff main...task-a-branch --stat`, then content), confirm it stayed inside owned paths, and re-run its checks yourself.

### 7. Integrate and verify the whole

Merge one branch at a time, running checks after each. A suite that passes per branch can fail combined (semantic conflicts without textual ones). Run the full verification last, then follow verification-before-completion.

### 8. Clean up

Remove temporary worktrees and branches you created, only after merges are confirmed: `git worktree remove ../task-a`. Do not delete branches the user created.

## Worked example

Plan: add input validation to three independent CLI subcommands (`init`, `sync`, `export`), plus update a shared `CHANGELOG.md`.

| Part | Owns | Reads | Deliverable |
| --- | --- | --- | --- |
| A | `cli/init.py`, `tests/test_init.py` | `cli/common.py` | branch + test results |
| B | `cli/sync.py`, `tests/test_sync.py` | `cli/common.py` | branch + test results |
| C | `cli/export.py`, `tests/test_export.py` | `cli/common.py` | branch + test results |
| Coordinator | `CHANGELOG.md`, `cli/common.py` | all | merged result |

All three need a new helper in `cli/common.py`. That shared file would create a conflict, so the coordinator adds the helper first, commits it, and only then creates the worktrees from that commit. Agents merge back one at a time; the coordinator writes the changelog entry last and runs the full suite.

## Anti-patterns

- **Shared-file free-for-all.** Two agents editing one module or the same lockfile.
- **Under-specified brief.** "Fix the tests" with no scope; the agent wanders.
- **Trusting the summary.** Merging a branch because its report sounded confident.
- **Parallelizing coupled work.** Splitting a refactor and its callers across agents.
- **Fan-out for its own sake.** Ten agents where two would do.
- **Silent scope creep.** Agents "helpfully" editing outside owned paths.
- **Unbounded authority.** Briefs that permit pushing or destructive cleanup.
- **Merging all at once.** Hiding which branch broke the build.

## Verification checklist

- [ ] Independence of parts was checked, not assumed.
- [ ] Every path has exactly one owner; shared files assigned to the coordinator.
- [ ] Each brief is self-contained and lists forbidden actions.
- [ ] Each writing agent worked in its own worktree or branch.
- [ ] Every diff was read and stayed inside owned paths.
- [ ] Checks were re-run by the coordinator, per branch and combined.
- [ ] Temporary worktrees/branches created for this task were cleaned up safely.
- [ ] Final report separates verified results from unverified ones.
