# Linux Triage Playbook

Read-only first. Every command here only inspects state unless marked otherwise. Output varies by distribution, kernel, and installed packages (`iostat` needs `sysstat`; `resolvectl` needs systemd-resolved).

## OOM in detail

| Observation | Meaning | Next step |
| :--- | :--- | :--- |
| `Out of memory: Killed process N (name)` in `journalctl -k` | Kernel global OOM killer | Check what grew (`ps -eo pid,rss,cmd --sort=-rss \| head`); look for leaks, missing limits |
| `Memory cgroup out of memory` | A cgroup (service, container) hit its `memory.max`, not the whole host | `systemctl show <unit> -p MemoryMax,MemoryCurrent`; raise limit or fix usage |
| Process vanished, no kernel message, `systemd-oomd` in journal | User-space OOM daemon acted | `journalctl -u systemd-oomd` |
| Service restarts with exit code 137 | SIGKILL (128+9), often OOM | Correlate timestamps with kernel log |
| `free -h` "available" is low and swap is thrashing | Real memory pressure | `cat /proc/pressure/memory`, `vmstat 1` (si/so columns) |

"Free" memory being low is normal because Linux uses spare RAM for cache; judge by "available" and by pressure.

## Network and DNS

```bash
ip -br addr                 # interfaces and addresses
ip route                    # default route present?
ss -tulpn                   # listening sockets (process names need root)
resolvectl status           # resolver per link (systemd-resolved)
getent hosts example.com    # resolution as applications see it (nsswitch)
```

| Symptom | Check | Typical cause |
| :--- | :--- | :--- |
| Name resolves with `dig` but app fails | `getent hosts name`, `/etc/nsswitch.conf` | Resolver config differs between tools |
| `connection refused` | `ss -tlnp` shows nothing on that port | Service down or bound to loopback only |
| `connection timed out` | Firewall or routing | `ip route get <ip>`; check host firewall rules (`nft list ruleset`, needs root; read only) |
| Intermittent resets | MTU, conntrack, load balancer idle timeouts | Reproduce with timestamps; `ss -ti` for retransmits |

## Permissions, SELinux, AppArmor

- Identify who runs the process: `ps -o user,group,cmd -p <pid>` or `systemctl show <unit> -p User,Group`.
- Check the path chain: `namei -l /full/path/to/file` shows each directory's permissions.
- SELinux denials: `ausearch -m avc -ts recent` (root). Generate a targeted policy only after confirming the access is legitimate; never set permissive mode permanently.
- systemd sandboxing (`ProtectSystem=`, `ReadWritePaths=`, `PrivateTmp=`) can deny writes that file permissions allow; read `systemctl cat <unit>`.

## Boot and service ordering

```bash
systemctl --failed
journalctl -b -p warning --no-pager | tail -n 50
journalctl -b -1 -p err --no-pager | tail -n 50    # previous boot, if persistent journal is enabled
systemd-analyze blame | head
systemd-analyze critical-chain <unit>
```

If the previous boot's journal is empty, journald storage is volatile; note that and look at `/var/log` and `last -x` instead.

## Time

`timedatectl status`: clock skew breaks TLS, Kerberos, and log correlation. Confirm NTP sync state before chasing certificate errors.

## Crashes

`coredumpctl list` and `coredumpctl info <pid>` show recent core dumps and signals. A SIGSEGV points to the application or its libraries; SIGKILL to an external killer (OOM, operator, watchdog); SIGABRT to an assertion or allocator error.

## Containers on a single host (not orchestration)

`docker ps -a` / `podman ps -a` show exit codes (137 = SIGKILL, 143 = SIGTERM); `docker logs --tail 100 <name>`. If the problem is scheduling, networking overlays, or cluster state, this skill does not apply.

## Writing up the result

Record: symptom and exact error, first-seen time, environment, evidence collected (commands and key lines, redacted), hypothesis, test, root cause, change made (exact), verification, and follow-up prevention. If the root cause was not confirmed, say so.

## Stop and ask the user before

Restarting production services, changing kernel parameters, editing unit files, deleting or truncating files, changing firewall rules, or running anything with `sudo` whose effect you cannot state in one sentence.
