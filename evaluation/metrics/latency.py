# OWNER: P4
#
# PURPOSE:
# Latency metrics.

from typing import List, Dict, Any
from datetime import datetime

def calculate_latencies(
    processed_events: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """
    Measure:
    - event-to-result latency (time difference between ingestion/event_time and storage time)
    - window completion latency (time between window end and window storage)
    """
    latencies = []
    
    for ev in processed_events:
        evt_time_str = ev.get("event_time")
        proc_time_str = ev.get("processed_at") or ev.get("processing_time")
        
        if evt_time_str and proc_time_str:
            try:
                evt_t = datetime.fromisoformat(evt_time_str.replace("Z", "+00:00"))
                proc_t = datetime.fromisoformat(proc_time_str.replace("Z", "+00:00"))
                diff = (proc_t - evt_t).total_seconds()
                latencies.append(diff)
            except Exception:
                continue
                
    if not latencies:
        return {
            "mean_latency_sec": 0.0,
            "p95_latency_sec": 0.0,
            "p99_latency_sec": 0.0
        }
        
    latencies.sort()
    n = len(latencies)
    mean_val = sum(latencies) / n
    p95_val = latencies[int(n * 0.95)] if n > 0 else 0.0
    p99_val = latencies[int(n * 0.99)] if n > 0 else 0.0
    
    return {
        "mean_latency_sec": mean_val,
        "p95_latency_sec": p95_val,
        "p99_latency_sec": p99_val
    }
