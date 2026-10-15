---
name: agent-behavior-evaluation
description: >
  Design and run small, honest evaluations of whether an AI agent or Agent Skill
  changes behavior as intended: activation tests (should and should not trigger),
  execution tests with pass/fail rubrics, baseline comparison, repeat runs, and
  reporting that never overstates what was tested. Use when authoring or revising a
  skill or system prompt, comparing agent behavior with and without a skill, writing
  scenarios.md files, or triaging regressions in agent output. Not for writing the
  skill itself (see agent-skill-authoring) or unit-testing application code (see
  unit-testing).
compatibility: >
  Any environment where an agent can be run on fixed prompts in isolated sessions.
  Optional scripting (Python 3 or shell) for aggregating results.
metadata:
  author: michaelweissdev
  version: "1.0.0"
  tags: "evaluation, evals, agent-skills, testing, ai-agents, quality"
  topics: "ai-agents, testing, devtools"
---

# Agent Behavior Evaluation

Agent behavior is stochastic and context-dependent, so "I tried it once and it worked" is weak evidence. This skill gives a lightweight, rigorous method: define expected behavior as checkable rubrics, run against a baseline, repeat, and report exactly what was and was not tested.

Related skills: [agent-skill-authoring](../agent-skill-authoring/SKILL.md) (writing the skill under test), [verification-before-completion](../verification-before-completion/SKILL.md) (evidence standards), [unit-testing](../unit-testing/SKILL.md) (deterministic code tests), [skill-security-audit](../skill-security-audit/SKILL.md) (safety review of skills). Depth: [rubric patterns](references/rubric-patterns.md), [scenarios](references/scenarios.md), [sources](references/sources.md).

## When to use

- You wrote or changed a skill, prompt, or agent configuration and want to know if it helps.
- A skill triggers too often, too rarely, or at the wrong times.
- You need `scenarios.md` entries or a regression set for agent behavior.
- Comparing two versions of instructions.

## When not to use

- Verifying deterministic code: write unit tests.
- Judging one-off output quality for a user task: that is review, not evaluation.
- Security vetting of third-party skills: use skill-security-audit.

## Non-negotiable rules

1. **Never claim a test you did not run.** Mark every scenario as written-not-executed until it was run, and record when, with which agent/model, and how many times.
2. **Define pass/fail before looking at output.** Rubrics written after seeing results bend to fit them.
3. **Always have a baseline.** Run the same task without the skill (or with the previous version). Improvement is a difference, not an absolute.
4. **Run in isolation.** Fresh sessions, no leaked context, no files from a previous attempt. State the setup.
5. **One run is an anecdote.** Repeat where variance matters and report counts ("4 of 5"), not impressions.
6. **Evaluations are safe by construction.** Use scratch directories and fixtures; no real credentials, production systems, or destructive commands. Do not give the agent real secrets to see if it leaks them; use obvious dummy values.
7. **Report limits.** State sample size, what the rubric cannot detect, and known confounds.

## Workflow

### 1. State the behavior under test

One sentence: "With the skill, the agent verifies before claiming done." If you cannot state it, you cannot test it.

### 2. Write three kinds of scenarios

- **Positive activation**: prompts that should trigger the skill (include indirect phrasings that never name it).
- **Negative activation**: near-miss prompts that should not trigger it (adjacent topics, trivial versions).
- **Execution**: a small concrete task with fixtures and a rubric.

Aim for realistic prompts, including messy ones. Keep each scenario small enough to run in minutes.

### 3. Write rubrics as observable checks

Prefer binary, mechanically checkable items ("ran a test command after the last edit", "did not modify test files") over graded quality ("good explanation"). Add a small number of graded items only when needed, with anchors for each score. Include **fail conditions** explicitly. See [rubric patterns](references/rubric-patterns.md).

### 4. Prepare fixtures

A scratch repo or directory with the minimum needed state. Version the fixture so reruns are identical. Seed traps the skill is supposed to defend against (a flaky test, a misleading comment).

### 5. Run baseline and treatment

Same prompt, same fixture, same agent settings. Alternate order or randomize to avoid drift. Capture the transcript or tool-call log, not only the final message, because many rubric items concern process.

### 6. Score and aggregate

Score against the rubric, ideally by someone who did not write the skill, or by a second pass with a different method (a mechanical check plus a human read). If you use an LLM as grader, give it the rubric, validate it on a few known pass/fail transcripts, and spot-check its verdicts.

### 7. Diagnose and iterate

For each failure, locate the cause: description did not trigger, instruction ambiguous, instruction buried, conflicting guidance, or the task exceeded the agent. Change one thing, rerun the affected scenarios plus a few unchanged ones to catch regressions.

### 8. Report honestly

Include: what was run, how many times, baseline vs treatment counts, failures, what was not tested. Update scenario statuses accordingly.

## Worked example

Skill under test: `verification-before-completion`. Behavior: agent reruns tests after the last edit and reports skipped tests.

- Fixture: tiny repo; one failing test (off-by-one) and three skipped tests.
- Prompt: "Fix the failing pagination test and tell me when it's done."
- Rubric (binary): ran tests after final edit; quoted pass and skip counts; mentioned skips as a gap; did not edit test assertions.
- Runs: 5 baseline, 5 with skill, fresh sessions.
- Result recorded: baseline 1/5 passed all four items; treatment 4/5. The one treatment failure never mentioned skips.
- Diagnosis: the skip-reporting instruction was in a paragraph, not in the checklist. Moved it to the report format and reran only that scenario (5/5).
- Limits stated: one fixture, one model, graded by the author; the numbers are illustrative of method, not a benchmark.

(The numbers above are an illustrative example of reporting format, not results of a real run.)

## Anti-patterns

- **Happy-path only.** No negative activation tests, so over-triggering goes unseen.
- **Rubric after the fact.** Defining success post hoc.
- **No baseline.** Crediting the skill for what the model does anyway.
- **Single run.** Declaring victory from one lucky transcript.
- **Grading the final message only.** Missing process violations.
- **Overfitting.** Tuning instructions to the exact test prompts.
- **Leaky fixtures.** Answers or prior attempts left in the working directory.
- **Fake results.** Writing "passed" for scenarios never executed.

## Verification checklist

- [ ] Behavior under test stated in one sentence.
- [ ] Positive, negative, and execution scenarios exist.
- [ ] Rubrics are mostly binary and include fail conditions, written before running.
- [ ] A baseline was run under identical conditions.
- [ ] Runs were isolated; fixtures are versioned.
- [ ] Counts and conditions are reported, not impressions.
- [ ] Scenario statuses are truthful (executed vs written only).
- [ ] No real secrets or production systems were involved.
- [ ] Limitations are stated.
