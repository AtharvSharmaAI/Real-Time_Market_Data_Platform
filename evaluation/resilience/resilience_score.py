# OWNER: P4
#
# PURPOSE:
# Resilience Score Calculation.

from typing import Dict, Any

def calculate_resilience_score(
    correctness_score: float,
    recovery_score: float,
    integrity_score: float
) -> float:
    """
    Resilience = 0.40 * Correctness + 0.30 * Recovery + 0.30 * Data Integrity
    Values must be between 0.0 and 1.0.
    """
    c = max(0.0, min(1.0, correctness_score))
    r = max(0.0, min(1.0, recovery_score))
    i = max(0.0, min(1.0, integrity_score))
    
    score = 0.40 * c + 0.30 * r + 0.30 * i
    return round(score, 4)
