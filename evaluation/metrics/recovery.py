# OWNER: P4
#
# PURPOSE:
# Recovery metrics.

from typing import List, Dict, Any
from datetime import datetime

def calculate_recovery_metrics(
    failure_timestamp: str,
    recovery_start_timestamp: str,
    backlog_cleared_timestamp: str
) -> Dict[str, Any]:
    """
    Measure:
    - downtime (from failure_timestamp to recovery_start_timestamp)
    - backlog recovery duration (from recovery_start_timestamp to backlog_cleared_timestamp)
    - total recovery time (from failure_timestamp to backlog_cleared_timestamp)
    """
    try:
        fail_t = datetime.fromisoformat(failure_timestamp.replace("Z", "+00:00"))
        rec_start_t = datetime.fromisoformat(recovery_start_timestamp.replace("Z", "+00:00"))
        cleared_t = datetime.fromisoformat(backlog_cleared_timestamp.replace("Z", "+00:00"))
        
        downtime = (rec_start_t - fail_t).total_seconds()
        backlog_duration = (cleared_t - rec_start_t).total_seconds()
        total_recovery = (cleared_t - fail_t).total_seconds()
    except Exception:
        downtime = 0.0
        backlog_duration = 0.0
        total_recovery = 0.0
        
    return {
        "downtime_seconds": downtime,
        "backlog_clear_time_seconds": backlog_duration,
        "total_recovery_seconds": total_recovery
    }
