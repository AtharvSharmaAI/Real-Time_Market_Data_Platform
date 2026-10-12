# OWNER: P2
#
# PURPOSE:
# Kafka consumer wrapper.
#
# RESPONSIBILITIES:
# consume raw-trades
# deserialize
# pass events into processing pipeline
# commit offsets only according to chosen processing semantics
# document at-least-once/idempotency assumptions

import json
import logging
from typing import Dict, Any, Generator
from processor.src.config import settings

logger = logging.getLogger("processor.consumer")

class KafkaTradeConsumer:
    def __init__(self):
        self.consumer = None
        try:
            from confluent_kafka import Consumer
            self.consumer = Consumer({
                "bootstrap.servers": settings.bootstrap_servers,
                "group.id": settings.consumer_group,
                "auto.offset.reset": "earliest",
                "enable.auto.commit": False # manual commit for at-least-once delivery guarantees
            })
            self.consumer.subscribe([settings.input_topic])
            logger.info(f"Subscribed to Kafka topic: {settings.input_topic}")
        except ImportError:
            logger.warning("confluent-kafka not found. Running in simulation consumer mode.")

    def poll_messages(self, limit: int = 1000) -> Generator[Dict[str, Any], None, None]:
        """
        Polls messages from Kafka or generates simulation messages if Kafka is offline.
        """
        if self.consumer:
            # Poll from real Kafka
            received = 0
            while received < limit:
                try:
                    msg = self.consumer.poll(1.0)
                    if msg is not None and not msg.error():
                        received += 1
                        yield json.loads(msg.value().decode("utf-8"))
                except Exception as e:
                    logger.error(f"Error polling Kafka: {e}")
        else:
            # Generate simulated stream
            import random
            import time
            import uuid
            from datetime import datetime, timezone
            symbols = ["AAPL", "GOOGL", "MSFT", "AMZN"]
            for _ in range(limit):
                yield {
                    "event_id": f"evt-{uuid.uuid4().hex[:12]}",
                    "event_time": datetime.now(timezone.utc).isoformat(),
                    "symbol": random.choice(symbols),
                    "price": round(150.0 + random.uniform(-10.0, 10.0), 2),
                    "volume": float(random.randint(10, 500)),
                    "exchange": random.choice(["NYSE", "NASDAQ"]),
                    "side": random.choice(["BUY", "SELL"]),
                    "schema_version": "1.0.0"
                }
                time.sleep(0.01)  # ~100 events/s, like the generator default; unthrottled pins a CPU

    def commit(self):
        """
        Commit offsets manually to ensure at-least-once processing semantics.
        """
        if self.consumer:
            try:
                self.consumer.commit(asynchronous=False)
            except Exception as e:
                logger.error(f"Failed to commit Kafka offsets: {e}")
