import React, { useState, useEffect } from 'react';
import { fetchHealth, fetchTrades, fetchVWAP, fetchAnomalies } from '../services/api';
import SystemStatus from '../components/SystemStatus';
import MarketChart from '../components/MarketChart';
import VWAPPanel from '../components/VWAPPanel';
import AnomalyPanel from '../components/AnomalyPanel';

export default function Dashboard() {
  const [health, setHealth] = useState({ status: "OK" });
  const [trades, setTrades] = useState([]);
  const [vwap, setVwap] = useState([]);
  const [anoms, setAnoms] = useState([]);
  const [systemMetrics, setSystemMetrics] = useState({
    throughput: 154.2,
    latency: 18.5,
    dlq_rate: 0.1,
    anomaly_rate: 1.4
  });

  useEffect(() => {
    const loadData = async () => {
      try {
        const h = await fetchHealth();
        setHealth(h);

        const t = await fetchTrades();
        setTrades(t);

        const v = await fetchVWAP();
        setVwap(v);

        const a = await fetchAnomalies();
        setAnoms(a);

        // Compute simulated dynamic metrics if backend is mock
        if (h.mode === "simulation") {
          setSystemMetrics({
            throughput: parseFloat((120 + Math.random() * 40).toFixed(1)),
            latency: parseFloat((12 + Math.random() * 8).toFixed(1)),
            dlq_rate: parseFloat((Math.random() < 0.1 ? 0.2 : 0.0).toFixed(1)),
            anomaly_rate: parseFloat((0.8 + Math.random() * 1.5).toFixed(1))
          });
        }
      } catch (err) {
        console.error(err);
      }
    };

    loadData();
    const interval = setInterval(loadData, 2000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div style={{
      padding: '40px 24px',
      maxWidth: '1440px',
      margin: '0 auto',
      minHeight: '100vh',
      backgroundColor: '#0F172A',
      color: '#F8FAFC',
      fontFamily: 'system-ui, -apple-system, sans-serif'
    }}>
      {/* Top Header */}
      <header style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '40px', borderBottom: '1px solid rgba(255, 255, 255, 0.05)', paddingBottom: '20px' }}>
        <div>
          <h1 style={{ fontSize: '2.5rem', fontWeight: 800, margin: 0, background: 'linear-gradient(135deg, #38BDF8, #A78BFA)', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent', letterSpacing: '-0.03em' }}>
            MarketFlow Dashboard
          </h1>
          <p style={{ color: '#64748B', marginTop: '6px', fontSize: '1rem', fontWeight: 500 }}>
            Real-time event processing, windowing, and anomaly pipeline analytics.
          </p>
        </div>
      </header>

      {/* Grid Layout */}
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 2fr', gap: '32px', marginBottom: '32px' }}>
        <div style={{ display: 'flex', flexDirection: 'column', gap: '32px' }}>
          <SystemStatus health={health} metrics={systemMetrics} />
          <AnomalyPanel anomalies={anoms} />
        </div>
        <div style={{ display: 'flex', flexDirection: 'column', gap: '32px' }}>
          <MarketChart trades={trades} />
          <VWAPPanel vwapData={vwap} />
        </div>
      </div>
    </div>
  );
}
