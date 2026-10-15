# Symptom Guide (read-only checks)

All commands here are read-only. Always add `-n NAMESPACE` and confirm `kubectl config current-context`.

## Service reachable? Walk the chain

1. **Pods Ready?** `kubectl get pods -l app=NAME -o wide`. Not Ready pods are removed from endpoints.
2. **Selector matches?** Compare `kubectl get svc SVC -o jsonpath='{.spec.selector}'` with `kubectl get pods --show-labels`.
3. **Endpoints populated?** `kubectl get endpointslices -l kubernetes.io/service-name=<svc>` (`kubectl get endpoints` still works but is deprecated).
4. **Port mapping:** `port` (Service) -> `targetPort` (container port or name). A mismatch yields connection refused.
5. **DNS:** from a debug pod (approved), resolve `SVC.NS.svc.cluster.local`. Check `kubectl -n kube-system get pods -l k8s-app=kube-dns` and CoreDNS logs.
6. **NetworkPolicy:** `kubectl get networkpolicy`; policies are additive allow rules per selected pod; a pod selected by any ingress policy denies unlisted traffic. Egress policies must also allow DNS (UDP/TCP 53).
7. **Ingress / Gateway:** controller logs, ingress events, backend service name and port.

## Pending pods

- `describe pod` Events: `FailedScheduling` messages enumerate which nodes failed and why (resources, taints, affinity, volume node affinity).
- `kubectl describe node NODE`: Allocatable vs Allocated resources, Taints, Conditions.
- PVC: `kubectl get pvc`, `describe pvc` (unbound, StorageClass missing, zone mismatch).
- Quotas: `kubectl describe resourcequota` and LimitRange may block creation (shows as ReplicaSet events rather than pod events: `kubectl describe rs`).

## Memory and CPU

- OOMKilled shows in `Last State: Terminated, Reason: OOMKilled`. Limits are per container; the node can also OOM-kill when overcommitted, then pods show `Evicted` or abrupt exits.
- `kubectl top pod/node` requires metrics-server; absence is itself a finding.
- CPU limits cause throttling without crashes: latency symptoms, no restarts. Needs metrics (cAdvisor `container_cpu_cfs_throttled_*`) rather than kubectl.

## Nodes

- `kubectl get nodes`; `describe node` Conditions (`Ready`, `MemoryPressure`, `DiskPressure`, `PIDPressure`), recent events.
- NotReady: kubelet, container runtime, network plugin or cloud health. Node shell access is a separate, authorized step.
- Cordon/drain are state changes; propose, do not run unapproved.

## Rollout problems

- `kubectl rollout status deployment/NAME`, `kubectl rollout history deployment/NAME`.
- `kubectl describe deployment`: conditions `Progressing`/`ReplicaFailure`, `maxUnavailable`/`maxSurge` blocking progress.
- Compare ReplicaSets: `kubectl get rs -o wide`.

## Admission and RBAC

- `kubectl auth can-i VERB RESOURCE --as=SERVICEACCOUNT` (impersonation needs permission; read-only check).
- Webhook failures appear in API error messages and events of the owning controller.
- Pod Security Admission rejections appear when creating pods (ReplicaSet events).

## Evidence hygiene

Save outputs of `describe`, `get events`, and `logs --previous` to files before any change. Avoid `-o yaml` on Secrets and review pod YAML for plain-text env values before sharing.
