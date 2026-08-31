# OWNER: P2
#
# PURPOSE:
# Late event categorization and handling.
#
# RESPONSIBILITIES:
# - Detect late events based on watermark
# - Categorize late events (dropped vs accepted)

from datetime import datetime
from processor.event_time.watermark import WatermarkTracker

class LateEventHandler:
    def __init__(self, tracker: WatermarkTracker):
        self.tracker = tracker

    def is_late(self, event_time: datetime) -> bool:
        """
        Check if an event_time is behind the current watermark.
        """
        watermark = self.tracker.get_watermark()
        return event_time < watermark
