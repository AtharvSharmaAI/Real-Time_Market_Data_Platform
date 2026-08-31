// OWNER: P3
//
// PURPOSE:
// API service client.

const API_BASE_URL = "/api";

export async function fetchHealth() {
  try {
    const res = await fetch(`${API_BASE_URL}/health`);
    if (!res.ok) throw new Error("Health check failed");
    return await res.json();
  } catch (err) {
    return { status: "OK", mode: "simulation" };
  }
}

export async function fetchTrades() {
  try {
    const res = await fetch(`${API_BASE_URL}/trades`);
    if (!res.ok) throw new Error("Fetch trades failed");
    return await res.json();
  } catch (err) {
    // Return mock data for simulation mode
    return [
      { event_id: "evt-001", symbol: "AAPL", price: 175.25, volume: 150, exchange: "NASDAQ", side: "BUY", event_time: new Date().toISOString() },
      { event_id: "evt-002", symbol: "MSFT", price: 420.50, volume: 300, exchange: "NYSE", side: "SELL", event_time: new Date().toISOString() },
      { event_id: "evt-003", symbol: "GOOGL", price: 150.10, volume: 200, exchange: "NASDAQ", side: "BUY", event_time: new Date().toISOString() },
      { event_id: "evt-004", symbol: "AMZN", price: 178.90, volume: 100, exchange: "NYSE", side: "BUY", event_time: new Date().toISOString() }
    ];
  }
}

export async function fetchVWAP() {
  try {
    const res = await fetch(`${API_BASE_URL}/vwap`);
    if (!res.ok) throw new Error("Fetch VWAP failed");
    return await res.json();
  } catch (err) {
    // Return mock VWAP statistics
    return [
      { symbol: "AAPL", vwap: 175.45, volume: 24500, window_start: "14:00:00", window_end: "14:00:05" },
      { symbol: "MSFT", vwap: 421.10, volume: 45000, window_start: "14:00:00", window_end: "14:00:05" },
      { symbol: "GOOGL", vwap: 150.05, volume: 12000, window_start: "14:00:00", window_end: "14:00:05" },
      { symbol: "AMZN", vwap: 178.60, volume: 18500, window_start: "14:00:00", window_end: "14:00:05" }
    ];
  }
}

export async function fetchAnomalies() {
  try {
    const res = await fetch(`${API_BASE_URL}/anomalies`);
    if (!res.ok) throw new Error("Fetch anomalies failed");
    return await res.json();
  } catch (err) {
    return [
      { symbol: "AAPL", anomaly_type: "PRICE_SPIKE", anomaly_score: 4.25, processed_at: new Date().toISOString() },
      { symbol: "MSFT", anomaly_type: "VOLUME_SPIKE", anomaly_score: 3.80, processed_at: new Date().toISOString() }
    ];
  }
}
