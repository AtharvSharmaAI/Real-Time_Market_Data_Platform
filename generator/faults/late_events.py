# OWNER: P1
#
# PURPOSE:
# Inject late events.

import random
from datetime import datetime, timedelta
from typing import Dict, Any

def inject_lateness(event: Dict[str, Any], prob: float = 0.15, lateness_sec: float = 9.0, seed: int = None) -> Dict[str, Any]:
    """
    Modifies the event_time of the event to make it late based on probability.
    """
    if seed is not None:
        h_val = hash(event.get("event_id", "0"))
        random.seed(seed + abs(h_val) % 10000)
        
    if random.random() > prob:
        return event
        
    corrupted = event.copy()
    original_time_str = corrupted.get("event_time")
    
    # Parse and subtract lateness
    try:
        if isinstance(original_time_str, str):
            original_time = datetime.fromisoformat(original_time_str.replace("Z", "+00:00"))
            late_time = original_time - timedelta(seconds=lateness_sec)
            corrupted["event_time"] = late_time.isoformat()
        elif isinstance(original_time_str, datetime):
            late_time = original_time_str - timedelta(seconds=lateness_sec)
            corrupted["event_time"] = late_time
    except Exception:
        pass
        
    return corrupted
