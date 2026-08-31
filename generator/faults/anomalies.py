# OWNER: P1
#
# PURPOSE:
# Inject data anomalies.

import random
from typing import Dict, Any

def inject_anomaly(event: Dict[str, Any], prob: float = 0.05, seed: int = None) -> Dict[str, Any]:
    """
    Randomly inject a price or volume spike.
    """
    if seed is not None:
        h_val = hash(event.get("event_id", "0"))
        random.seed(seed + abs(h_val) % 10000)
        
    if random.random() > prob:
        return event
        
    anomalous = event.copy()
    anomaly_type = random.choice(["price_spike", "volume_spike"])
    
    if anomaly_type == "price_spike":
        # Spike price by 5x to 10x
        anomalous["price"] = round(anomalous.get("price", 100.0) * random.uniform(5.0, 10.0), 2)
    elif anomaly_type == "volume_spike":
        # Spike volume by 5x to 10x
        anomalous["volume"] = float(anomalous.get("volume", 50.0) * random.randint(5, 10))
        
    return anomalous
