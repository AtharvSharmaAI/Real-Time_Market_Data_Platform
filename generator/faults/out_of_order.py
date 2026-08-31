# OWNER: P1
#
# PURPOSE:
# Inject out-of-order events.

import random
from typing import Dict, Any, List

class OutOfOrderInjector:
    def __init__(self, prob: float = 0.1, buffer_size: int = 5, seed: int = None):
        self.prob = prob
        self.buffer_size = buffer_size
        self.buffer: List[Dict[str, Any]] = []
        if seed is not None:
            random.seed(seed)

    def process_event(self, event: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Buffering events to release them out of order.
        Returns a list of events ready to be emitted.
        """
        self.buffer.append(event)
        
        # If buffer is full or randomly triggered, flush buffer out-of-order
        if len(self.buffer) >= self.buffer_size or (len(self.buffer) > 1 and random.random() <= self.prob):
            # Shuffle the buffer to create disorder
            random.shuffle(self.buffer)
            flushed = list(self.buffer)
            self.buffer.clear()
            return flushed
            
        return []

    def flush(self) -> List[Dict[str, Any]]:
        """Flush remaining buffered events."""
        flushed = list(self.buffer)
        self.buffer.clear()
        return flushed
