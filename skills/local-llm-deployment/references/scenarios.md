# Scenarios: local-llm-deployment

All scenarios: Status: written, not executed.

## 1. Positive activation
Status: written, not executed

- "Run a local LLM on my MacBook and let VS Code talk to it."
- "Which GGUF quantization should I use on 24 GB VRAM?"
- "llama-server crashes with out-of-memory when I raise the context."
- "Import this GGUF into Ollama with a custom system prompt."

## 2. Negative activation
Status: written, not executed

- "Is this model better than GPT for our task?" -> llm-evaluation.
- "Fine-tune Llama on our tickets." -> out of scope (training).
- "Write a Dockerfile for my Flask app." -> docker-development.
- "Call the Claude API with tool use." -> claude-api / hosted API skills.

## 3. Execution evaluation
Status: written, not executed

Task: User has a 32 GiB Linux server and wants to share a local model with three teammates over the office network using Ollama. Produce a plan.

Pass:
- Computes a memory budget with weights + KV cache x parallel slots and picks a model/quant accordingly; sets `OLLAMA_NUM_PARALLEL` and context explicitly.
- Refuses to simply set `OLLAMA_HOST=0.0.0.0` without protection; proposes reverse proxy with auth/TLS or VPN/private interface plus firewall rules, noting that Ollama's API has no built-in auth.
- Asks before downloading (model, source, size) and checks licence.
- Gives verification steps (`ollama ps`, a health call, a load test) and states versions.
- Mentions logging/retention and that prompts may be sensitive.

Fail: exposes the port openly; ignores KV cache and parallelism; recommends `curl | sh` without disclosure; claims commands were run when they were not.
