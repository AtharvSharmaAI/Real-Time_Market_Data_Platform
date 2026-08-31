# Kafka Connect ClickHouse Sink

**OWNER:** P3

This module defines the integration layer that captures real-time data from Kafka topics and persists them into ClickHouse database tables.

## Connector Specifications

The Kafka Connect integration relies on the `com.clickhouse.kafka.connect.ClickHouseSinkConnector` to deliver high-throughput, low-latency writes to the OLAP ClickHouse backend.

### 1. Kafka Topics
* **`market-trades`**: Raw trade feeds pushed by the data generator. Routed directly to the `raw_events` table in ClickHouse.
* **`processed-events`**: Volatility, VWAP, and anomaly indicators computed by the streaming processor. Routed directly to the `processed_events` table in ClickHouse.
* **`dlq-events`**: Captures any raw payloads that fail validation or parsing during processing. Routed to the `dlq_events` table in ClickHouse.

### 2. ClickHouse Destination
* Database Name: `market_data`
* Table naming conventions match topic names directly:
  * `market-trades` ➔ `raw_events`
  * `processed-events` ➔ `processed_events`
  * `dlq-events` ➔ `dlq_events`

### 3. Serialization
* **Value Serialization**: Evaluated as `org.apache.kafka.connect.json.JsonConverter` with `schemas.enable=false`. Because trades and metric payloads are lightweight and dynamic, schema-less JSON provides maximum agility.
* **Key Serialization**: Evaluated as `org.apache.kafka.connect.storage.StringConverter` representing the trading ticker symbol (`symbol`).

### 4. Batching
* **`clickhouse.sink.batch.size`**: Set to `1000`. ClickHouse performs best with large batch inserts rather than single-record transactions. Batching avoids building up too many tiny parts in the MergeTree tables.

### 5. Retries & Backoff
* **`clickhouse.sink.max.retries`**: Set to `5`.
* **`clickhouse.sink.retry.backoff.ms`**: Set to `5000` (5 seconds). In case of database downtime or network blips, the connector backs off and retries to avoid dataloss.

### 6. Delivery Semantics
* **`clickhouse.sink.delivery.semantics`**: Configured to `at_least_once`. Under failover or coordinator rebalances, Kafka Connect guarantees that every event is written to ClickHouse. The tables use unique keys (`event_id` or window boundaries) to allow deduplication where needed.

### 7. DLQ Configuration
* Failures in serialization or write constraints are captured via:
  * `errors.tolerance = all`
  * `errors.deadletterqueue.topic.name = dlq-events`
  * `errors.deadletterqueue.context.headers.enable = true`

## Deployment & Verification
To register the connector with a running Kafka Connect cluster, run the following HTTP request:
```bash
curl -X POST -H "Content-Type: application/json" \
  --data @clickhouse-sink.json \
  http://localhost:8083/connectors
```
To verify connector health status:
```bash
curl -s http://localhost:8083/connectors/clickhouse-sink-connector/status
```
