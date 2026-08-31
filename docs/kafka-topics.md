# Kafka Topics and Event Flow

This document outlines the Kafka topic architecture and schema flow.

## Topics

1. **`market-data`**:
   - **Purpose**: Unified incoming stream of raw transaction ticks.
   - **Partitions**: 3 (for load distribution)
   - **Replication**: 1 (local simulation) or 3 (production deployment)
   - **Retention**: 24 hours
2. **`market-data-dlq`**:
   - **Purpose**: Direct destination for transactions failing validation.
   - **Partitions**: 1
   - **Replication**: 1

## Event Flow Diagram

```mermaid
sequenceDiagram
    participant G as Generator
    participant K as Kafka Broker
    participant P as Streaming Processor
    participant DLQ as DLQ Topic
    participant DB as ClickHouse

    G->>K: Emit trade record to 'market-data'
    K->>P: Fetch records
    alt Valid Event schema
        P->>P: Filter Duplicates
        P->>P: Align Watermarks
        P->>DB: Write VWAP & Anomalies
    else Invalid event schema
        P->>K: Write record to 'market-data-dlq'
    end
```