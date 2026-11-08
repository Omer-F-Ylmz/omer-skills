# ADR-<NNNN>: Choice of primary database for <PROJECT>

## Status
Proposed (<YYYY-MM-DD>). Deciders: <names/roles>. Supersedes: none.

## Context
<PROJECT> needs a primary datastore for <core domain data>. No project specifics were provided, so this ADR is a template with the following assumptions, which must be confirmed or corrected:
- A1: The system is a transactional application (OLTP) with structured, relational data.
- A2: Expected scale is <rows / GB / QPS>; assumed moderate (single-node capable for the first 1-2 years).
- A3: The team is small and has stronger SQL experience than NoSQL/distributed-systems experience.
- A4: Deployment target is <cloud/provider/on-prem>; managed offerings are acceptable.
- A5: Strong consistency is required for core entities; eventual consistency is acceptable only for derived or analytics data.
- A6: No regulatory constraint beyond <e.g. KVKK/GDPR>; to be verified.

## Decision drivers
1. Data model fit (relational integrity vs. flexible documents).
2. Consistency and transaction guarantees.
3. Scalability and performance at the expected load (A2).
4. Operational burden and team familiarity (A3).
5. Cost: licensing, hosting, and operations.
6. Ecosystem: tooling, ORMs, migrations, backups, observability.
7. Portability and vendor lock-in risk.
8. Compliance, security, and data-residency requirements (A6).

## Options considered

### Option 1: PostgreSQL (relational)
- Pros: full ACID; rich SQL, JSONB, extensions; mature tooling; many managed offerings; low license cost; fits A1/A5.
- Cons: horizontal write scaling needs extra effort (partitioning, sharding, or extensions); needs tuning at high scale.

### Option 2: MySQL / MariaDB (relational)
- Pros: widely known; mature replication; many managed offerings; good for simple read-heavy workloads.
- Cons: fewer advanced features than Postgres (varies by version); behavioral differences across engine and version; same horizontal write-scaling limits.

### Option 3: Document store (e.g. MongoDB)
- Pros: flexible schema; natural fit for nested documents; built-in horizontal sharding.
- Cons: weaker fit for relational integrity and multi-entity transactions; join-heavy queries are awkward; schema discipline moves into application code; the team has less experience with it (A3).

### Option 4: Distributed SQL (e.g. CockroachDB, Spanner-class)
- Pros: horizontal scale with SQL and strong consistency; resilience across regions.
- Cons: higher operational and cost overhead; added write latency; likely more than A2 requires; smaller ecosystem.

### Option 5: Embedded/single-file SQL (e.g. SQLite)
- Pros: zero operations; minimal cost; simple deployment.
- Cons: limited concurrent writers; no built-in network access or HA; suitable only for small or single-node workloads.

## Decision
Under assumptions A1-A6, choose **Option 1: PostgreSQL** as the primary database, using <managed service / self-hosted> on <provider>.

Rationale by driver:
- Drivers 1-2: the relational model and ACID transactions match A1/A5.
- Driver 3: a single primary with read replicas covers A2; partitioning is the scale-out path.
- Driver 4: SQL skills already exist in the team (A3), and managed hosting limits operational work.
- Drivers 5-7: no license cost, wide tooling, and open-source portability limit lock-in.
- Driver 8: the managed options support encryption and region selection (verify against A6).

If A1, A2, or A5 turn out false (for example a schema-less, write-heavy, globally distributed workload), this decision must be revisited.

## Consequences

### Positive
- Strong integrity guarantees and a familiar query model.
- Large ecosystem, with a hiring pool and tooling for migrations, backup, and monitoring.
- JSONB allows some flexible-schema data without a second datastore.

### Negative
- Horizontal write scaling is not automatic; a sharding or partitioning effort is possible if load far exceeds A2.
- Requires attention to vacuum/bloat, connection pooling, and index tuning.
- Managed-service choice may add some lock-in at the operations level (backups, extensions).

## Follow-ups
- [ ] Confirm or correct assumptions A1-A6 with <owner>; revise the status to Accepted.
- [ ] Fill in the load estimates (A2): <rows, QPS, growth>.
- [ ] Choose hosting: <managed vs. self-hosted>, <provider>, <region>.
- [ ] Define backup/restore targets (RPO <x>, RTO <y>) and test a restore.
- [ ] Select migration tooling and ORM/driver: <tool>.
- [ ] Set up monitoring and a connection-pooling policy.
- [ ] Set a review trigger: revisit this ADR if load exceeds <threshold> or requirements change.

Not verified: this is a generic template. No project files were inspected, and no option was benchmarked.