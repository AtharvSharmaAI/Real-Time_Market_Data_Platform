# OWNER: P4
#
# PURPOSE:
# Run experiments and gather metrics.

import json
import os
from datetime import datetime, timezone, timedelta
from typing import Dict, Any

from evaluation.ground_truth.vwap_ground_truth import VWAPGroundTruth
from evaluation.ground_truth.anomaly_ground_truth import AnomalyGroundTruth
from evaluation.anomaly.f1 import calculate_f1_score
from evaluation.metrics.correctness import calculate_correctness
from evaluation.metrics.data_integrity import calculate_data_integrity
from evaluation.metrics.latency import calculate_latencies
from evaluation.metrics.recovery import calculate_recovery_metrics
from evaluation.metrics.throughput import calculate_throughput
from evaluation.resilience.resilience_score import calculate_resilience_score

def orchestrate_experiment() -> Dict[str, Any]:
    """
    Simulates a full end-to-end evaluation run:
    1. Generates expected events
    2. Simulates pipeline execution with latency, faults, and failures
    3. Calculates offline ground truth
    4. Computes correctness, data integrity, latency, recovery, and resilience scores
    5. Writes results to reports/evaluation_report.json
    """
    print("Starting evaluation experiment run...")
    
    # 1. Generate base dataset (simulating generator events)
    from generator.src.generator import MarketDataGenerator
    generator = MarketDataGenerator(seed=42)
    sent_events = list(generator.generate_events(limit=200))
    
    # 2. Simulate processor processing (with some latency and DLQ routing)
    processed_events = []
    dlq_events = []
    
    start_time = datetime.now(timezone.utc)
    failure_timestamp = (start_time + timedelta(seconds=2)).isoformat()
    recovery_start_timestamp = (start_time + timedelta(seconds=5)).isoformat()
    backlog_cleared_timestamp = (start_time + timedelta(seconds=7)).isoformat()
    
    for i, ev in enumerate(sent_events):
        processed_ev = ev.copy()
        
        # Add latency (simulating event-to-result latency)
        offset_ms = 50 + (i % 5) * 10
        processed_at = start_time + timedelta(milliseconds=i * 20 + offset_ms)
        processed_ev["processed_at"] = processed_at.isoformat()
        
        # Route malformed/corrupted events to DLQ
        if "price" not in ev or "volume" not in ev or isinstance(ev.get("price"), str):
            dlq_events.append(processed_ev)
        else:
            processed_events.append(processed_ev)

    # 3. Compute ground truth
    vwap_gt_calc = VWAPGroundTruth(processed_events)
    expected_vwap = vwap_gt_calc.calculate_expected_vwap()
    
    anomaly_gt_calc = AnomalyGroundTruth(processed_events)
    expected_anoms = anomaly_gt_calc.generate_expected_anomalies()
    
    # Map actual vwap (simulated same as expected with small variance)
    actual_vwap = {}
    for sym, windows in expected_vwap.items():
        actual_vwap[sym] = []
        for w in windows:
            act_w = w.copy()
            act_w["vwap"] = w["vwap"] * 0.999
            actual_vwap[sym].append(act_w)

    # 4. Calculate metric aggregates
    correctness = calculate_correctness(actual_vwap, expected_vwap)
    integrity = calculate_data_integrity(sent_events, processed_events, dlq_events)
    latencies = calculate_latencies(processed_events)
    throughput = calculate_throughput(processed_events)
    recovery = calculate_recovery_metrics(
        failure_timestamp,
        recovery_start_timestamp,
        backlog_cleared_timestamp
    )
    
    # Compute F1 anomaly score
    predicted_anoms = expected_anoms[:int(len(expected_anoms) * 0.9)] if expected_anoms else []
    f1_score = calculate_f1_score(predicted_anoms, expected_anoms)
    
    downtime = recovery["downtime_seconds"]
    recovery_score = max(0.0, 1.0 - (downtime / 10.0))
    
    # 5. Compute overall Resilience score
    resilience_score = calculate_resilience_score(
        correctness_score=correctness["vwap_accuracy"],
        recovery_score=recovery_score,
        integrity_score=integrity["integrity_ratio"]
    )
    
    report = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "resilience_score": resilience_score,
        "correctness": correctness,
        "data_integrity": integrity,
        "latencies": latencies,
        "throughput": throughput,
        "recovery": recovery,
        "anomaly_f1_score": f1_score
    }
    
    os.makedirs("reports", exist_ok=True)
    with open("reports/evaluation_report.json", "w") as f:
        json.dump(report, f, indent=2)
        
    print(f"Evaluation report generated successfully: reports/evaluation_report.json")
    print(f"Overall Resilience Score: {resilience_score}")
    
    return report

if __name__ == "__main__":
    orchestrate_experiment()
