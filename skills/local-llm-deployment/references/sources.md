# Sources and provenance: local-llm-deployment

Consulted 2026-10-15. All text is original.

## Official sources
- Ollama FAQ (docs/faq.mdx on the main branch): environment variables and defaults, `ollama ps` PROCESSOR column, `num_ctx` setting methods.
- Ollama Modelfile reference (docs/modelfile.mdx): instructions, PARAMETER defaults, GGUF import via FROM and `ollama create -f`.
- Ollama import guide (docs/import.mdx): "Ollama does not quantize GGUF models during import"; safetensors import.
- Ollama API reference (docs/api.md): endpoints, `/api/embed` replacing `/api/embeddings`, `stream` and `keep_alive` defaults.
- https://docs.ollama.com/api/openai-compatibility: base URL, supported endpoints and request fields, unsupported items.
- Local read-only verification: `ollama --version` = 0.40.3; `ollama --help`, `ollama run --help`, `ollama create --help` (shows `-q/--quantize` for safetensors, example nvfp4), `ollama show --help`, `ollama ps`, `GET /api/version`, `GET /v1/models`, `GET /api/tags` against the running local server. No model was pulled, run, or deleted.
- llama.cpp server README on master (tools/server/README.md): binary `llama-server`, flags, endpoints, default port 9931 and `-lm/--load-mode` as written on master at fetch time (older builds: 8080, `--mlock`). The latest GitHub release tag could not be confirmed reliably, so no llama.cpp version number is stated; confirm with the installed build.
- llama.cpp quantize README (tools/quantize/README.md): quant type names, bits/weight and size table for Llama-3.1-8B, convert_hf_to_gguf.py and llama-quantize usage and options.
- https://huggingface.co/docs/hub/ollama: `ollama run hf.co/<user>/<repo>[:quant]`, default Q4_K_M, private GGUF setup.

## External repositories (ideas only)
- huggingface/skills - license Apache-2.0 (GitHub API). Skill list includes `huggingface-local-models` (llama.cpp/GGUF selection) and `hf-mem` (memory estimation). Not read in depth. Decision: ideas only (memory sizing, GGUF selection as topics); no text copied.
- supabase/agent-skills - MIT; not relevant.

## Not verified
- Memory formulas (KV cache) are standard transformer arithmetic from general knowledge, not tested here.
- `llama-bench` existence and exact options were not checked.
- OLLAMA_* variable behaviour beyond what the FAQ states; chat completions were not executed.
