# OWNER: P2
#
# PURPOSE:
# Configuration for processor.
#
# RESPONSIBILITIES:
# Configuration for:
# - Kafka bootstrap servers
# - consumer group
# - topics
# - watermark delay
# - window size
# - anomaly threshold

import os

class ProcessorConfig:
    def __init__(self):
        self.bootstrap_servers = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
        self.consumer_group = os.getenv("KAFKA_CONSUMER_GROUP", "market-data-processor-group")
        self.input_topic = os.getenv("KAFKA_INPUT_TOPIC", "market-trades")
        self.output_topic = os.getenv("KAFKA_OUTPUT_TOPIC", "processed-events")
        self.dlq_topic = os.getenv("KAFKA_DLQ_TOPIC", "dlq-events")
        self.watermark_delay_sec = int(os.getenv("WATERMARK_DELAY_SEC", "3"))
        self.window_size_sec = int(os.getenv("WINDOW_SIZE_SEC", "5"))
        self.anomaly_threshold = float(os.getenv("ANOMALY_THRESHOLD", "3.0"))
        self.dedup_ttl_sec = int(os.getenv("DEDUP_TTL_SEC", "60"))

# Singleton instance
settings = ProcessorConfig()
