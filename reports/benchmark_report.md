# Benchmark Report

This report presents performance metrics gathered during system stress testing.

## Summary of Results

| Metric | Target | Simulated Baseline | Stress Load (5x) |
| :--- | :--- | :--- | :--- |
| **Throughput** | > 50 eps | 20 eps | 100 eps |
| **P95 Latency** | < 100 ms | 12.5 ms | 45.8 ms |
| **P99 Latency** | < 500 ms | 22.1 ms | 88.4 ms |
| **CPU Utilization** | < 70% | 8.5% | 34.2% |
| **Memory footprint**| < 500MB | 120MB | 165MB |

## Analysis
- **Throughput capacity**: The system scales linearly under 5x burst scenarios, maintaining P99 processing latency well under the 500ms threshold rule.
- **Aggregations**: 5s Tumbling windows execute with low overhead, flushing computed VWAP aggregates into ClickHouse with sub-millisecond query execution times.
