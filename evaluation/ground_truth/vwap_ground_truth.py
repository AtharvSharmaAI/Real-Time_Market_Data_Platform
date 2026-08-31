# OWNER: P4
#
# PURPOSE:
# VWAP Ground Truth.

from typing import List, Dict, Any
from collections import defaultdict
from datetime import datetime

class VWAPGroundTruth:
    def __init__(self, events: List[Dict[str, Any]]):
        self.events = events

    def calculate_expected_vwap(self, window_size_sec: int = 5) -> Dict[str, List[Dict[str, Any]]]:
        """
        Calculate expected VWAP offline for 5s tumbling windows based on event_time.
        Returns a dict mapping symbol to a list of dicts:
        {
           "symbol": [
              {"window_start": str, "window_end": str, "vwap": float, "volume": float}
           ]
        }
        """
        symbol_events = defaultdict(list)
        for ev in self.events:
            if "event_time" in ev and "price" in ev and "volume" in ev and "symbol" in ev:
                try:
                    price = float(ev["price"])
                    volume = float(ev["volume"])
                    evt_time = datetime.fromisoformat(ev["event_time"].replace("Z", "+00:00"))
                    symbol_events[ev["symbol"]].append((evt_time, price, volume))
                except Exception:
                    continue

        expected = {}
        for symbol, evs in symbol_events.items():
            if not evs:
                continue
            evs.sort(key=lambda x: x[0])
            
            window_groups = defaultdict(list)
            for evt_time, price, volume in evs:
                epoch = int(evt_time.timestamp())
                w_idx = epoch // window_size_sec
                window_groups[w_idx].append((price, volume))
                
            expected[symbol] = []
            for w_idx in sorted(window_groups.keys()):
                group = window_groups[w_idx]
                w_start_epoch = w_idx * window_size_sec
                w_end_epoch = w_start_epoch + window_size_sec
                
                total_value = sum(p * v for p, v in group)
                total_volume = sum(v for _, v in group)
                vwap = total_value / total_volume if total_volume > 0 else 0.0
                
                expected[symbol].append({
                    "window_start": datetime.fromtimestamp(w_start_epoch).isoformat(),
                    "window_end": datetime.fromtimestamp(w_end_epoch).isoformat(),
                    "vwap": vwap,
                    "volume": total_volume
                })
                
        return expected
