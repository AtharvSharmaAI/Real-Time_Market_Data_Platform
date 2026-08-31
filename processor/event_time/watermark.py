# OWNER: P2
#
# PURPOSE:
# Watermark tracker.
#
# RESPONSIBILITIES:
# - Track max event time seen
# - Maintain watermark threshold

from datetime import datetime, timedelta

class WatermarkTracker:
    def __init__(self, delay_seconds: int = 3):
        self.delay = timedelta(seconds=delay_seconds)
        self.max_event_time: datetime = None

    def update(self, event_time: datetime) -> datetime:
        """
        Update maximum event time seen and return the new watermark datetime.
        """
        if self.max_event_time is None or event_time > self.max_event_time:
            self.max_event_time = event_time
            
        return self.get_watermark()

    def get_watermark(self) -> datetime:
        """
        Retrieve current watermark.
        """
        if self.max_event_time is None:
            return datetime.min
        return self.max_event_time - self.delay
