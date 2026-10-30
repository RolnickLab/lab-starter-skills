# Data Systems & Reliability (DDIA)

## Core Concepts
*   **Reliability:** Systems must continue to work correctly even when things go wrong (fault-tolerance).
*   **Scalability:** Measure system behavior as load (requests, data volume) increases. Define your load parameters first.
*   **Maintainability:** Operability, Simplicity, and Evolvability.

## Data Models
*   **Systems of Record:** The authoritative version of data.
*   **Derived Data:** Data produced by transforming existing data (caches, indexes, materialized views).

## Consistency & CAP
*   **Linearizability (Strong Consistency):** Every operation appears to execute atomically at some point between its start and end.
*   **Eventual Consistency:** If no new updates are made to a data item, eventually all accesses will return the last updated value.
*   **CAP Theorem:** In the presence of a network partition (P), you must choose between Availability (A) and Consistency (C).

## Distributed Systems
*   **Single Point of Failure (SPOF):** Identify components that bring down the whole system if they fail.
*   **Idempotency:** Operations (especially in data pipelines) must be safe to retry without side effects.
