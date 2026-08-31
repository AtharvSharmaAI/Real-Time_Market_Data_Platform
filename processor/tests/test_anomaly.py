# OWNER: P2
#
# PURPOSE:
# Test anomaly detection.

from processor.anomaly.detector import AnomalyDetector

def test_z_score_calculation_and_rule_trigger():
    detector = AnomalyDetector(threshold=2.0)
    symbol = "AAPL"
    
    # Send varying baseline trades so std_dev > 0
    baselines = [100.0, 101.0, 99.0, 100.0, 101.0, 99.0, 100.0, 101.0, 99.0, 100.0]
    for val in baselines:
        flag, a_type, score = detector.detect(symbol, val, 100.0, 1.0)
        assert flag is False
        assert a_type == "NONE"
        assert score == 0.0

    # Spiking price (vwap) should trigger anomaly (mean ~100, std_dev ~0.8)
    # 150.0 is around 60 standard deviations away, so it should trigger
    flag, a_type, score = detector.detect(symbol, 150.0, 100.0, 1.0)
    assert flag is True
    assert a_type == "PRICE_SPIKE"
    assert score > 2.0
