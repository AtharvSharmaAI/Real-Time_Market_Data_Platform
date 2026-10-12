# OWNER: P2
#
# PURPOSE:
# Track historical metrics statistics.
#
# RESPONSIBILITIES:
# - Track moving average/std dev for Z-score anomaly detection

import math
from typing import Dict, List

MIN_SAMPLES = 5

class MetricStatsTracker:
    def __init__(self, window_limit: int = 50):
        self.limit = window_limit
        # symbol -> list of historical values
        self.history: Dict[str, List[float]] = {}

    def add_value(self, symbol: str, val: float):
        if symbol not in self.history:
            self.history[symbol] = []
        self.history[symbol].append(val)
        if len(self.history[symbol]) > self.limit:
            self.history[symbol].pop(0)

    def get_stats(self, symbol: str) -> tuple:
        """
        Return (mean, std_dev) for a symbol.
        """
        vals = self.history.get(symbol, [])
        if len(vals) < MIN_SAMPLES:  # z-score on fewer points is noise
            return 0.0, 0.0
            
        mean = sum(vals) / len(vals)
        variance = sum((x - mean) ** 2 for x in vals) / (len(vals) - 1)
        std_dev = math.sqrt(variance)
        return mean, std_dev
