# OWNER: P2
#
# PURPOSE:
# Orchestration entry point.
#
# RESPONSIBILITIES:
# It will eventually connect:
# Kafka consumer
# -> validation
# -> deduplication
# -> event-time processing
# -> watermark
# -> windows
# -> analytics
# -> anomaly detection
# -> output Kafka topic
# Keep orchestration separate from business logic.

import json
import logging
import os
import time
from datetime import datetime
from typing import Dict, Any, List

from processor.src.config import settings
from processor.src.consumer import KafkaTradeConsumer
from processor.validation.validator import validate_event
from processor.deduplication.deduplicator import Deduplicator
from processor.event_time.event_time import parse_event_time
from processor.event_time.watermark import WatermarkTracker
from processor.event_time.late_events import LateEventHandler
from processor.windows.state import WindowStateStore
from processor.windows.tumbling_window import TumblingWindowAssigner
from processor.analytics.vwap import calculate_vwap
from processor.analytics.volume import calculate_total_volume
from processor.analytics.volatility import calculate_volatility
from processor.anomaly.detector import AnomalyDetector
from processor.dlq.dlq_producer import DLQProducer
from prometheus_client import Counter, Histogram, start_http_server

# Metric names match monitoring/grafana/dashboards/*.json and monitoring/alerts/alerts.yml
EVENTS_RECEIVED = Counter("events_received", "Raw events consumed")
EVENTS_PROCESSED = Counter("events_processed", "Events assigned to a window")
EVENTS_INVALID = Counter("events_invalid", "Events failing validation")
EVENTS_DUPLICATE = Counter("events_duplicate", "Duplicate events dropped")
EVENTS_LATE = Counter("events_late", "Late events dropped")
DLQ_EVENTS = Counter("dlq_events", "Events routed to the DLQ")
ANOMALIES = Counter("anomalies_detected", "Windows flagged as anomalous", ["anomaly_type"])
LATENCY = Histogram("processing_latency_seconds", "Event time to processing time")

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("processor.main")

class ProcessingPipeline:
    def __init__(self):
        self.config = settings
        self.consumer = KafkaTradeConsumer()
        self.deduplicator = Deduplicator(ttl_seconds=self.config.dedup_ttl_sec)
        self.watermark_tracker = WatermarkTracker(delay_seconds=self.config.watermark_delay_sec)
        self.late_event_handler = LateEventHandler(self.watermark_tracker)
        self.window_state = WindowStateStore()
        self.window_assigner = TumblingWindowAssigner(size_seconds=self.config.window_size_sec)
        self.anomaly_detector = AnomalyDetector(threshold=self.config.anomaly_threshold)
        self.dlq_producer = DLQProducer(bootstrap_servers=self.config.bootstrap_servers, topic=self.config.dlq_topic)
        
        # In-memory record of open windows to check for finalization
        # Maps (symbol, window_start, window_end) -> window_end
        self.tracked_windows: Dict[tuple, datetime] = {}
        
        # Setup Kafka output producer if confluent-kafka is available
        self.producer = None
        try:
            from confluent_kafka import Producer
            self.producer = Producer({"bootstrap.servers": self.config.bootstrap_servers})
            logger.info("Initialized Kafka Output Producer.")
        except ImportError:
            logger.warning("confluent-kafka not found. Running output in simulation mode.")

    def run(self, limit: int = 100):
        """
        Runs the stream processing loop.
        """
        logger.info("Starting processing pipeline loop...")
        
        processed_count = 0
        for raw_msg in self.consumer.poll_messages(limit=limit):
            processed_count += 1
            EVENTS_RECEIVED.inc()
            try:
                # 1. Validation
                try:
                    valid_trade = validate_event(raw_msg)
                except Exception as val_err:
                    logger.warning(f"Validation failed: {val_err}. Routing to DLQ.")
                    EVENTS_INVALID.inc()
                    DLQ_EVENTS.inc()
                    self.dlq_producer.send_to_dlq(raw_msg, str(val_err))
                    continue

                # 2. Deduplication
                if self.deduplicator.is_duplicate(valid_trade.event_id):
                    EVENTS_DUPLICATE.inc()
                    logger.info(f"Duplicate event detected: {valid_trade.event_id}. Dropping.")
                    continue

                # 3. Event-time extraction and watermark update
                evt_time = parse_event_time(valid_trade.event_time)
                watermark = self.watermark_tracker.update(evt_time)

                # 4. Late event handling
                if self.late_event_handler.is_late(evt_time):
                    EVENTS_LATE.inc()
                    logger.warning(f"Late event dropped: {valid_trade.event_id} (event_time: {evt_time}, watermark: {watermark})")
                    continue

                # 5. Tumbling Window Assignment
                w_start, w_end = self.window_assigner.assign(evt_time)
                symbol = valid_trade.symbol
                
                # Add to WindowStateStore
                trade_dict = valid_trade.model_dump()
                self.window_state.add_to_window(symbol, w_start, w_end, trade_dict)
                
                window_key = (symbol, w_start, w_end)
                self.tracked_windows[window_key] = w_end
                EVENTS_PROCESSED.inc()
                LATENCY.observe(max((datetime.now(evt_time.tzinfo) - evt_time).total_seconds(), 0))

                # 6. Check and Finalize Windows
                # A window is finalized when the watermark is strictly greater than the window_end
                finalized_keys = []
                for key, end_time in self.tracked_windows.items():
                    if watermark >= end_time:
                        self.finalize_window(key[0], key[1], key[2])
                        finalized_keys.append(key)
                
                # Remove finalized windows from tracking
                for key in finalized_keys:
                    del self.tracked_windows[key]

            except Exception as e:
                logger.error(f"Error processing event: {e}", exc_info=True)
                
            # Commit offsets for at-least-once processing
            self.consumer.commit()
            
        logger.info(f"Processing loop completed. Processed {processed_count} messages.")

    def finalize_window(self, symbol: str, start: datetime, end: datetime):
        """
        Calculate metrics and anomalies for a window, then output the result.
        """
        trades = self.window_state.get_events(symbol, start, end)
        if not trades:
            return

        # Calculate aggregates
        vwap = calculate_vwap(trades)
        total_vol = calculate_total_volume(trades)
        volatility = calculate_volatility(trades)

        # Anomaly detection
        anomaly_flag, anomaly_type, anomaly_score = self.anomaly_detector.detect(
            symbol, vwap, total_vol, volatility
        )

        if anomaly_flag:
            ANOMALIES.labels(anomaly_type).inc()

        output_payload = {
            "symbol": symbol,
            "window_start": start.isoformat(),
            "window_end": end.isoformat(),
            "vwap": vwap,
            "volume": total_vol,
            "volatility": volatility,
            "anomaly_flag": 1 if anomaly_flag else 0,
            "anomaly_type": anomaly_type,
            "anomaly_score": anomaly_score,
            "processed_at": datetime.utcnow().isoformat()
        }

        # Write output payload
        if self.producer:
            try:
                self.producer.produce(
                    self.config.output_topic,
                    key=symbol,
                    value=json.dumps(output_payload)
                )
                self.producer.flush()
                logger.info(f"Produced finalized window to Kafka: {symbol} [{start} - {end}]")
            except Exception as e:
                logger.error(f"Failed to produce window result to Kafka: {e}")
        else:
            logger.info(f"[PROCESSED WINDOW SIMULATION] {json.dumps(output_payload)}")

        # Purge state to avoid memory leak
        self.window_state.purge_window(symbol, start, end)

if __name__ == "__main__":
    start_http_server(int(os.getenv("PROCESSOR_METRICS_PORT", "8001")))  # Prometheus scrape target
    pipeline = ProcessingPipeline()
    # Loop indefinitely in production/simulation running
    pipeline.run(limit=9999999)
