import pytest
from evaluation.anomaly.precision_recall import calculate_precision_recall
from evaluation.anomaly.f1 import calculate_f1_score
from evaluation.ground_truth.vwap_ground_truth import VWAPGroundTruth
from evaluation.ground_truth.anomaly_ground_truth import AnomalyGroundTruth
from evaluation.metrics.correctness import calculate_correctness
from evaluation.metrics.data_integrity import calculate_data_integrity
from evaluation.metrics.latency import calculate_latencies
from evaluation.metrics.recovery import calculate_recovery_metrics
from evaluation.metrics.throughput import calculate_throughput
from evaluation.resilience.resilience_score import calculate_resilience_score

def test_precision_recall_and_f1():
    predictions = [{"symbol": "AAPL", "anomaly_type": "PRICE_SPIKE", "event_id": "evt-1"}]
    ground_truth = [{"symbol": "AAPL", "anomaly_type": "PRICE_SPIKE", "event_id": "evt-1"}]
    
    precision, recall = calculate_precision_recall(predictions, ground_truth)
    assert precision == 1.0
    assert recall == 1.0
    
    f1 = calculate_f1_score(predictions, ground_truth)
    assert f1 == 1.0

def test_vwap_ground_truth():
    events = [
        {"symbol": "AAPL", "price": 100.0, "volume": 10.0, "event_time": "2026-08-31T12:00:01.000000"},
        {"symbol": "AAPL", "price": 102.0, "volume": 20.0, "event_time": "2026-08-31T12:00:02.000000"}
    ]
    gt = VWAPGroundTruth(events)
    expected = gt.calculate_expected_vwap(window_size_sec=5)
    assert "AAPL" in expected
    assert len(expected["AAPL"]) == 1
    assert abs(expected["AAPL"][0]["vwap"] - 101.33333) < 1e-4

def test_anomaly_ground_truth():
    events = [
        {"symbol": "AAPL", "price": 100.0, "volume": 10.0, "event_time": "2026-08-31T12:00:01.000000"},
        {"symbol": "AAPL", "price": 100.0, "volume": 10.0, "event_time": "2026-08-31T12:00:02.000000"},
        {"symbol": "AAPL", "price": 100.0, "volume": 10.0, "event_time": "2026-08-31T12:00:03.000000"},
        {"symbol": "AAPL", "price": 100.0, "volume": 10.0, "event_time": "2026-08-31T12:00:04.000000"},
        {"symbol": "AAPL", "price": 100.0, "volume": 10.0, "event_time": "2026-08-31T12:00:05.000000"},
        {"symbol": "AAPL", "price": 800.0, "volume": 10.0, "event_time": "2026-08-31T12:00:06.000000"}
    ]
    gt = AnomalyGroundTruth(events)
    anoms = gt.generate_expected_anomalies(threshold_factor=2.0)
    assert len(anoms) > 0
    assert anoms[0]["anomaly_type"] == "PRICE_SPIKE"

def test_resilience_score():
    score = calculate_resilience_score(correctness_score=0.9, recovery_score=0.8, integrity_score=0.95)
    assert score == 0.885
