# OWNER: P1
#
# PURPOSE:
# Inject malformed events.

import random
from typing import Dict, Any

def inject_malformation(event: Dict[str, Any], prob: float = 0.1, seed: int = None) -> Dict[str, Any]:
    """
    Randomly corrupt an event based on probability.
    """
    if seed is not None:
        # Avoid seed synchronization across multiple runs by using hash of event ID
        h_val = hash(event.get("event_id", "0"))
        random.seed(seed + abs(h_val) % 10000)
        
    if random.random() > prob:
        return event
        
    corrupted = event.copy()
    corruption_type = random.choice(["missing", "wrong_type", "invalid_value"])
    
    if corruption_type == "missing":
        field_to_remove = random.choice(["symbol", "price", "volume", "side"])
        if field_to_remove in corrupted:
            del corrupted[field_to_remove]
    elif corruption_type == "wrong_type":
        field_to_corrupt = random.choice(["price", "volume", "event_time"])
        corrupted[field_to_corrupt] = "corrupted_string_value"
    elif corruption_type == "invalid_value":
        field_to_corrupt = random.choice(["price", "volume", "side"])
        if field_to_corrupt == "price":
            corrupted["price"] = -50.0
        elif field_to_corrupt == "volume":
            corrupted["volume"] = 0.0
        elif field_to_corrupt == "side":
            corrupted["side"] = "HOLD"
            
    return corrupted
