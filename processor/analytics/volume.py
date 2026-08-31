# OWNER: P2
#
# PURPOSE:
# Volume calculation.
#
# RESPONSIBILITIES:
# - Sum total volume of trades in a window

from typing import List, Dict, Any

def calculate_total_volume(trades: List[Dict[str, Any]]) -> float:
    """
    Calculate the total volume for a list of trades in a window.
    """
    return round(sum(t.get("volume", 0.0) for t in trades), 4)
