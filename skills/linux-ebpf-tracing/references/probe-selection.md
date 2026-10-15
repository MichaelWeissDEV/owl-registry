# Probe Selection and Attach Failures

## Choosing a probe type

| Need | Prefer | Why | Caveat |
|---|---|---|---|
| Syscall entry/exit, args, return | `tracepoint:syscalls:sys_enter_*` / `sys_exit_*` | Stable names, typed `args` | One tracepoint per syscall; `raw_syscalls:sys_enter` covers all but is hot |
| Scheduler, block, net, filesystem events | `tracepoint:sched:*`, `block:*`, `net:*`, `ext4:*` | Kernel-maintained interface | Available set depends on kernel config |
| Time-based sampling | `profile:hz:N` (all CPUs), `interval:s:N` (one CPU, for timers/exit) | Bounded overhead | Statistical; use 49 or 99 Hz rather than 100 to avoid lockstep with timers |
| Kernel function not covered by tracepoints | `kprobe:` / `kretprobe:` | Reaches internals | Can be renamed/inlined/absent per kernel; may be unsafe to probe hot or notrace paths |
| Function entry/exit with typed args | `fentry:` / `fexit:` (needs BTF and a supporting kernel) | Lower overhead than kprobes where available | Check `bpftrace --info` for support |
| Userspace function | `uprobe:/path/bin:func`, USDT `usdt:/path:provider:probe` | Application-level view | Needs symbols or USDT probes; uprobes cost more per event |

Always check availability with `bpftrace -l '<pattern>'` and argument shape with `bpftrace -vl <probe>`.

## Attach and load failures: diagnose, do not bypass

| Symptom | Likely cause | Next read-only step |
|---|---|---|
| Permission / operation not permitted | Not root, missing CAP_BPF/CAP_PERFMON, lockdown, container restrictions | `id`; check whether you are in a container; ask the host owner. Do not escalate on your own |
| No such probe / no matching probes | Typo, kernel lacks it, function inlined | `bpftrace -l` with a broader pattern; `uname -r` |
| Unknown struct / cannot resolve field | No BTF and no kernel headers | `ls /sys/kernel/btf/vmlinux`; install matching kernel headers only with approval, or use a different probe |
| Verifier rejection | Program too complex or unsafe memory access | Simplify; fewer map keys; avoid unbounded loops. `-d verifier` shows stage output but is meant for developers |
| Syntax error on `args.x` | bpftrace older than 0.19 | `bpftrace --version`; use `args->x` or upgrade |
| Warning about lost events / full map | Too many events or keys | Add filters, shorten window |

## Overhead heuristics

- Events/sec x per-event work = cost. A `count()` on a tracepoint with 50k events/s is cheap; a `printf` on every one is not.
- Aggregate in kernel maps (`count`, `sum`, `hist`, `lhist`) rather than emitting per-event text.
- Prefer filtering by pid/comm/cgroup in the probe predicate so most events exit early.
- Measure the target's own latency before and during tracing when the claim matters.
