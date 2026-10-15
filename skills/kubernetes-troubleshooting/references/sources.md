# Sources and Provenance

## Official sources consulted (2026-10-15)

| URL | Used for |
|---|---|
| https://kubernetes.io/docs/tasks/debug/debug-application/debug-running-pod/ | `kubectl describe` fields (State, Ready, Restart Count, Conditions, Events); ephemeral containers stable since v1.25; `--target` needing runtime support; `--profile` values (legacy default, general, baseline, restricted, netadmin, sysadmin); `--copy-to` with `--share-processes`; node debug mounts host root at `/host` and uses host namespaces. |

Local tool: kubectl is installed on the authoring machine but no cluster was used; nothing was executed against a cluster.

## Not verified against primary docs

- Event retention (about one hour by default) and `kubectl top` requiring metrics-server: general operational knowledge.
- Exit code 137 meaning SIGKILL and the OOMKilled reason field: standard Linux/Kubernetes behavior, not re-fetched.
- NetworkPolicy additive semantics and EndpointSlice label `kubernetes.io/service-name`: stable upstream behavior, not re-fetched.
- Version-specific flag availability should be checked with `kubectl debug --help` on the user's client.

## Provenance

All text is original. External skill repositories (anthropics/skills, obra/superpowers, trailofbits/skills, vercel-labs/agent-skills, huggingface/skills, supabase/agent-skills) were not consulted; nothing copied.
