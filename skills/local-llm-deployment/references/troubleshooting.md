# Troubleshooting local inference

Confirm flag and variable names against the installed version (`ollama --help`, `llama-server --help`); they drift.

| Symptom | Likely cause | Check / fix |
|---|---|---|
| Very slow generation, CPU busy | Model not (fully) offloaded to GPU | `ollama ps` PROCESSOR column; llama.cpp `-ngl` / startup log of offloaded layers; smaller quant or context |
| Slow first response on long prompt | Prompt processing is compute-bound | Reduce context/prompt, enable flash attention, cache prompt prefixes where the server supports it |
| Out of memory on load or on long chats | Weights + KV cache exceed memory | Lower `num_ctx`/`-c`, lower `-np` / `OLLAMA_NUM_PARALLEL`, `OLLAMA_KV_CACHE_TYPE=q8_0` (needs `OLLAMA_FLASH_ATTENTION=1`) or `-ctk q8_0`, smaller quant |
| Model ignores start of a long document | Context shorter than the prompt (Ollama default 4096 per FAQ) | Raise `OLLAMA_CONTEXT_LENGTH` or request `options.num_ctx`; verify the model supports that length |
| Gibberish or role-confused output | Wrong chat template or a base (non-instruct) model | `ollama show <model> --template`; llama.cpp `--jinja` / `--chat-template-file`; use an instruct variant |
| Tool calling not working in llama-server | `--jinja` off (default-on on current master; older builds need the flag) or template lacks tool support | Pass `--jinja` explicitly on older builds; supply a tool-capable template per the server README |
| `/v1/embeddings` errors in llama-server | Server not run with an embedding model/pooling | Use `--embedding` with an embedding model and pooling type other than none |
| Connection refused | Server not running, wrong port (llama.cpp default port differs between builds) | Pass `--port` explicitly; `curl http://127.0.0.1:<port>/health` (llama-server) or `/api/version` (Ollama) |
| Reachable from other machines unexpectedly | Bound to 0.0.0.0 | Rebind to 127.0.0.1, add firewall rules and authentication |
| Model reloads every request | Keep-alive expired or too many models for memory | `OLLAMA_KEEP_ALIVE`, `OLLAMA_MAX_LOADED_MODELS`, per-request `keep_alive` |
| Requests queue or are rejected | Parallelism 1, queue full | `OLLAMA_NUM_PARALLEL`, `OLLAMA_MAX_QUEUE`; remember parallelism multiplies KV memory |
| Quality drop after quantizing | Aggressive quant, requantized file, no importance matrix for IQ types | Quantize from F16/BF16 source, higher bits, use `--imatrix`, evaluate on your task |
| Import of GGUF into Ollama fails or template wrong | Missing template metadata | Provide `TEMPLATE` (Go template) in the Modelfile; `ollama show --modelfile` of a similar model as reference |

## Collecting a useful bug report
Versions (`ollama --version`, `llama-server --version`), OS and hardware, exact command and environment variables (redact keys), model file name and quant, and relevant log lines. Do not paste prompts containing private data.
