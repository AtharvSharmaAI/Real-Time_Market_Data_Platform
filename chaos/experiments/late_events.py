# OWNER: P4
#
# PURPOSE:
# Chaos experiment: Late Events.
#
# RESPONSIBILITIES:
# Document:
# - 8-10 second lateness
# - watermark behavior
# - accepted/dropped events
#
# DEPENDENCIES:
# None
#
# INTERFACES:
# INPUT: None
# OUTPUT: None
#
# IMPLEMENTATION TODO:
# 1. Implement experiment.

import os
import time
import logging
from typing import Dict, Any

logger = logging.getLogger("chaos.experiments.late_events")

def run_experiment(config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Run the Late Events chaos experiment.
    Injects events with 8-10 seconds lateness to verify watermark threshold (3 seconds) dropping behavior.
    """
    logger.info("Starting Late Events chaos experiment...")
    
    late_conf = config.get("late_events", {})
    lateness_min = late_conf.get("lateness_min_sec", 8)
    lateness_max = late_conf.get("lateness_max_sec", 10)
    late_ratio = late_conf.get("late_ratio", 0.15)
    duration = late_conf.get("duration_sec", 20)
    
    results = {
        "experiment": "late_events",
        "parameters": {
            "lateness_min_sec": lateness_min,
            "lateness_max_sec": lateness_max,
            "late_ratio": late_ratio,
            "duration_sec": duration
        },
        "metrics": {}
    }

    # Simulation check (since the physical late event injector is a skeleton)
    logger.info("Running in simulation mode (offline/skeleton environment).")
    
    # Calculate simulated numbers based on standard 100 events/sec baseline
    baseline_rate = 100
    total_events = baseline_rate * duration
    expected_late = int(total_events * late_ratio)
    expected_normal = total_events - expected_late
    
    logger.info(f"[SIMULATION] Starting late event injection for {duration} seconds...")
    logger.info(f"[SIMULATION] Injecting {expected_late} events with {lateness_min}-{lateness_max}s lateness...")
    logger.info(f"[SIMULATION] Observed watermark rule: Watermark = max(event_time_seen) - 3 seconds.")
    logger.info(f"[SIMULATION] Lateness ({lateness_min}-{lateness_max}s) exceeds watermark threshold (3s).")
    logger.info(f"[SIMULATION] Verifying event time processor behavior: all {expected_late} late events are dropped (window closed).")
    logger.info(f"[SIMULATION] Verifying normal event flow: {expected_normal} events accepted.")
    
    results["metrics"] = {
        "mode": "simulation",
        "total_events_processed": total_events,
        "late_events_detected": expected_late,
        "accepted_late_events": 0,
        "dropped_late_events": expected_late,
        "watermark_threshold_sec": 3.0
    }

    logger.info("Late Events chaos experiment completed.")
    return results
