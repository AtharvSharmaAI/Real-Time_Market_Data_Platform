# Chaos Engineering Scenarios

This document explains the four required chaos scenario runner scripts used to validate platform resilience.

## Scenarios

### 1. Processor Kill & Restart
- **Script**: `chaos/experiments/processor_kill.py`
- **Action**: Terminates the stream processor process during high-load stream generation, waits for 5 seconds, and restarts it.
- **Expected Outcome**: Consumer offset checkpointing ensures processing resumes exactly from the last saved state, resulting in zero lost events.

### 2. 5x Traffic Burst
- **Script**: `chaos/experiments/traffic_burst.py`
- **Action**: Activates `TrafficBurstController` to increase transaction production rate by 5x (e.g. from 20 to 100 events/sec).
- **Expected Outcome**: System backlog grows temporarily, Prometheus throughput spikes, and the processor recovers to baseline latency after the burst terminates.

### 3. Bad Data Injection
- **Script**: `chaos/experiments/bad_data.py`
- **Action**: Injects malformed event schemas (e.g. missing prices, wrong types, incorrect strings) into the broker.
- **Expected Outcome**: Validation engine filters these payloads, increments the DLQ counter, routes bad records to the DLQ topic, and continues processing healthy records.

### 4. Late & Out-of-Order Events
- **Script**: `chaos/experiments/late_events.py` / `out_of_order.py`
- **Action**: Introduces event-time latency offset (e.g. subtracting 10-30 seconds from event timestamps) or buffers and shuffles event emission order.
- **Expected Outcome**: Watermark rules drop events that are older than the allowed lateness buffer, and out-of-order records within the watermark are successfully aligned and computed in the correct tumbling windows.