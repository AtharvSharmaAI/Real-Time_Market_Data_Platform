# OWNER: P2
#
# PURPOSE:
# Anomaly detection rules.
#
# RESPONSIBILITIES:
# - Trigger anomalies based on thresholds (Z-score, hard bounds)

from typing import Tuple

def evaluate_zscore_anomaly(val: float, mean: float, std_dev: float, threshold: float = 3.0) -> Tuple[bool, float]:
    """
    Check if a value constitutes an anomaly based on running Z-score.
    """
    if std_dev == 0.0:
        return False, 0.0
        
    z_score = abs(val - mean) / std_dev
    return z_score > threshold, round(z_score, 2)
