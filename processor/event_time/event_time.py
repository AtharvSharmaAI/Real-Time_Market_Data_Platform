# OWNER: P2
#
# PURPOSE:
# Event time parsing helper.
#
# RESPONSIBILITIES:
# Extract event time from payload and parse to datetime.

from datetime import datetime
from typing import Union

def parse_event_time(event_time_input: Union[str, datetime]) -> datetime:
    """
    Standardize the event time into a datetime object.
    Supports ISO formats.
    """
    if isinstance(event_time_input, datetime):
        return event_time_input
    if isinstance(event_time_input, str):
        # Handle Zulu suffix and standard formatting
        iso_str = event_time_input.replace("Z", "+00:00")
        try:
            return datetime.fromisoformat(iso_str)
        except ValueError:
            # Fallback for millisecond/microsecond variations
            for fmt in ("%Y-%m-%dT%H:%M:%S.%f", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%d %H:%M:%S"):
                try:
                    return datetime.strptime(event_time_input, fmt)
                except ValueError:
                    continue
            raise ValueError(f"Unable to parse event_time: {event_time_input}")
            
    raise TypeError(f"Invalid type for event_time: {type(event_time_input)}")
