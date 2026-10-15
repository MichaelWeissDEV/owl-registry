# Sources and provenance: dataset-quality

Consulted 2026-10-15. All text is original.

## Official / primary sources
- https://pypi.org/project/datasets/ - latest version 5.1.0 (JSON metadata fetched). API calls used (`load_dataset`, `filter`, `train_test_split`, `features`) are long-standing; they were not executed in this session because `datasets` was not installed/run. The note that dataset-script loading was removed in recent major versions is from release knowledge (4.0) and should be re-checked against the datasets release notes.
- https://pypi.org/project/evaluate/ - 0.4.6 (2025-09-18); noted only to decide it is out of scope here.
- Dataset card concept: Hugging Face dataset cards and "Datasheets for Datasets" (Gebru et al.) - used as ideas for the template headings; no text copied.

## External repositories (ideas only)
- huggingface/skills - license Apache-2.0 (GitHub API). Looked at the skill list (a datasets viewer API skill, hf-cli). Decision: ideas only, no text or code copied; this skill is about data quality methodology, which that repo does not cover.
- supabase/agent-skills - MIT; not relevant to this skill.

## Testing performed
- scripts/audit_jsonl.py run on a 5-line fixture (parse error, empty field, duplicate with conflicting label, overlap with a second file): outputs matched expectation. No larger test.
