# Scenarios: rag-evaluation

All scenarios: Status: written, not executed.

## 1. Positive activation
Status: written, not executed

- "Our RAG chatbot hallucinates. How do I measure and fix it?"
- "Compare two embedding models and three chunk sizes for our docs search."
- "Compute nDCG@10 and recall@5 for these retrieval runs."
- "Add regression tests so prompt injection through documents is caught."

## 2. Negative activation
Status: written, not executed

- "Tune BM25 analyzers and synonyms in Elasticsearch." -> elasticsearch-search.
- "Compare GPT and Claude on summarisation quality." -> llm-evaluation.
- "Cache LLM responses with Redis." -> redis-caching.
- "Remove duplicates from my training JSONL." -> dataset-quality.

## 3. Execution evaluation
Status: written, not executed

Task: Given runs.jsonl with the two-query fixture in references/metrics-notes.md, compute metrics at k=1 and k=3 and interpret them.

Pass:
- Runs scripts/retrieval_metrics.py (or equivalent) and reports recall@3 = 0.75, nDCG@3 about 0.62, MRR = 0.75, skipping the query with no relevant docs and saying so.
- States the nDCG gain/discount variant used.
- Explains that recall is the priority metric for RAG and that gold labels should be document/section level.
- Proposes the next step as failure attribution by pipeline stage rather than a prompt tweak.

Fail: counts the no-relevant query as 0 silently; mixes gain formulas; recommends judging only end-to-end answers; sends corpus text to a hosted judge without asking.
