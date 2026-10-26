# Database Scaling & Architecture Patterns

This guide details the patterns for scaling data systems beyond a single node.

## 1. Vertical vs. Horizontal Scaling

### Vertical Scaling (Scale Up)
*   **Strategy:** Buy a bigger server (More RAM, CPU, faster NVMe).
*   **Pros:** Simplicity. No code changes. No network overhead.
*   **Cons:** Hardware limits. Cost curve becomes exponential.
*   **Guideline:** Always scale up first. Modern hardware (128 cores, 2TB RAM) can handle massive loads. Do not shard until you hit the limit of the biggest available instance.

### Horizontal Scaling (Scale Out)
*   **Strategy:** Add more nodes.
*   **Pros:** Infinite theoretical scale. Cheaper commodity hardware.
*   **Cons:** Distributed system complexity (CAP theorem), network latency, consistency challenges.

## 2. Read Scaling: Replication

Use this when **Read Load >>> Write Load** (Common web app pattern).

*   **Primary Node:** Handles all Writes and some Reads.
*   **Replica Nodes:** Handle only Reads. Async replication from Primary.
*   **Challenge:** **Replication Lag**. Data written to Primary might not appear on Replica immediately (Eventual Consistency).
*   **Mitigation:**
    *   **Sticky Sessions:** Read your own writes (route user to Primary for their own data).
    *   **Versioning:** Check version token to verify replica is up to date.

## 3. Write Scaling: Sharding (Partitioning)

Use this when **Write Volume > Single Node Capacity** or **Data Size > Single Disk**.

*   **Strategy:** Split data across nodes by a "Shard Key" (e.g., User ID, Region).
*   **Sharding Patterns:**
    *   **Key Range:** A-M on Node 1, N-Z on Node 2. (Hotspot risk if everyone adds "Apple").
    *   **Hash:** `hash(key) % num_shards`. (Uniform distribution, but adding nodes requires rebalancing).
*   **Cons:**
    *   **Cross-Shard Joins:** Extremely expensive. Avoid them.
    *   **Transactions:** Distributed transactions (2PC) are slow.

## 4. Indexing Strategy

Indexes are the single biggest performance lever.

### B-Tree (Default)
*   **Use:** Equality (`=`) and Range (`<`, `>`).
*   **Note:** Left-prefix rule. Index `(A, B)` supports query on `A` and `(A, B)`, but NOT `B` alone.

### Hash Index
*   **Use:** Only Equality (`=`). O(1) lookup.
*   **Cons:** No range queries.

### GIN (Generalized Inverted Index)
*   **Use:** JSONB, Arrays, Full Text Search.
*   **Pattern:** "Inverted Index" maps values to rows (like a book index).

### BRIN (Block Range Index)
*   **Use:** Time-series or naturally ordered data on disk.
*   **Pros:** Tiny size.
*   **Cons:** Only works if data is physically sorted.

## 5. Caching Patterns

### Cache-Aside (Lazy Loading)
1.  App asks Cache.
2.  Hit? Return.
3.  Miss? App asks DB -> Write to Cache -> Return.
*   **Pros:** Resilient to cache failure (DB is source of truth).
*   **Cons:** First hit is slow. Stale data if DB changes without cache update.

### Write-Through
1.  App writes to Cache AND DB synchronously.
*   **Pros:** Consistency.
*   **Cons:** Higher write latency.

### Write-Back (Write-Behind)
1.  App writes to Cache.
2.  Cache async writes to DB.
*   **Pros:** Fast writes.
*   **Cons:** Data loss if Cache crashes before flush. Use for metrics/logs, not financial data.
