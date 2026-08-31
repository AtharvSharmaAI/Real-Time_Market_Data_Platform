# OWNER: P2
#
# PURPOSE:
# DLQ producer.
#
# RESPONSIBILITIES:
# - Write malformed/failed messages to DLQ topic
# - Support fallback simulation logging

import json
import logging
from typing import Dict, Any

logger = logging.getLogger("processor.dlq")

class DLQProducer:
    def __init__(self, bootstrap_servers: str = None, topic: str = "dlq-events"):
        self.topic = topic
        self.producer = None
        
        # Try to initialize confluent_kafka producer
        try:
            from confluent_kafka import Producer
            if bootstrap_servers:
                self.producer = Producer({"bootstrap.servers": bootstrap_servers})
                logger.info(f"Initialized Kafka DLQ Producer for topic: {topic}")
        except ImportError:
            logger.warning("confluent-kafka not found. Running DLQ in simulation mode.")

    def send_to_dlq(self, payload: Dict[str, Any], error_message: str):
        """
        Produce validation failure payload and error context to DLQ.
        """
        dlq_event = {
            "raw_payload": json.dumps(payload),
            "error_message": error_message
        }
        
        if self.producer:
            try:
                self.producer.produce(
                    self.topic,
                    key=payload.get("event_id", "unknown"),
                    value=json.dumps(dlq_event)
                )
                self.producer.flush()
                logger.info(f"Sent event to Kafka DLQ: {payload.get('event_id')}")
                return
            except Exception as e:
                logger.error(f"Failed to produce to Kafka DLQ: {e}")
                
        # Simulation mode fallback
        logger.info(f"[DLQ SIMULATION] event_id={payload.get('event_id')} - Error: {error_message}")
