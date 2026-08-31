# OWNER: P4
#
# PURPOSE:
# Anomaly Precision and Recall.

from typing import List, Dict, Any, Tuple

def calculate_precision_recall(
    predictions: List[Dict[str, Any]], 
    ground_truth: List[Dict[str, Any]]
) -> Tuple[float, float]:
    """
    Calculate Precision and Recall.
    Precision = TP / (TP + FP)
    Recall = TP / (TP + FN)
    """
    pred_set = set()
    for p in predictions:
        pred_set.add((p.get("symbol"), p.get("anomaly_type"), p.get("event_id")))
        
    gt_set = set()
    for gt in ground_truth:
        gt_set.add((gt.get("symbol"), gt.get("anomaly_type"), gt.get("event_id")))
        
    if not pred_set and not gt_set:
        return 1.0, 1.0
        
    tp = len(pred_set.intersection(gt_set))
    fp = len(pred_set - gt_set)
    fn = len(gt_set - pred_set)
    
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    
    return precision, recall
