---
name: system-architecture-design
description: >
  Design, document, and evaluate distributed software architectures, domain models,
  and scalability patterns. Use when drafting Architecture Decision Records (ADRs),
  creating C4 model diagrams, evaluating modular monolith vs microservices trade-offs,
  defining Domain-Driven Design (DDD) bounded contexts, designing event-driven systems,
  or applying CQRS, sharding, and caching strategies under CAP/PACELC constraints.
compatibility: >
  Agent Skills-compatible coding agents designing software architectures, authoring
  technical documentation, or reviewing system topologies. Tooling is required only
  for executable validation.
metadata:
  author: michaelweissdev
  version: "1.0.0"
  tags: "architecture, system-design, adr, c4-model, ddd, microservices, modular-monolith, event-driven, cqrs, scalability"
  topics: "software-development"
---

# System Architecture Design & Engineering

System architecture design is the intentional definition of software components, their boundaries, interaction patterns, and data consistency models to satisfy functional requirements while optimizing non-functional trade-offs: availability, latency, maintainability, and operational simplicity.

## Purpose & Overview

Modern software systems fail when architectural decisions are made ad-hoc without explicit trade-off analyses, when boundaries are porous, or when distributed systems primitives are adopted prematurely. A disciplined architectural approach communicates topology clearly, defines explicit bounded contexts, and records rationale before code is written.

This skill equips agents with methods and templates to:
- Formulate and record technical trade-offs using structured **Architecture Decision Records (ADRs)**.
- Document system topologies across abstraction levels using the **C4 Model** (Context, Container, Component, Code).
- Make informed trade-offs between **Modular Monoliths** and **Microservices** based on team cognitive load and data dependencies.
- Partition complex business logic using **Domain-Driven Design (DDD)** bounded contexts and ubiquitous language.
- Architect resilient asynchronous communication using **Event-Driven Architecture (EDA)**, the Transactional Outbox pattern, and idempotent consumers.
- Navigate consistency constraints governed by the **CAP and PACELC theorems**.
- Scale read and write operations using **CQRS**, read replicas, horizontal sharding, and multi-tier caching.

---

## Core Principles & Rules

1. **Default to a Modular Monolith First**: Unless independent deployment frequency, heterogeneous hardware needs, or massive organizational scale dictate microservices, design a clean modular monolith with strictly enforced module boundaries. Premature microservices replace in-process method calls with network failure domains.
2. **Document Decisions in Immutable ADRs**: Never change fundamental system design in commit messages or chat channels. Capture the context, options considered, trade-offs, and consequences in a standardized Architecture Decision Record.
3. **Decouple Data Storage per Bounded Context**: Microservices or modules must never share a single database table or perform cross-boundary direct SQL joins. Each context owns its database schema and communicates through well-defined APIs or events.
4. **Assume Network Failure in Distributed Systems**: Remote procedure calls (REST, gRPC) can fail, time out, or duplicate. Every inter-service interaction must implement timeouts, circuit breakers, retries with exponential backoff and jitter, and idempotent consumer semantics.
5. **Acknowledge the PACELC Theorem**: Under network partitions (P), choose between Availability (A) and Consistency (C); Else (E) under normal execution, choose between Latency (L) and Consistency (C). Acknowledge that strong global consistency inevitably increases write latency.
6. **Use the Transactional Outbox Pattern for Reliable Events**: Never publish a message to an external message broker (Kafka, RabbitMQ) inside a database transaction without an outbox table. If the broker is unreachable, the database transaction rolls back, or the message is lost.

---

## Standard Workflows & Procedures

### Workflow 1: Authoring an Architecture Decision Record (ADR)

Use the Michael Nygard ADR format to capture decisions:

```markdown
# ADR-0012: Adopt Transactional Outbox Pattern for Order State Events

## Status
Accepted

## Context
When an order is created or status changes in the Orders service, downstream services (Inventory, Billing, Notifications) require immediate notification. Directly publishing to Apache Kafka within the HTTP request transaction creates a dual-write problem: if Kafka is unavailable or slow, the database transaction fails; conversely, if the database commits but the Kafka publish fails, state diverges.

## Decision
We will implement the Transactional Outbox Pattern:
1. Every order mutation writes both the entity change and an `outbox_events` record within the same local ACID PostgreSQL transaction.
2. An asynchronous Debezium CDC (Change Data Capture) connector reads PostgreSQL WAL logs and streams messages into Kafka with at-least-once delivery.
3. Downstream consumers will enforce idempotency by storing processed event IDs.

## Consequences
### Positive
- Guaranteed atomicity between database mutations and event publications.
- Zero latency overhead on user-facing HTTP transactions from Kafka broker delays.
- Decouples API availability from message broker availability.

### Negative / Trade-offs
- Additional infrastructure complexity (maintaining Debezium Kafka Connect instances).
- Downstream services must handle duplicate events through idempotent processing.
```

### Workflow 2: C4 Model Architectural Diagramming

The C4 model partitions system architecture into four progressive levels of zoom:

```
Level 1: System Context
  ┌─────────────────────────────────────────────────────────────────┐
  │ [User] ──► [E-Commerce Platform] ──► [Stripe Payment Gateway]   │
  └─────────────────────────────────────────────────────────────────┘
                                   │
                                   ▼
Level 2: Container (Applications & Data Stores)
  ┌─────────────────────────────────────────────────────────────────┐
  │ [Web SPA] ──► [API Gateway] ──► [Order Service] ──► [PostgreSQL]│
  │                                        │                        │
  │                                        ▼                        │
  │                                 [Kafka Broker]                  │
  └─────────────────────────────────────────────────────────────────┘
                                   │
                                   ▼
Level 3: Component (Modules inside Order Service)
  ┌─────────────────────────────────────────────────────────────────┐
  │ [OrderController] ──► [OrderService] ──► [OrderRepository]      │
  │                              │                                  │
  │                              ▼                                  │
  │                     [OutboxWriterComponent]                     │
  └─────────────────────────────────────────────────────────────────┘
                                   │
                                   ▼
Level 4: Code (Class diagrams / entity relationships - used sparingly)
```

### Workflow 3: Decomposing Domains with Domain-Driven Design (DDD)

1. **Identify Ubiquitous Language**: Standardize business terms between domain experts and engineering. Avoid overloaded words (e.g. "Account" can mean User Identity in Auth, but Ledger Account in Billing).
2. **Define Bounded Contexts**: Draw explicit boundaries where a specific domain model applies.
3. **Map Context Relationships (Context Mapping)**:
   - *Shared Kernel*: Shared library between teams (use sparingly).
   - *Customer-Supplier / Upstream-Downstream*: Upstream produces data, downstream consumes.
   - *Anticorruption Layer (ACL)*: Translates external or legacy data models into clean internal domain concepts.

---

## Real-World Examples & Patterns

### Pattern 1: Transactional Outbox with PostgreSQL

Ensure database writes and event publishing remain atomic:

```sql
-- Application database transaction
BEGIN;

-- 1. Mutate business entity
INSERT INTO orders (id, customer_id, total_cents, status, created_at)
VALUES ('ord_1084', 'cust_992', 14900, 'PENDING', NOW());

-- 2. Insert corresponding event record in the same atomic transaction
INSERT INTO outbox_events (
    id, 
    aggregate_type, 
    aggregate_id, 
    event_type, 
    payload, 
    created_at
) VALUES (
    gen_random_uuid(),
    'ORDER',
    'ord_1084',
    'OrderCreated',
    jsonb_build_object(
        'order_id', 'ord_1084',
        'customer_id', 'cust_992',
        'total_cents', 14900,
        'status', 'PENDING'
    ),
    NOW()
);

COMMIT;
```

A background relay or CDC agent publishes rows from `outbox_events` to the messaging system, deleting or marking rows as published upon broker acknowledgment.

### Pattern 2: CQRS with Read-Optimized Materialized Views

Separate high-write operational workloads from complex query and search requirements:

```
[Client Writes] ──► [Command Handler] ──► [Write DB: PostgreSQL (Normalized)]
                                                   │
                                                   ▼ Debezium / Kafka CDC
                                           [Projector / Worker]
                                                   │
                                                   ▼
[Client Reads]  ◄── [Query Handler]   ◄── [Read DB: Elasticsearch / Redis]
```

Benefits:
- Write models focus strictly on enforcing business invariants and atomic transactions.
- Read models are pre-joined, denormalized, and indexed for sub-millisecond query latency.

### Pattern 3: Multi-Tier Caching with Stampede Protection

Implement Cache-Aside with Distributed Locking or Probabilistic Early Expiration (XFetch) to avoid the cache stampede (thundering herd) problem when popular cache keys expire:

```python
import time
import math
import random
from typing import Callable, Any

class DistributedCacheTier:
    def __init__(self, redis_client):
        self.redis = redis_client

    def get_with_xfetch(
        self, 
        key: str, 
        ttl_seconds: int, 
        beta: float, 
        compute_fn: Callable[[], Any]
    ) -> Any:
        """
        Probabilistic Early Expiration (XFetch algorithm)
        beta > 1.0: more aggressive pre-computation
        """
        entry = self.redis.get_json(key)
        now = time.time()

        # If key missing or probabilistic check triggers early recomputation
        if not entry:
            return self._compute_and_set(key, ttl_seconds, compute_fn)

        val = entry["value"]
        delta = entry["compute_duration"] # time taken to compute value
        expiry = entry["expires_at"]

        # XFetch decision condition: -beta * delta * ln(random(0,1))
        # As now approaches expiry, probability of True increases to 1.0
        if (now - (delta * beta * math.log(random.random()))) >= expiry:
            # Recompute in background or return fresh computation
            return self._compute_and_set(key, ttl_seconds, compute_fn)

        return val

    def _compute_and_set(self, key: str, ttl: int, compute_fn: Callable[[], Any]) -> Any:
        start = time.time()
        val = compute_fn()
        duration = time.time() - start

        self.redis.set_json(key, {
            "value": val,
            "compute_duration": duration,
            "expires_at": time.time() + ttl
        }, ex=ttl + 300) # Keep slightly longer than soft expiry
        return val
```

---

## Common Anti-Patterns & Pitfalls

| Anti-Pattern | Operational Hazard | Correct Engineering Approach |
|:---|:---|:---|
| **Distributed Monolith** | Services share a database or require lockstep deployments, multiplying network failure modes without deployment autonomy. | Consolidate back into a modular monolith or decouple data models completely. |
| **Dual Writes without Outbox** | Updating database and publishing to message queue independently results in lost events or phantom messages. | Use the Transactional Outbox pattern with CDC or an atomic relay. |
| **Entity-Service Antipatttern** | Creating a microservice for every database table (`UserService`, `OrderService`, `AddressService`) causes deep call graphs and high latency. | Group related entities into a single Bounded Context Aggregate around business capabilities. |
| **Synchronous RPC Chains** | Service A calls B, which calls C, which calls D. Total availability is $A_a \times A_b \times A_c \times A_d$, drastically increasing failure rate. | Replace deep synchronous chains with asynchronous event choreography or materialized read views. |
| **Unbounded In-Memory Caches** | Unbounded maps in application memory cause out-of-memory crashes under load spikes. | Always enforce max-size eviction policies (LRU/LFU/W-TinyLFU) and memory limits. |
| **Over-Abstracted Interfaces** | Creating factory-provider-strategy layers for single-implementation classes creates cognitive overhead. | Follow YAGNI; create abstractions only when multiple concrete implementations or test boundaries exist. |

---

## Verification Checklist

- [ ] Architecture Decision Record (ADR) documented with context, options, consequences, and trade-offs.
- [ ] Bounded contexts defined with explicit ubiquitous language and independent database ownership.
- [ ] C4 diagrams created for at least Context (Level 1) and Container (Level 2) views.
- [ ] Asynchronous event publications use the Transactional Outbox pattern to prevent dual-write inconsistencies.
- [ ] Network boundaries implement timeouts, circuit breakers, retries with jitter, and idempotent consumer handlers.
- [ ] CAP/PACELC trade-offs documented (strong vs. eventual consistency explicitly chosen and justified).
- [ ] Caching layers implement max-capacity limits, TTLs, and stampede mitigation (probabilistic early refresh or mutex).
- [ ] Horizontal scaling path defined (stateless application tier, database read replicas or sharding strategy).

---

## Tooling & Reference Guides

- **Architecture Decision Records (ADRs)**: Michael Nygard's format and lightweight CLI tools (`adr-tools`).
- **The C4 Model**: Visualizing software architecture by Simon Brown ([c4model.com](https://c4model.com)).
- **Domain-Driven Design (DDD)**: Eric Evans' Domain-Driven Design: Tackling Complexity in the Heart of Software.
- **Designing Data-Intensive Applications**: Martin Kleppmann's authoritative reference on distributed data systems and consistency models.
- **Debezium**: Open source distributed platform for Change Data Capture (CDC) implementing the Outbox pattern.
- **Mermaid.js C4 & Flowcharts**: Text-based diagramming tool for embedding architectures in git repositories.
