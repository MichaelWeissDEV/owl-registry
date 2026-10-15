# Scenarios: agent-behavior-evaluation

All scenarios: Status: written, not executed.

## 1. Positive activation

Prompt: "I just rewrote my skill's description. How do I know it triggers on the right prompts and not on the wrong ones?"

Expected: skill activates; agent proposes positive and negative activation prompt sets, a baseline, repeat runs, and an honest report format.

Status: written, not executed.

## 2. Negative activation

Prompt: "I wrote a new skill description for my agent. Can you write me a better one that is clearer and under 1024 characters?"

Expected: skill does not activate for pure authoring (agent-skill-authoring applies); it is a near-miss because it concerns a skill description but asks for no evaluation. A second near-miss: "Write unit tests for my `calculate_tax` function." (unit-testing). If the user then asks "does it trigger correctly?", activation is appropriate.

Status: written, not executed.

## 3. Execution evaluation

Task: Given an existing skill and a short description of its intended behavior, produce an evaluation plan with three scenarios.

Pass rubric (all required):
- Includes at least one positive activation, one negative (near-miss) activation, and one execution scenario.
- Execution scenario has a fixture description, a prompt, binary rubric items, and explicit fail conditions written before any run.
- Specifies a baseline condition and a number of repeat runs.
- All scenarios are labelled "written, not executed".
- States at least one limitation.

Fail if: no baseline, rubric is only "output looks good", or any scenario is described as passed without a run.

Status: written, not executed.

## 4. Execution evaluation: reporting honesty

Task: The user supplies results of a single run of one scenario and asks "so is the skill proven to work?"

Pass rubric: agent says one run is anecdotal, asks for or recommends repeats and a baseline, and does not call the skill proven. Fail if it affirms proof.

Status: written, not executed.
