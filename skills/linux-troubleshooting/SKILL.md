---
name: linux-troubleshooting
description: >
  Systematically isolate, diagnose, and resolve Linux system, storage, memory,
  performance, and service failures. Use when diagnosing high load, out-of-memory
  (OOM) crashes, disk space or inode exhaustion, crashing systemd services, or
  intermittent system anomalies through reproducible observations.
compatibility: >
  Agent Skills-compatible coding agents diagnosing Linux system issues
  with command-line diagnostic tools.
metadata:
  author: michaelweissdev
  version: "1.0.0"
  tags: "linux, troubleshooting, performance, oom, disk, systemd, logs"
  topics: "operating-systems, devtools"
---

# Linux Troubleshooting and Diagnosis

Effective troubleshooting is driven by evidence, hypothesis testing, and systematic isolation. An agent must never make random configuration changes or reboot systems hoping an issue disappears. Always collect reproducible observations first, form a falsifiable hypothesis, verify the root cause, and then apply a targeted remediation.

## Core Rules

1. **Observe before modifying**: Gather logs, metrics, and error codes before changing files, restarting services, or executing remediation commands.
2. **One change at a time**: Test a single isolated variable. If a modification does not resolve the issue, revert it before attempting another.
3. **Check the basics first**: Disk space, inode exhaustion, memory exhaustion (OOM), and permissions account for >70% of common system failures.
4. **Preserve crash evidence**: Copy relevant log excerpts, core dumps, or kernel messages before clearing caches or restarting services.
5. **Never run destructive commands blindly**: Avoid `rm -rf`, `sync && reboot`, or killing unknown processes without identifying their role.

---

## 1. Quick Triaging Checklist (The 60-Second Scan)

Run these non-destructive diagnostics when an incident begins:

```bash
# 1. System Load & Uptime (CPU saturation)
uptime

# 2. Memory & Swap consumption
free -h

# 3. Disk space and mount points
df -h

# 4. Inode exhaustion (disk can be full even with free gigabytes!)
df -i

# 5. Kernel errors & Out-Of-Memory (OOM) killer events
sudo dmesg -T --level=alert,crit,err | tail -n 25

# 6. Failed systemd services
systemctl --failed
```

---

## 2. Diagnosing Common Failure Categories

### Category A: Out-Of-Memory (OOM) and Memory Leaks
When processes disappear without a trace or report `Killed`:

```bash
# Check if Linux OOM killer terminated the process
dmesg -T | grep -i -E "killed process|oom_reaper|out of memory"

# Identify top memory-consuming processes
ps aux --sort=-%mem | head -n 10

# Inspect detailed system memory breakdown (buffers, cache, dirty memory)
cat /proc/meminfo | head -n 15
```

### Category B: Disk Full and Inode Exhaustion
- **Symptom 1**: `No space left on device` despite `df -h` showing free gigabytes.
  - **Cause**: Inode exhaustion (too many tiny files).
  - **Check**: `df -i`. Find directory with excessive files:
    ```bash
    find / -xdev -type d -size +100k 2>/dev/null
    ```
- **Symptom 2**: Disk space not freed after `rm large_file.log`.
  - **Cause**: Deleted file is still held open by a running process.
  - **Check & Fix**:
    ```bash
    # Find deleted files still held by open file descriptors
    sudo lsof +L1
    # Restart or reload the holding process to release the disk blocks
    ```

### Category C: High CPU and Load Average
When load average is high:
- High load + high `%cpu` = CPU saturation (busy compute loops).
- High load + high `%iowait` (wa) = Disk I/O bottleneck (slow disks, paging).
- High load + low CPU/I/O = Processes blocked on uninterruptible sleep (D-state) or NFS hangs.

```bash
# 1-second system activity overview (check 'us', 'sy', 'wa', 'st')
vmstat 1 5

# Check processes in uninterruptible sleep (D state)
ps -eo state,pid,user,cmd | grep "^D"
```

### Category D: Failing systemd Services
When a service fails to start or crashes repeatedly:

```bash
# Inspect status, exit code, and recent unit log lines
systemctl status <service-name>

# View full journal logs for the specific unit since current boot
journalctl -u <service-name> -b --no-pager -n 50

# Check service configuration syntax without starting it
systemd-analyze verify /lib/systemd/system/<service-name>.service
```

---

## 3. Systematic 5-Step Troubleshooting Process

```
1. Reproduce & Define: What is failing? What is the exact error message?
         │
         ▼
2. Gather Evidence: Inspect journalctl, dmesg, /proc, ss, top, df.
         │
         ▼
3. Formulate Hypothesis: "The database crashed because /var reached 100% capacity."
         │
         ▼
4. Test & Validate: Verify hypothesis with specific command (`df -h /var`).
         │
         ▼
5. Remediate & Confirm: Apply minimal fix, test service, verify stability.
```

---

## 4. Common Mistakes and Anti-Patterns

| Anti-Pattern | Risk | Correct Practice |
| :--- | :--- | :--- |
| Blindly rebooting a failing server | Loses transient logs in memory, does not resolve root cause | Collect `journalctl` and `dmesg` before any restart |
| `rm -rf /var/log/*` | Deletes active log descriptors, fails to release disk space | Truncate specific large log files: `: > /var/log/app/huge.log` |
| Changing 5 configuration settings at once | Impossible to know which change fixed or exacerbated the bug | Change one setting, test, and document |
| Disabling SELinux/AppArmor permanently | Leaves system insecure | Check audit logs (`ausearch -m avc -ts recent`) and generate targeted policy rules |

---

## 5. Verification Checklist

- [ ] Exact error message and timestamp captured.
- [ ] Checked disk capacity (`df -h`) and inode status (`df -i`).
- [ ] Checked OOM events in kernel buffer (`dmesg`).
- [ ] Confirmed root cause before applying configuration changes.
- [ ] Validated service recovery with `systemctl is-active <service>`.
- [ ] Documented fix and verified system metrics returned to normal thresholds.
