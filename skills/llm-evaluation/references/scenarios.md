# Scenarios: llm-evaluation

All scenarios: Status: written, not executed.

## 1. Positive activation
Status: written, not executed

- "How do I know whether the new prompt is actually better than the old one?"
- "Set up an LLM-as-judge to grade our support-bot answers."
- "Run MMLU-style benchmarks on this model with lm-eval."
- "Add a quality gate to CI for our summarisation feature."

## 2. Negative activation
Status: written, not executed

- "Deduplicate my training data." -> dataset-quality.
- "What is recall@10 of my vector index?" -> rag-evaluation.
- "Install Ollama and run Llama locally." -> local-llm-deployment.
- "Write pytest tests for this parser." -> unit-testing.

## 3. Execution evaluation
Status: written, not executed

Task: A team reports "prompt B scored 78% vs prompt A 74% on our 100-item eval, so B is better; judged by the same model that generated the answers." Review the claim and propose a corrected evaluation plan.

Pass:
- Computes or states that with n=100 the 95% interval half-width is about 8 points, so a 4-point gap is unresolved; asks for paired analysis and more items.
- Flags self-preference and lack of judge calibration against human labels; proposes position/order control, pinned judge version, and a 50-200 item human-labelled calibration set with agreement reported.
- Asks whether the set was used to tune the prompts; requires a frozen test set.
- States that no data should go to a hosted judge without authorization.
- Does not claim a result; labels the plan as designed, not executed.

Fail: accepts the 4-point gap as significant; recommends BLEU/ROUGE alone; reports `--limit` benchmark runs as final; invents numbers.
