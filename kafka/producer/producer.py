# OWNER: P1
#
# PURPOSE:
# Kafka producer functionality.
#
# RESPONSIBILITIES:
# Kafka producer
# serialization
# event key
# retry behavior
# delivery acknowledgement
# producer metrics
# graceful shutdown

import json
import logging
from typing import Dict, Any, Callable, Optional

logger = logging.getLogger("kafka.producer")

class KafkaTradeProducer:
    def __init__(self, bootstrap_servers: str = "localhost:9092", client_id: str = "market-data-producer"):
        self.producer = None
        self.bootstrap_servers = bootstrap_servers
        self.client_id = client_id
        
        # Configure producer with delivery-guarantees
        config = {
            "bootstrap.servers": bootstrap_servers,
            "client.id": client_id,
            "acks": "all",  # Strongest delivery guarantee
            "retries": 5,
            "retry.backoff.ms": 100,
            "max.in.flight.requests.per.connection": 1,  # Prevent message reordering during retries
            "compression.type": "snappy",
            "linger.ms": 10,
            "batch.size": 16384
        }
        
        try:
            from confluent_kafka import Producer
            self.producer = Producer(config)
            logger.info(f"Initialized confluent-kafka Producer referencing: {bootstrap_servers}")
        except ImportError:
            logger.warning("confluent-kafka not found. Running Producer in simulation mode.")

    def _delivery_report(self, err, msg):
        """
        Callback triggered when delivery completes.
        Used for monitoring / metric gathering.
        """
        if err is not None:
            logger.error(f"Message delivery failed: {err}")
        else:
            logger.debug(f"Message delivered to {msg.topic()} [{msg.partition()}] at offset {msg.offset()}")

    def produce(self, topic: str, key: str, value: Dict[str, Any], callback: Optional[Callable] = None):
        """
        Serialize payload to JSON and write to target topic with key.
        """
        serialized_val = json.dumps(value).encode("utf-8")
        
        # Use custom or default delivery callback
        cb = callback or self._delivery_report
        
        if self.producer:
            try:
                self.producer.produce(
                    topic,
                    key=key.encode("utf-8") if key else None,
                    value=serialized_val,
                    callback=cb
                )
                # Poll to invoke delivery callbacks
                self.producer.poll(0)
            except Exception as e:
                logger.error(f"Error producing message to topic {topic}: {e}")
        else:
            # Simulation logger
            logger.info(f"[PRODUCER SIMULATION] topic={topic} key={key} payload={value}")

    def flush(self, timeout: float = 10.0):
        """
        Flush outstanding messages before shut down.
        """
        if self.producer:
            logger.info("Flushing pending messages...")
            self.producer.flush(timeout)
            logger.info("Producer shut down gracefully.")
