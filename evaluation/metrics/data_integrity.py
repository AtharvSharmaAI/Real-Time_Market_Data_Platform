# OWNER: P4
#
# PURPOSE:
# Data Integrity metrics.

from typing import List, Dict, Any

def calculate_data_integrity(
    sent_events: List[Dict[str, Any]],
    processed_events: List[Dict[str, Any]],
    dlq_events: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """
    Measure:
    - duplicates processed
    - lost events
    - DLQ rate
    - data integrity ratio
    """
    sent_ids = {e["event_id"] for e in sent_events if "event_id" in e}
    processed_ids = [e["event_id"] for e in processed_events if "event_id" in e]
    dlq_ids = {e["event_id"] for e in dlq_events if "event_id" in e}
    
    unique_processed_ids = set(processed_ids)
    
    # Calculate duplicates
    total_duplicates = len(processed_ids) - len(unique_processed_ids)
    
    # Calculate lost events (sent but never processed nor went to DLQ)
    lost_ids = sent_ids - unique_processed_ids - dlq_ids
    total_lost = len(lost_ids)
    
    total_sent = len(sent_ids)
    integrity_ratio = 1.0
    if total_sent > 0:
        # Lost events subtract directly from integrity
        integrity_ratio = max(0.0, 1.0 - (total_lost / total_sent))
        
    return {
        "sent_count": total_sent,
        "unique_processed_count": len(unique_processed_ids),
        "duplicate_count": total_duplicates,
        "dlq_count": len(dlq_ids),
        "lost_count": total_lost,
        "integrity_ratio": integrity_ratio
    }
