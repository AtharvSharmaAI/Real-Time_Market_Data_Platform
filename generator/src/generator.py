# OWNER: P1
#
# PURPOSE:
# Generate realistic market-style trade events.

import random
from datetime import datetime, timezone
from typing import Generator, Dict, Any

from generator.src.config import settings
from generator.src.market_data import MarketSimulator
from generator.src.schemas import MarketTradeEvent

# Import fault injection functions
from generator.faults.malformed import inject_malformation
from generator.faults.duplicate import inject_duplicate
from generator.faults.late_events import inject_lateness
from generator.faults.anomalies import inject_anomaly
from generator.faults.out_of_order import OutOfOrderInjector
from generator.faults.traffic_burst import TrafficBurstController

class MarketDataGenerator:
    def __init__(self, seed: int = None):
        self.config = settings
        self.simulator = MarketSimulator(seed=seed or self.config.seed)
        self.out_of_order_injector = OutOfOrderInjector(
            prob=self.config.prob_out_of_order,
            seed=seed or self.config.seed
        )
        self.burst_controller = TrafficBurstController(
            multiplier=self.config.burst_multiplier
        )
        self.seq_num = 0
        if seed is not None:
            random.seed(seed)

    def generate_events(self, limit: int = 100) -> Generator[Dict[str, Any], None, None]:
        """
        Generate raw trade events and pass them through fault injection rules.
        """
        produced = 0
        while produced < limit:
            self.seq_num += 1
            symbol = random.choice(self.config.symbols)
            price, volume, side = self.simulator.generate_next_trade(symbol)
            
            # 1. Construct canonical trade event
            trade_obj = MarketTradeEvent(
                event_id=f"evt-{self.seq_num:06d}-{random.randint(1000, 9999)}",
                event_time=datetime.now(timezone.utc),
                symbol=symbol,
                price=price,
                volume=volume,
                exchange="NASDAQ" if random.random() > 0.5 else "NYSE",
                side=side
            )
            
            event = trade_obj.model_dump()
            # Convert event_time to ISO format string
            event["event_time"] = event["event_time"].isoformat()

            # 2. Inject anomalies (price/volume spikes)
            event = inject_anomaly(event, prob=self.config.prob_anomaly)

            # 3. Inject lateness (alter event_time)
            event = inject_lateness(event, prob=self.config.prob_late)

            # 4. Inject malformations
            event = inject_malformation(event, prob=self.config.prob_malformed)

            # 5. Inject duplicates (can yield multiple events)
            events_to_emit = inject_duplicate(event, prob=self.config.prob_duplicate)

            # 6. Inject out-of-order boundaries
            for ev in events_to_emit:
                ordered_events = self.out_of_order_injector.process_event(ev)
                for o_ev in ordered_events:
                    yield o_ev
                    produced += 1
                    if produced >= limit:
                        return

        # Flush any remaining events in out-of-order buffer
        for o_ev in self.out_of_order_injector.flush():
            yield o_ev

if __name__ == "__main__":
    import time
    import json
    
    print("Starting generator loop...")
    gen = MarketDataGenerator()
    
    producer = None
    try:
        from confluent_kafka import Producer
        producer = Producer({"bootstrap.servers": gen.config.bootstrap_servers})
        print(f"Initialized confluent-kafka Producer. Sending events to {gen.config.input_topic}...")
    except ImportError:
        print("confluent-kafka not found. Running generator in console log mode...")
        
    try:
        # Loop indefinitely
        for event in gen.generate_events(limit=9999999):
            if producer:
                producer.produce(
                    gen.config.input_topic,
                    key=event["symbol"],
                    value=json.dumps(event)
                )
                producer.poll(0)
            else:
                print(json.dumps(event))
            
            # Control rate based on baseline_rate configuration
            sleep_time = 1.0 / float(gen.config.baseline_rate) if gen.config.baseline_rate else 0.05
            time.sleep(sleep_time)
            
        if producer:
            producer.flush()
    except KeyboardInterrupt:
        print("Generator stopped by user.")
