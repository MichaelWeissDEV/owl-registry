# Retrieval metric notes

## Hand-computed fixture (matches the bundled script's output)

Two queries (a third, with no relevant document, is skipped):

- q1: relevant = {d1: grade 1, d7: grade 2}; retrieved = [d3, d1, d9]
- q2: relevant = {a}; retrieved = [a]

At k=3:
- Recall@3: q1 = 1 of 2 relevant found = 0.5; q2 = 1.0; macro = 0.75.
- Precision@3: q1 = 1/3; q2 = 1/3 (the script divides by k even when fewer than k results exist); macro = 0.3333.
- MRR: q1 = 1/2 (d1 at rank 2); q2 = 1; macro = 0.75.
- nDCG@3 (linear gain): q1 DCG = 1/log2(3) = 0.6309; ideal order gains [2, 1] gives 2/log2(2) + 1/log2(3) = 2.6309; nDCG = 0.2398. q2 = 1. Macro = 0.6199.

Duplicate case (run as its own file): relevant = [a, b]; retrieved = [a, a, b]; at k=3 recall = 1.0 and precision = 2/3 = 0.6667 (the repeated `a` counts once; a naive count would give 1.0).

Run: `python3 -I scripts/retrieval_metrics.py runs.jsonl --k 1 3`.

## Variants to state explicitly
- **Gain**: linear `rel` (used here) versus exponential `2^rel - 1` (common in learning-to-rank). Exponential emphasises highly relevant documents.
- **Discount**: `1/log2(i+1)` (used here) versus `1/log2(i)` with special-casing the first rank.
- **Recall denominator**: all relevant documents versus relevant documents capped at k (some toolkits cap); state the choice. With many relevant documents and a small k, uncapped recall cannot reach 1.
- **Duplicates**: the script counts a document id once (later repeats get zero gain); real pipelines that return several chunks of the same document should map chunks to document ids first.
- **Unjudged documents**: treated as non-relevant. If gold labels are incomplete (a relevant passage that nobody labelled), metrics are pessimistic; sample top results from the new system and add judgements ("pooling") when comparing systems.

## Choosing k
Use the number of passages you actually put in the prompt. Report recall at a larger candidate depth (for example 50) for the first-stage retriever and at the final k after reranking; the gap is the reranker's loss or gain.

## Groundedness arithmetic
Answer split into 8 atomic claims; 6 supported by retrieved context, 1 contradicted, 1 not found: groundedness = 6/8 = 0.75, contradiction rate = 1/8. Report both; contradictions are worse than unsupported additions.
