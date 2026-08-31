# OWNER: P4
#
# PURPOSE:
# Correctness metrics.

from typing import List, Dict, Any

def calculate_correctness(
    actual_vwap: Dict[str, List[Dict[str, Any]]],
    expected_vwap: Dict[str, List[Dict[str, Any]]],
    tolerance: float = 1e-4
) -> Dict[str, Any]:
    """
    Calculate correctness score based on:
    - Average Absolute Percentage Error (APE) on VWAP
    - Proportion of expected windows matching actual windows
    """
    total_expected = 0
    matched = 0
    errors = []
    
    for symbol, expected_windows in expected_vwap.items():
        actual_windows = actual_vwap.get(symbol, [])
        # Map actual window bounds to their VWAP value
        actual_map = {
            (w["window_start"], w["window_end"]): w["vwap"]
            for w in actual_windows
        }
        
        for exp_w in expected_windows:
            total_expected += 1
            key = (exp_w["window_start"], exp_w["window_end"])
            
            if key in actual_map:
                act_vwap = actual_map[key]
                exp_vwap = exp_w["vwap"]
                matched += 1
                
                # Percent error
                if exp_vwap > 0:
                    err = abs(act_vwap - exp_vwap) / exp_vwap
                    errors.append(err)
                else:
                    if abs(act_vwap) < tolerance:
                        errors.append(0.0)
                    else:
                        errors.append(1.0) # Maximum error
            else:
                # Missing window
                errors.append(1.0)
                
    avg_error = sum(errors) / len(errors) if errors else 0.0
    accuracy_score = max(0.0, 1.0 - avg_error)
    
    return {
        "vwap_accuracy": accuracy_score,
        "missing_windows": total_expected - matched,
        "total_windows": total_expected,
        "correctness_ratio": matched / total_expected if total_expected > 0 else 1.0
      }
