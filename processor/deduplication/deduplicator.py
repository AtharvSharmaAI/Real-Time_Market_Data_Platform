# OWNER: P2
#
# PURPOSE:
# Deduplication logic.
#
# RESPONSIBILITIES:
# - Track unique event IDs
# - Handle deduplication
# - State TTL management

from datetime import datetime, timedelta
from typing import Dict

class Deduplicator:
    def __init__(self, ttl_seconds: int = 60):
        self.ttl = timedelta(seconds=ttl_seconds)
        # Store event_id -> insertion time (datetime) to manage TTL
        self.seen_events: Dict[str, datetime] = {}

    def is_duplicate(self, event_id: str) -> bool:
        """
        Check if an event_id is a duplicate. If not duplicate, record it.
        """
        self.clean_expired()
        
        if event_id in self.seen_events:
            return True
            
        self.seen_events[event_id] = datetime.now()
        return False

    def clean_expired(self):
        """
        Removes keys from the deduplication state that exceed the TTL.
        """
        now = datetime.now()
        expired_keys = [
            k for k, v in self.seen_events.items() if now - v > self.ttl
        ]
        for k in expired_keys:
            del self.seen_events[k]
