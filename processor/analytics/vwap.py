# OWNER: P2
#
# PURPOSE:
# VWAP calculation logic.
#
# RESPONSIBILITIES:
# - Calculate VWAP for a given set of trades.
# - Validate price and volume inputs to avoid division by zero or invalid calculations.

from typing import List, Dict, Any

def calculate_vwap(trades: List[Dict[str, Any]]) -> float:
    """
    Calculate the Volume Weighted Average Price (VWAP) for a list of trades.
    Formula: Sum(Price * Volume) / Sum(Volume)
    """
    if not trades:
        return 0.0
        
    total_value = 0.0
    total_volume = 0.0
    
    for trade in trades:
        price = trade.get("price", 0.0)
        volume = trade.get("volume", 0.0)
        
        # Guard rails for invalid inputs
        if price < 0 or volume <= 0:
            continue
            
        total_value += price * volume
        total_volume += volume
        
    if total_volume == 0.0:
        return 0.0
        
    return round(total_value / total_volume, 4)
