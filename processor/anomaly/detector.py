# OWNER: P2
#
# PURPOSE:
# Anomaly detection runner.
#
# RESPONSIBILITIES:
# - Run anomaly checks against window aggregates
# - Classify anomalies

from typing import Tuple
from processor.anomaly.statistics import MetricStatsTracker
from processor.anomaly.rules import evaluate_zscore_anomaly

class AnomalyDetector:
    def __init__(self, threshold: float = 3.0):
        self.threshold = threshold
        self.vwap_tracker = MetricStatsTracker()
        self.volume_tracker = MetricStatsTracker()
        self.volatility_tracker = MetricStatsTracker()

    def detect(self, symbol: str, vwap: float, volume: float, volatility: float) -> Tuple[bool, str, float]:
        """
        Run Z-score checks on vwap, volume, and volatility.
        Returns (anomaly_flag, anomaly_type, anomaly_score).
        """
        # Get historical statistics
        vwap_mean, vwap_std = self.vwap_tracker.get_stats(symbol)
        vol_mean, vol_std = self.volume_tracker.get_stats(symbol)
        vola_mean, vola_std = self.volatility_tracker.get_stats(symbol)

        # Run evaluations
        vwap_anomaly, vwap_z = evaluate_zscore_anomaly(vwap, vwap_mean, vwap_std, self.threshold)
        vol_anomaly, vol_z = evaluate_zscore_anomaly(volume, vol_mean, vol_std, self.threshold)
        vola_anomaly, vola_z = evaluate_zscore_anomaly(volatility, vola_mean, vola_std, self.threshold)

        # Add values to history for next time
        self.vwap_tracker.add_value(symbol, vwap)
        self.volume_tracker.add_value(symbol, volume)
        self.volatility_tracker.add_value(symbol, volatility)

        # Determine highest severity anomaly
        if vwap_anomaly:
            return True, "PRICE_SPIKE", vwap_z
        if vol_anomaly:
            return True, "VOLUME_SPIKE", vol_z
        if vola_anomaly:
            return True, "VOLATILITY_SPIKE", vola_z

        return False, "NONE", 0.0
