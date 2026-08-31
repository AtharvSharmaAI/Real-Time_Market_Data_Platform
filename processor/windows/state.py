# OWNER: P2
#
# PURPOSE:
# Manage state for window aggregates.
#
# RESPONSIBILITIES:
# - Maintain in-memory state of active windows
# - Handle TTL/purge for closed windows

from datetime import datetime
from typing import Dict, List, Any

class WindowStateStore:
    def __init__(self):
        # Store window key -> list of events/trades
        # Key is (symbol, window_start, window_end)
        self.active_windows: Dict[tuple, List[Dict[str, Any]]] = {}

    def add_to_window(self, symbol: str, window_start: datetime, window_end: datetime, event: Dict[str, Any]):
        """
        Add event to the appropriate window state.
        """
        key = (symbol, window_start, window_end)
        if key not in self.active_windows:
            self.active_windows[key] = []
        self.active_windows[key].append(event)

    def get_events(self, symbol: str, window_start: datetime, window_end: datetime) -> List[Dict[str, Any]]:
        """
        Retrieve events for a window.
        """
        key = (symbol, window_start, window_end)
        return self.active_windows.get(key, [])

    def purge_window(self, symbol: str, window_start: datetime, window_end: datetime):
        """
        Remove window from active state (finalized/closed).
        """
        key = (symbol, window_start, window_end)
        if key in self.active_windows:
            del self.active_windows[key]
