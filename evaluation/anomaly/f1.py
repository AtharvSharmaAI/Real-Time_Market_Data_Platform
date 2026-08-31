# OWNER: P4
#
# PURPOSE:
# Anomaly F1 Score.

from evaluation.anomaly.precision_recall import calculate_precision_recall
from typing import List, Dict, Any

def calculate_f1_score(
    predictions: List[Dict[str, Any]], 
    ground_truth: List[Dict[str, Any]]
) -> float:
    """
    Calculate F1 Score.
    F1 = 2 * (Precision * Recall) / (Precision + Recall)
    """
    precision, recall = calculate_precision_recall(predictions, ground_truth)
    if (precision + recall) == 0.0:
        return 0.0
    return 2.0 * (precision * recall) / (precision + recall)
