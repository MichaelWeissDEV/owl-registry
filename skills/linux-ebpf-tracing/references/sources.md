# Sources and Provenance

## Official sources consulted (2026-10-15)

| URL | Used for |
|---|---|
| https://github.com/bpftrace/bpftrace/blob/master/docs/tutorial_one_liners.md | One-liner patterns (openat, block_rq_issue, vfs_read latency, profile), `args.xxx` needing bpftrace 0.19+, BTF vs header includes, kprobe fragility warning, `bpftrace -l` / `-vl`. |
| https://github.com/bpftrace/bpftrace/blob/master/man/adoc/bpftrace.adoc | `--unsafe` semantics (enables `system` and relaxed kprobe checks), `-e`, `-l`, `--dry-run`, `-d`, `--info`, `BPFTRACE_*` env mapping; no minimum kernel version stated. |
| https://docs.kernel.org/bpf/bpf_design_QA.html | Statement that tracing BPF programs are root-only. |
| https://github.com/bpftrace/bpftrace | README: check `bpftrace --version` against docs; tools/ directory. |

## Not verified from primary docs

- CAP_BPF / CAP_PERFMON requirement is from kernel patch discussions on LWN (found via search) and general knowledge; the current kernel capability man page was not fetched. Hence the skill tells readers to verify with `bpftrace --info` and `id`.
- Specific kernel version minimums for BTF/fentry were intentionally not stated.
- bpftrace's own INSTALL docs paths returned 404; the older fork INSTALL (kernel 4.9+ recommendation) was seen only as a search snippet and is not relied on.
- `fentry`/`fexit` probe availability depends on bpftrace version and kernel; marked "check --info".
- No bpftrace program was executed (macOS authoring host).

## Provenance

All text is original. External skill repositories (anthropics/skills, obra/superpowers, trailofbits/skills, vercel-labs/agent-skills, huggingface/skills, supabase/agent-skills) were not consulted; nothing copied. bpftrace is Apache-2.0 licensed; only command syntax facts were used, no text reproduced.
