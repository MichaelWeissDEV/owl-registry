# Subagent brief template

A subagent starts with no memory of your conversation. Everything it needs must be in the brief.

```text
Role: You are implementing part <X> of <overall task>.

Goal: <one or two sentences, outcome not method>

Context you need:
- <relevant facts you already verified, with file paths>
- <conventions: test command, style rules>

You own (may edit): <paths>
Read-only: <paths>
Do not touch: <paths, including shared/generated files>

Constraints:
- Work only in <worktree path> on branch <name>.
- Do not push, force, rebase shared branches, or change any remote.
- Do not install global software or modify system settings.
- Do not read or print credentials or environment secrets.
- Do not delete files outside your owned paths.

Checks to run before reporting: <exact commands>

Report format:
1. Summary (3 lines max)
2. Files changed (list)
3. Commands run and their key output (counts, failures)
4. Verified facts vs. assumptions/guesses (separate lists)
5. Blockers or out-of-scope discoveries (do not act on them)
```

## Tips

- Give the objective and acceptance check, not a line-by-line script; trust the agent for tactics.
- Include what you already ruled out so it does not repeat dead ends.
- Ask for evidence, not adjectives: "report the test counts", not "say if it works".
- For read-only research agents, ask for sources (file paths and line ranges) so you can spot check.
- Keep briefs short enough that the boundaries are the first thing read.

## Spot checks when results arrive

1. `git diff <base>...<branch> --stat`: only owned paths?
2. Re-run the stated checks yourself.
3. Search for leftovers: debug prints, commented-out code, stray files.
4. Compare the report's "verified" list against what you can reproduce.
