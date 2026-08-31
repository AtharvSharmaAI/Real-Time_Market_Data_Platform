# OWNER: P4
#
# PURPOSE:
# Throughput metrics.

from typing import List, Dict, Any
from collections import defaultdict
from datetime import datetime

def calculate_throughput(
    processed_events: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """
    Measure:
    - events/sec (average throughput)
    - peak events/sec (maximum throughput within a 1-second window)
    """
    if not processed_events:
        return {
            "avg_throughput_eps": 0.0,
            "peak_throughput_eps": 0.0
        }
        
    sec_counts = defaultdict(int)
    timestamps = []
    
    for ev in processed_events:
        proc_time_str = ev.get("processed_at") or ev.get("processing_time")
        if proc_time_str:
            try:
                t = datetime.fromisoformat(proc_time_str.replace("Z", "+00:00"))
                second_bucket = int(t.timestamp())
                sec_counts[second_bucket] += 1
                timestamps.append(second_bucket)
            except Exception:
                continue
                
    if not sec_counts:
        return {
            "avg_throughput_eps": 0.0,
            "peak_throughput_eps": 0.0
        }
        
    total_events = sum(sec_counts.values())
    min_t = min(sec_counts.keys())
    max_t = max(sec_counts.keys())
    duration = max(1, max_t - min_t + 1)
    
    avg_throughput = total_events / duration
    peak_throughput = max(sec_counts.values())
    
    return {
        "avg_throughput_eps": avg_throughput,
        "peak_throughput_eps": peak_throughput
    }
