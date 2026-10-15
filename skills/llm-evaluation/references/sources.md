# Sources and provenance: llm-evaluation

Consulted 2026-10-15. All text is original.

## Official sources
- https://raw.githubusercontent.com/EleutherAI/lm-evaluation-harness/main/docs/interface.md - subcommands (`run`, `ls`, `validate`), flag names and short forms, legacy form still accepted. Version 0.4.13 from https://pypi.org/pypi/lm-eval/json (released 2026-08-31, MIT, Python >=3.10).
- https://pypi.org/pypi/evaluate/json - Hugging Face evaluate 0.4.6 (2025-09-18); README recommends LightEval as the more actively maintained library.
- Statistics (McNemar, bootstrap, Wilson interval, Cohen's kappa, Krippendorff's alpha, Holm-Bonferroni): standard methods from general knowledge; not fetched.
- LLM-judge biases (position, verbosity, self-preference): widely reported in the research literature (for example the MT-Bench/LLM-as-a-judge work); stated as general guidance, citations not re-fetched.

## External repositories (ideas only)
- huggingface/skills - license Apache-2.0 (GitHub API). Skill list shows `huggingface-community-evals` (inspect-ai and lighteval). Not read in depth; no text copied. Decision: ideas only; this skill is written independently and does not cover inspect-ai or lighteval usage.

## Executed
- scripts/paired_bootstrap.py run on a synthetic 200-item fixture: produced a sensible CI. The lm-eval commands were not executed (lm-eval not installed); flags are taken from the official interface doc.
