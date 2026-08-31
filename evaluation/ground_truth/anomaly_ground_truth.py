# OWNER: P4
#
# PURPOSE:
# Anomaly Ground Truth.

from typing import List, Dict, Any
from collections import defaultdict
import math

class AnomalyGroundTruth:
    def __init__(self, events: List[Dict[str, Any]]):
        self.events = events

    def generate_expected_anomalies(self, threshold_factor: float = 3.0) -> List[Dict[str, Any]]:
        """
        Calculates expected price/volume anomalies offline based on a running Z-score simulation.
        Produces expected anomaly events:
        [
           {"symbol": str, "anomaly_type": str, "anomaly_score": float, "event_id": str}
        ]
        """
        expected_anomalies = []
        symbol_price_history = defaultdict(list)
        symbol_volume_history = defaultdict(list)
        
        # Sort events chronologically to simulate stream processing
        sorted_events = sorted(self.events, key=lambda e: e.get("event_time", ""))
        
        for ev in sorted_events:
            symbol = ev.get("symbol")
            price = ev.get("price")
            volume = ev.get("volume")
            event_id = ev.get("event_id")
            
            if not symbol or price is None or volume is None:
                continue
                
            try:
                price = float(price)
                volume = float(volume)
            except ValueError:
                continue

            # Price Anomaly Z-Score Check
            prices = symbol_price_history[symbol]
            if len(prices) >= 5:
                mean = sum(prices) / len(prices)
                variance = sum((x - mean) ** 2 for x in prices) / len(prices)
                std_dev = math.sqrt(variance)
                if std_dev > 0:
                    z_score = abs(price - mean) / std_dev
                    if z_score > threshold_factor:
                        expected_anomalies.append({
                            "symbol": symbol,
                            "anomaly_type": "PRICE_SPIKE",
                            "anomaly_score": z_score,
                            "event_id": event_id
                        })
            
            # Volume Anomaly Z-Score Check
            volumes = symbol_volume_history[symbol]
            if len(volumes) >= 5:
                mean = sum(volumes) / len(volumes)
                variance = sum((x - mean) ** 2 for x in volumes) / len(volumes)
                std_dev = math.sqrt(variance)
                if std_dev > 0:
                    z_score = abs(volume - mean) / std_dev
                    if z_score > threshold_factor:
                        expected_anomalies.append({
                            "symbol": symbol,
                            "anomaly_type": "VOLUME_SPIKE",
                            "anomaly_score": z_score,
                            "event_id": event_id
                        })

            # Append to history, keeping size moderate (e.g. 50 events)
            prices.append(price)
            if len(prices) > 50:
                prices.pop(0)
                
            volumes.append(volume)
            if len(volumes) > 50:
                volumes.pop(0)
                
        return expected_anomalies
