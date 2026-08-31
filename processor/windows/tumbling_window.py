# OWNER: P2
#
# PURPOSE:
# Tumbling window assignment.
#
# RESPONSIBILITIES:
# - Assign events to 5-second windows
# - Return window boundaries (start/end)

from datetime import datetime, timedelta
from typing import Tuple

class TumblingWindowAssigner:
    def __init__(self, size_seconds: int = 5):
        self.size = size_seconds

    def assign(self, event_time: datetime) -> Tuple[datetime, datetime]:
        """
        Assigns event_time to a tumbling window, returning (window_start, window_end).
        """
        # Round seconds down to nearest interval
        # Ex: if event_time is 14:00:03, size is 5, window_start is 14:00:00, window_end is 14:00:05
        second_offset = event_time.second % self.size
        window_start = event_time.replace(second=event_time.second - second_offset, microsecond=0)
        window_end = window_start + timedelta(seconds=self.size)
        return window_start, window_end
