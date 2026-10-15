# Evidence Log and Timeline Templates

## Evidence log (one row per item)

| ID | Description | Source (host/system) | Collected by | Collected at (UTC) | Method | SHA-256 | Stored at (read-only) | Transfers |
|---|---|---|---|---|---|---|---|---|
| E-001 | Volume snapshot of web-01 | cloud console | A. Rivera | 2026-10-15T03:12Z | Provider snapshot | n/a (provider id) | snapshot id | none |
| E-002 | auth log export | SIEM | J. Kim | 2026-10-15T03:40Z | Query export | `<hash>` | evidence bucket | to analyst 03:55Z |

Rules: never edit an item; derive working copies from the stored original; note tool versions used.

## Timeline template

| Time (UTC) | Event | Source / evidence ID | Confidence (observed / inferred) | Notes |
|---|---|---|---|---|

Separate three clocks: event time in the log, collection time, and action time (what responders did). Record host clock skew when known.

## Read-only collection notes (Linux, if host access is approved)

Run from trusted tooling and write output to external, approved storage, not to the suspect disk. Record each command and its time. Typical volatile reads: `date -u`, `uptime`, `ps` process listings, `ss` socket listings, `ip route`, `ip neigh`, `mount`, logged-in users (`w`). Interpret with caution: a rootkit can hide from them. Memory acquisition and disk imaging require dedicated tools chosen with the incident lead; do not improvise them.

Avoid: tools that touch access times on many files (RFC 3227 mentions `tar`-style copying), installing packages, running vendor "cleaner" scripts, rebooting.

## Containment option card

| Option | Preserves state? | Reversible? | Side effects | Authorizer |
|---|---|---|---|---|
| Quarantine security group / VLAN | yes | yes | Service outage for the host | Incident lead |
| Disable one account or key | yes | yes | Breaks that integration | System owner |
| Block indicator at egress | yes | yes | False-positive risk | Network owner |
| Power off | no (volatile data lost) | partial | Evidence loss | Incident lead + legal |
| Reimage | no | no | Destroys evidence unless imaged first | Incident lead |
