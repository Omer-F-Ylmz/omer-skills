# ADR-[NNN]: Choose the primary database for [system name]

## Status
Proposed ([date], [author/approvers])

## Context
[System name] needs a primary store for its core transactional data ([main entities, e.g. users, orders, payments]). The data is mostly relational and has integrity rules between entities. Some attributes vary by record and need semi-structured storage. Expected load is [X reads/s, Y writes/s], growing to [size] within [time span]. The team knows [current skills]. Hosting will be [cloud provider / on-prem]. No database has been chosen yet. Everything that depends on the database (ORM, migrations, backups, hosting) is waiting on this decision.

## Decision drivers
1. Data integrity: ACID transactions across several entities, plus foreign keys and constraints.
2. Query flexibility: joins, aggregations and ad-hoc reporting without a second store.
3. Semi-structured data: store variable attributes without a schema migration for every change.
4. Operational burden: a managed offering, backups, point-in-time recovery and a small ops team.
5. Scalability to [target load]: vertical scaling plus read replicas must be enough for that horizon.
6. Ecosystem and skills: driver/ORM support in [language/framework], plus team familiarity and hiring pool.
7. Cost and lock-in: licence cost, managed-service cost and how easily data can be moved out.

## Options considered

### Option A: PostgreSQL
- Pro: full ACID, strong constraints, rich SQL (CTEs, window functions).
- Pro: JSONB with indexing covers semi-structured data in the same store.
- Pro: open-source licence, available as a managed service from every major cloud, low lock-in.
- Pro: broad extensions (full-text search, PostGIS, pgvector) can delay adding extra stores.
- Con: horizontal write scaling needs extra tooling (Citus, sharding) or a different design.
- Con: needs tuning knowledge (vacuum, connection pooling) at higher load.

### Option B: MySQL / MariaDB
- Pro: ACID with InnoDB, mature, widely known, many managed offerings.
- Pro: good read-replica support and predictable performance for simple OLTP access.
- Con: JSON support and advanced SQL features are weaker than PostgreSQL's.
- Con: some behaviour differs by version and fork (MySQL vs MariaDB), which complicates portability.
- Con: horizontal write scaling also needs extra tooling (Vitess, sharding).

### Option C: MongoDB (document store)
- Pro: flexible schema fits semi-structured and fast-changing data.
- Pro: built-in sharding for horizontal scale.
- Pro: natural mapping to nested objects in application code.
- Con: multi-document transactions exist but are costlier and less idiomatic, and relational integrity moves into application code.
- Con: joins and ad-hoc reporting are weaker and often need a separate analytics store.
- Con: SSPL licence and a mostly vendor-managed offering (Atlas) raise lock-in and cost concerns.

### Option D: Distributed SQL (e.g. CockroachDB, Spanner, YugabyteDB)
- Pro: SQL and ACID with horizontal write scaling and multi-region support.
- Pro: PostgreSQL wire compatibility (CockroachDB, YugabyteDB) eases migration.
- Con: higher latency per transaction and higher cost at small scale.
- Con: partial feature compatibility, smaller ecosystem and fewer people who know it.
- Con: stronger vendor or licence lock-in depending on the product.

## Decision
Proposed: **PostgreSQL**, run as [managed service, e.g. AWS RDS / Azure Database for PostgreSQL / Cloud SQL].

Rationale by driver:
- Drivers 1 and 2: it is the only option here that offers full relational integrity and rich SQL without trade-offs.
- Driver 3: JSONB covers variable attributes, so a separate document store is not needed.
- Driver 4: mature managed offerings give backups and PITR out of the box.
- Driver 5: [target load] fits vertical scaling plus read replicas. Option D's horizontal scaling is not needed at this horizon, so its cost and latency are not justified.
- Drivers 6 and 7: wide ORM support, an open licence and low lock-in. [Confirm team skills.]

## Consequences

### Positive
- Business data has a single store with strong integrity guarantees.
- Reporting can run directly with SQL, at least at first.
- Low licence cost and a straightforward exit path because of the open format and wire protocol.

### Negative
- Write scaling beyond one primary will need sharding or a move to Option D. That is a known future cost.
- JSONB overuse can hide schema design problems, so conventions are needed.
- The team needs operating skills for vacuum, indexing and connection pooling.

### Follow-ups
- [ ] Confirm the load and growth figures in Context. Revisit this ADR if write load passes [threshold].
- [ ] Choose the managed provider and instance class, then estimate monthly cost.
- [ ] Choose the migration tool ([e.g. Flyway / EF Core migrations / Alembic]) and naming conventions.
- [ ] Set up connection pooling ([e.g. PgBouncer]) and read-replica routing.
- [ ] Define the backup/PITR retention policy and test a restore.
- [ ] Write JSONB usage rules: when a column instead of JSONB, and which indexes.

---
Not covered: I had no details about the project, so the load figures, stack, team skills and hosting are placeholders. The PostgreSQL decision depends on those assumptions and should be checked against them before the status moves to Accepted.