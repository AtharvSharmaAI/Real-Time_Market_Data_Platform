# OWNER: P1
#
# PURPOSE:
# Inject duplicate events.

import random
from typing import Dict, Any, List

def inject_duplicate(event: Dict[str, Any], prob: float = 0.05, seed: int = None) -> List[Dict[str, Any]]:
    """
    Duplicate an event based on probability.
    Returns a list containing the original and optional duplicate event.
    """
    if seed is not None:
        h_val = hash(event.get("event_id", "0"))
        random.seed(seed + abs(h_val) % 10000)
        
    outputs = [event]
    if random.random() <= prob:
        # Keep same event_id to verify deduplication
        outputs.append(event.copy())
    return outputs
