# OWNER: P2
#
# PURPOSE:
# Price volatility calculation.
#
# RESPONSIBILITIES:
# - Calculate standard deviation of prices in a window

import math
from typing import List, Dict, Any

def calculate_volatility(trades: List[Dict[str, Any]]) -> float:
    """
    Calculate the price volatility (standard deviation) for a list of trades in a window.
    """
    if len(trades) < 2:
        return 0.0
        
    prices = [t.get("price", 0.0) for t in trades]
    mean_price = sum(prices) / len(prices)
    
    variance = sum((p - mean_price) ** 2 for p in prices) / (len(prices) - 1)
    return round(math.sqrt(variance), 4)
