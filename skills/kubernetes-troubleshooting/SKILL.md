---
name: kubernetes-troubleshooting
description: >
  Diagnose broken Kubernetes workloads with a layered, read-only-first method: Pending pods,
  ImagePullBackOff, CrashLoopBackOff, OOMKilled, failing probes, Services with no endpoints,
  DNS and NetworkPolicy problems, node pressure. Teaches reading status, events and logs in
  order, forming hypotheses, and when (and how carefully) to use kubectl debug, exec or
  ephemeral containers. Use when a pod, deployment, service or node is unhealthy and the user
  needs root cause, not a restart. Not for writing manifests (use kubernetes-manifests), cluster
  provisioning or Helm authoring, container image hardening (container-security), or incidents
  that look like a security compromise (incident-response).
compatibility: >
  Requires kubectl configured for the target cluster. kubectl debug with ephemeral containers is
  stable since Kubernetes v1.25 and needs a container runtime that supports them. Examples target
  current upstream Kubernetes; managed clusters may restrict some operations.
metadata:
  author: michaelweissdev
  version: "1.0.0"
  tags: "kubernetes, kubectl, troubleshooting, debugging, pods, events, networking"
  topics: "devops, operations"
---

# Kubernetes Troubleshooting

Kubernetes tells you what is wrong in three places, in this order of usefulness: **object status** (what phase/state and why), **events** (what the control plane and kubelet did), and **container logs** (what the application said). Most incidents are solved without ever entering a container. The failure mode to avoid is "restart it and see", which destroys the evidence (previous container state, events age out after about an hour by default).

Boundaries: authoring manifests is `kubernetes-manifests`; image/runtime security is `container-security`; host OS problems are `linux-troubleshooting`; suspected compromise switches to `incident-response`; observability design is `logging-observability`.

## Non-negotiable rules

1. **Identify the cluster and namespace before every command.** `kubectl config current-context` and `-n <namespace>` explicitly. Many bad outages begin with the wrong context. Never assume production vs staging.
2. **Read-only first.** `get`, `describe`, `logs`, `events`, `top`, `auth can-i` change nothing. State changes (`delete`, `rollout restart`, `scale`, `edit`, `patch`, `apply`, `drain`, `cordon`, `taint`) need explicit user authorization with the effect and undo path stated.
3. **Do not delete pods to "fix" them** until you have captured status, events, and `logs --previous`; deleting a pod removes its history and may delete the only copy of a failing replica's state (emptyDir).
4. **`kubectl debug` and `exec` run code in the workload's environment**: they can see mounted secrets and service-account tokens and can alter state. Get authorization, prefer a copy (`--copy-to`) or an ephemeral container with a restrictive `--profile`, and never print Secret contents (`get secret -o yaml` / `jsonpath` of data) into chat. Use `kubectl describe secret` (shows sizes only) or check key names.
5. **Node-level debugging is privileged**: `kubectl debug node/...` mounts the host filesystem at `/host`. Only with approval; read, do not edit.
6. **Do not weaken security to make it work**: no `privileged`, `hostPath`, disabling NetworkPolicy, or `runAsUser: 0` as a "test".

## The method

### 1. Frame the symptom as a layer question

Work top-down; stop at the first layer that explains the symptom.

1. **Scheduling**: is the pod assigned to a node? (`Pending`)
2. **Image**: can the kubelet pull it? (`ErrImagePull`, `ImagePullBackOff`)
3. **Container start**: does the process start and stay up? (`CrashLoopBackOff`, `CreateContainerConfigError`, `RunContainerError`)
4. **Health**: do probes pass? (`Running` but `0/1 READY`, restarts from liveness)
5. **Resources**: OOMKilled, CPU throttling, eviction
6. **Networking**: Service selector -> endpoints -> DNS -> NetworkPolicy -> ingress
7. **Node/cluster**: NotReady, pressure conditions, control-plane/admission failures

### 2. Gather evidence (read-only, in this order)

```bash
kubectl config current-context
kubectl -n NS get pods -o wide                      # phase, restarts, node
kubectl -n NS describe pod POD                      # State, Last State, Reason, Exit Code, Events
kubectl -n NS get events --sort-by=.lastTimestamp   # namespace events (also: --field-selector involvedObject.name=POD)
kubectl -n NS logs POD -c CONTAINER                 # current
kubectl -n NS logs POD -c CONTAINER --previous      # the crashed instance
kubectl -n NS get pod POD -o yaml                   # spec + status (beware: may include env values; do not paste secrets)
```

`describe` shows container state (Waiting/Running/Terminated), restart count, probes, requests/limits, conditions and the Events section with source component and reason. Events are namespaced objects with a short retention, so capture them early.

### 3. Match the signature, then test the hypothesis

| Signature | Usual meaning | Confirming evidence | Likely cause classes |
|---|---|---|---|
| `Pending`, event `FailedScheduling` | Scheduler cannot place pod | Event text: insufficient cpu/memory, untolerated taint, node affinity/selector mismatch, unbound PVC | Resource requests too high, missing toleration/label, PVC/StorageClass |
| `ImagePullBackOff` | Pull failed | Event message (not found, unauthorized, timeout) | Wrong tag/registry, missing `imagePullSecrets`, network/egress |
| `CrashLoopBackOff` | Container exits repeatedly | `Last State: Terminated`, `Exit Code`, `logs --previous` | App error, bad config/env, missing dependency |
| Exit code 137 / `Reason: OOMKilled` | Killed for memory (or SIGKILL) | `Last State` reason; node/cgroup memory | Limit too low, leak. 137 alone is SIGKILL; confirm OOMKilled reason before concluding |
| `CreateContainerConfigError` | Missing ConfigMap/Secret key | Event names the missing key/object | Typo, wrong namespace, not created yet |
| `Running`, not Ready | Readiness probe failing | Event `Unhealthy`, probe config | Wrong port/path, slow start (consider startupProbe), dependency down |
| Restarts with healthy-looking app | Liveness probe too strict | `Liveness probe failed` events | Aggressive timeouts, GC pauses |
| `Evicted` | Node pressure | Pod status message, node conditions (`DiskPressure`, `MemoryPressure`) | Node resource exhaustion, ephemeral-storage |
| Service has no traffic | Selector/endpoint mismatch | EndpointSlices (`kubectl get endpointslices -l kubernetes.io/service-name=<svc>`) empty; `kubectl get endpoints` is deprecated | Labels do not match, pods not Ready, wrong `targetPort` |
| In-cluster name resolution fails | DNS | CoreDNS pods/logs, a test lookup from a debug pod | CoreDNS down, NetworkPolicy blocking port 53, search-domain `ndots` effects |

Write the hypothesis as a prediction ("if the service has no endpoints, `get endpoints` is empty and selector labels differ from pod labels"), run the single command that tests it, and discard the hypothesis if the output disagrees.

### 4. When you must enter the workload

Prefer, in order:
1. More read-only data (`kubectl top` if metrics-server exists, node `describe`, logs of neighbours).
2. **Ephemeral debug container** for minimal images (stable since v1.25):
   ```bash
   kubectl -n NS debug -it POD --image=busybox:1.28 --target=CONTAINER --profile=general
   ```
   `--target` shares the process namespace of the target container if the runtime supports it; without runtime support `ps` may not show other containers' processes. Profiles from the official docs: `legacy` (default today, planned for deprecation), `general`, `baseline`, `restricted`, `netadmin`, `sysadmin`. Use the least privileged profile that works; `sysadmin` and `netadmin` add privileges and need approval.
3. **Copy of the pod** to avoid disturbing the original:
   ```bash
   kubectl -n NS debug POD -it --copy-to=POD-debug --image=ubuntu --share-processes
   ```
   Creates a new pod; delete it when done (a cleanup that you announce). It does not reproduce all state (traffic, owner controller behavior).
4. `kubectl exec` into the app container: last resort, read-only commands only.
5. Node debugging (`kubectl debug node/NAME -it --image=...`): host root at `/host`, host namespaces; approval required.

### 5. Change one thing, with authorization

After root cause is evidenced: propose the smallest fix (e.g. raise memory limit, correct selector), show the diff, apply only on approval, and verify with the same signals that showed the fault (events clear, `READY n/n`, endpoints populated). Roll back path: `kubectl rollout undo` for Deployments; keep the previous manifest.

## Worked example: CrashLoopBackOff after a deploy

1. `get pods -o wide`: `api-7c9` `CrashLoopBackOff`, 6 restarts. Context and namespace confirmed as staging.
2. `describe pod`: `Last State: Terminated, Reason: Error, Exit Code: 1`; no OOMKilled; Events show backoff only.
3. `logs --previous`: `Error: required env DATABASE_URL not set`.
4. Hypothesis: the new Deployment revision dropped an env var. Test (read-only): `kubectl rollout history deployment/api` and compare the revision's pod template (`get deployment api -o yaml` focusing on `env`).
5. Finding: `envFrom` reference to a ConfigMap was renamed. Proposed fix: correct the reference in the manifest repo (not an in-cluster edit); apply via the normal pipeline after approval. Verify pods Ready and error gone.

At no point was a pod deleted or exec'd into.

## Anti-patterns

- `kubectl delete pod` / `rollout restart` as the first move.
- Reading only `logs` (current) and missing `--previous`.
- Treating exit 137 as always OOM, or `Running` as healthy.
- Ignoring events because `describe` "looked fine" after they aged out.
- `kubectl get secret -o yaml` pasted into a ticket.
- Debugging with `privileged` pods in production without approval.
- Editing live objects (`kubectl edit`) so the cluster drifts from Git.
- Changing multiple variables at once.

## Verification checklist

- [ ] Context and namespace stated.
- [ ] Status, events and previous logs captured before any change.
- [ ] Hypothesis stated and tested with a specific command.
- [ ] Any exec/debug/state change was explicitly authorized; least-privilege profile used.
- [ ] Fix verified with the same signals; temporary debug pods removed.
- [ ] No secret values printed.

## References

- [references/symptom-guide.md](references/symptom-guide.md): deeper per-symptom checks (networking, nodes, storage).
- [references/scenarios.md](references/scenarios.md): scenarios.
- [references/sources.md](references/sources.md): sources and provenance.
