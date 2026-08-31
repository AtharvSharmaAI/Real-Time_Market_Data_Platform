import React, { useState, useEffect } from 'react';
import { fetchAnomalies } from '../services/api';
import AnomalyPanel from '../components/AnomalyPanel';

export default function Anomalies() {
  const [anoms, setAnoms] = useState([]);
  const [error, setError] = useState(null);

  useEffect(() => {
    const load = async () => {
      try {
        const data = await fetchAnomalies();
        setAnoms(data);
      } catch (err) {
        setError(err.message);
      }
    };
    load();
    const timer = setInterval(load, 3000);
    return () => clearInterval(timer);
  }, []);

  return (
    <div style={{
      padding: '40px 20px',
      maxWidth: '1200px',
      margin: '0 auto',
      minHeight: '100vh',
      backgroundColor: '#0F172A',
      color: '#F8FAFC',
      fontFamily: 'system-ui, -apple-system, sans-serif'
    }}>
      <div style={{ marginBottom: '32px' }}>
        <h1 style={{ fontSize: '2.25rem', fontWeight: 800, margin: 0, background: 'linear-gradient(135deg, #F43F5E, #F59E0B)', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent' }}>
          Anomaly Center
        </h1>
        <p style={{ color: '#94A3B8', marginTop: '8px', fontSize: '1rem' }}>
          Real-time volatility tracking and statistical outlier monitoring.
        </p>
      </div>

      {error && (
        <div style={{ padding: '16px', backgroundColor: 'rgba(239, 68, 68, 0.1)', border: '1px solid rgba(239, 68, 68, 0.2)', color: '#EF4444', borderRadius: '8px', marginBottom: '24px' }}>
          Error loading anomalies: {error}
        </div>
      )}

      <div style={{ display: 'grid', gridTemplateColumns: '1fr', gap: '24px' }}>
        <AnomalyPanel anomalies={anoms} />
      </div>
    </div>
  );
}
