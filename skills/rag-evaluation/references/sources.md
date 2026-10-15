# Sources and provenance: rag-evaluation

Consulted 2026-10-15. All text is original.

## Sources
- Information-retrieval metric definitions (recall, precision, MRR, MAP, nDCG with log2 discount): standard textbook definitions (for example Manning, Raghavan, Schuetze, Introduction to Information Retrieval; Jarvelin and Kekalainen 2002 for nDCG). From general knowledge; not re-fetched. Metric arithmetic verified by running scripts/retrieval_metrics.py on a hand-computed fixture.
- RAG evaluation frameworks (Ragas, TruLens, DeepEval): mentioned only as examples. Their metric names and definitions were NOT checked in this session; the skill tells the reader to read definitions in the pinned installed version.
- OWASP guidance on prompt injection (general concept of indirect injection): general knowledge, not fetched.

## External repositories (ideas only)
- huggingface/skills - Apache-2.0 (GitHub API); skill list reviewed, nothing RAG-specific found. No text copied.
- supabase/agent-skills - MIT; has a Supabase Vectors area in its broad skill; not read. No text copied.

## Tested
- scripts/retrieval_metrics.py executed on a 3-line fixture; outputs agree with hand computation (recall@3 0.75, nDCG@3 0.6199, MRR 0.75).
