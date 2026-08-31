# OWNER: P1
#
# PURPOSE:
# Replay events from recorded/sample data.

import os
import json
import time
from typing import Generator, Dict, Any, List

class EventReplayer:
    def __init__(self, sample_file: str = None, speed: float = 1.0):
        self.speed = speed
        self.events: List[Dict[str, Any]] = []
        
        if sample_file and os.path.exists(sample_file):
            try:
                with open(sample_file, "r") as f:
                    self.events = json.load(f)
            except Exception as e:
                print(f"Error loading replay file: {e}")

    def replay(self, rate_per_second: int = 10) -> Generator[Dict[str, Any], None, None]:
        """
        Replay recorded events at a specified rate.
        If no events were loaded, generates mock trade events on the fly to replay.
        """
        delay = 1.0 / (rate_per_second * self.speed)
        
        if not self.events:
            # Fallback to dynamic generation if file is missing
            from generator.src.generator import MarketDataGenerator
            gen = MarketDataGenerator()
            for event in gen.generate_events(limit=1000):
                yield event
                time.sleep(delay)
        else:
            for event in self.events:
                yield event
                time.sleep(delay)
