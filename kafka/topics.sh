#!/bin/bash
# OWNER: P1
#
# PURPOSE:
# Document and create Kafka topics.
#
# RESPONSIBILITIES:
# Create and configure the following topics:
# - market-trades
# - processed-events
# - dlq-events
#
# Partitioning Strategy:
# - Key: symbol (Ticker symbol)
# - Partitions: 3 (supports parallel consumers per symbol group)
# - Partitioning Strategy: Murmur2 key-based partition hashing (guarantees chronological ordering per symbol)

BOOTSTRAP_SERVERS=${KAFKA_BOOTSTRAP_SERVERS:-"localhost:9092"}

echo "Initializing Kafka topics on bootstrap server: ${BOOTSTRAP_SERVERS}..."

# 1. market-trades
# Purpose: Raw trades stream
# Producer: Generator
# Consumer: Processor
echo "Creating topic 'market-trades'..."
kafka-topics --bootstrap-server ${BOOTSTRAP_SERVERS} \
  --create --if-not-exists \
  --topic market-trades \
  --partitions 3 \
  --replication-factor 1 \
  --config cleanup.policy=delete \
  --config retention.ms=86400000 # 24 hours retention

# 2. processed-events
# Purpose: Completed tumbling windows (vwap, volatility, anomaly flags)
# Producer: Processor
# Consumer: ClickHouse Sink, API / Alerting
echo "Creating topic 'processed-events'..."
kafka-topics --bootstrap-server ${BOOTSTRAP_SERVERS} \
  --create --if-not-exists \
  --topic processed-events \
  --partitions 3 \
  --replication-factor 1 \
  --config cleanup.policy=delete \
  --config retention.ms=604800000 # 7 days retention

# 3. dlq-events
# Purpose: Failed schema/domain validations or processing issues
# Producer: Processor
# Consumer: DLQ archiver, Debugging tools
echo "Creating topic 'dlq-events'..."
kafka-topics --bootstrap-server ${BOOTSTRAP_SERVERS} \
  --create --if-not-exists \
  --topic dlq-events \
  --partitions 1 \
  --replication-factor 1 \
  --config cleanup.policy=delete \
  --config retention.ms=1209600000 # 14 days retention

echo "All topics successfully initialized/verified."
