import React from 'react';

export default function AnomalyPanel({ anomalies = [] }) {
  return (
    <div style={{
      background: 'rgba(30, 41, 59, 0.6)',
      backdropFilter: 'blur(12px)',
      border: '1px solid rgba(255, 255, 255, 0.08)',
      borderRadius: '16px',
      padding: '24px',
      color: '#F8FAFC',
      boxShadow: '0 8px 32px 0 rgba(0, 0, 0, 0.3)',
      width: '100%',
      fontFamily: 'system-ui, -apple-system, sans-serif'
    }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
        <h2 style={{ fontSize: '1.25rem', fontWeight: 600, margin: 0, letterSpacing: '-0.025em' }}>Real-Time Anomaly Detections</h2>
        <span style={{
          backgroundColor: anomalies.length > 0 ? 'rgba(239, 68, 68, 0.15)' : 'rgba(16, 185, 129, 0.15)',
          color: anomalies.length > 0 ? '#F87171' : '#34D399',
          padding: '4px 10px',
          borderRadius: '20px',
          fontSize: '0.75rem',
          fontWeight: 700
        }}>
          {anomalies.length} Detected
        </span>
      </div>

      <div style={{ display: 'flex', flexDirection: 'column', gap: '12px', maxHeight: '350px', overflowY: 'auto' }}>
        {anomalies.map((anom, idx) => {
          const isHighAlert = anom.anomaly_score > 3.0;
          return (
            <div key={idx} style={{
              padding: '16px',
              backgroundColor: 'rgba(15, 23, 42, 0.3)',
              borderRadius: '12px',
              borderLeft: `4px solid ${isHighAlert ? '#EF4444' : '#F59E0B'}`,
              display: 'flex',
              justifyContent: 'space-between',
              alignItems: 'center'
            }}>
              <div>
                <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                  <span style={{ fontWeight: 700, fontSize: '1rem', color: '#38BDF8' }}>{anom.symbol}</span>
                  <span style={{
                    backgroundColor: isHighAlert ? 'rgba(239, 68, 68, 0.1)' : 'rgba(245, 158, 11, 0.1)',
                    color: isHighAlert ? '#F87171' : '#FBBF24',
                    padding: '2px 6px',
                    borderRadius: '4px',
                    fontSize: '0.65rem',
                    fontWeight: 700,
                    textTransform: 'uppercase'
                  }}>
                    {anom.anomaly_type}
                  </span>
                </div>
                <div style={{ fontSize: '0.75rem', color: '#64748B', marginTop: '4px' }}>
                  Processed: {new Date(anom.processed_at).toLocaleTimeString()}
                </div>
              </div>
              <div style={{ textAlign: 'right' }}>
                <div style={{ fontSize: '0.75rem', color: '#94A3B8' }}>Z-Score</div>
                <div style={{ fontSize: '1.25rem', fontWeight: 700, color: isHighAlert ? '#F87171' : '#FBBF24' }}>
                  {anom.anomaly_score?.toFixed(2) || "N/A"}
                </div>
              </div>
            </div>
          );
        })}
        {anomalies.length === 0 && (
          <div style={{ textAlign: 'center', padding: '32px', color: '#64748B' }}>
            No volatile or spike anomalies triggered. Markets are operating within normal ranges.
          </div>
        )}
      </div>
    </div>
  );
}
