# Scenarios: dataset-quality

All scenarios: Status: written, not executed (the bundled script itself was run once on a 5-line fixture, which is not one of these scenarios).

## 1. Positive activation
Status: written, not executed

- "My classifier gets 99% on the test set, suspiciously high." -> leakage and duplicate checks.
- "Clean this JSONL fine-tuning dataset before we train."
- "Write a dataset card and check for PII before I upload to the Hub."

## 2. Negative activation
Status: written, not executed

- "Convert this CSV from semicolons to commas." -> csv-data-processing.
- "Compare GPT outputs on my prompts with a rubric." -> llm-evaluation.
- "Measure recall@10 of my vector search." -> rag-evaluation.

## 3. Execution evaluation
Status: written, not executed

Task: Provided `train.jsonl` (2,000 rows) and `test.jsonl` (500 rows) with fields id, text, label, where 40 test texts also appear in train (differing in case/whitespace) and 5 train texts appear twice with different labels. Produce an audit and a cleaning plan.

Pass:
- Runs or reproduces the checks (script or equivalent) and reports: exact overlap = 40 rows, conflicting-label identical texts = 5, with row ids rather than full texts.
- Removes overlap from train (or justifies otherwise), keeps source files untouched, writes a removal log.
- Flags group/temporal leakage as a question to ask, not an assumption.
- Does not upload or call external APIs with the data; mentions PII screening.
- Produces dataset-card fields for counts removed.

Fail: edits files in place; reports accuracy gains as success; resamples before splitting; prints raw rows containing personal data.
