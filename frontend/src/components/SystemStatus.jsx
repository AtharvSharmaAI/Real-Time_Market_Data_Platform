import React from 'react';

export default function SystemStatus({ health = { status: "OK" }, metrics = { throughput: 120.4, latency: 15.2, dlq_rate: 0.0, anomaly_rate: 1.2 } }) {
  const statusColor = health.status === "OK" ? "#10B981" : "#EF4444";
  
  return (
    <div style={{
      background: 'rgba(30, 41, 59, 0.6)',
      backdropFilter: 'blur(12px)',
      border: '1px solid rgba(255, 255, 255, 0.08)',
      borderRadius: '16px',
      padding: '24px',
      color: '#F8FAFC',
      boxShadow: '0 8px 32px 0 rgba(0, 0, 0, 0.3)',
      maxWidth: '450px',
      width: '100%',
      fontFamily: 'system-ui, -apple-system, sans-serif'
    }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
        <h2 style={{ fontSize: '1.25rem', fontWeight: 600, margin: 0, letterSpacing: '-0.025em' }}>System Status</h2>
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
          <span style={{ width: '10px', height: '10px', borderRadius: '50%', backgroundColor: statusColor, display: 'inline-block' }}></span>
          <span style={{ fontSize: '0.875rem', color: '#94A3B8', textTransform: 'uppercase', fontWeight: 700 }}>
            {health.status || "UNKNOWN"}
          </span>
        </div>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '16px' }}>
        <div style={{ padding: '16px', backgroundColor: 'rgba(15, 23, 42, 0.4)', borderRadius: '12px' }}>
          <div style={{ fontSize: '0.75rem', color: '#64748B', textTransform: 'uppercase', fontWeight: 700, marginBottom: '4px' }}>Throughput</div>
          <div style={{ fontSize: '1.5rem', fontWeight: 700, color: '#38BDF8' }}>{metrics.throughput || "0.0"} <span style={{ fontSize: '0.75rem', color: '#94A3B8' }}>evt/s</span></div>
        </div>

        <div style={{ padding: '16px', backgroundColor: 'rgba(15, 23, 42, 0.4)', borderRadius: '12px' }}>
          <div style={{ fontSize: '0.75rem', color: '#64748B', textTransform: 'uppercase', fontWeight: 700, marginBottom: '4px' }}>Latency</div>
          <div style={{ fontSize: '1.5rem', fontWeight: 700, color: '#A78BFA' }}>{metrics.latency || "0.0"} <span style={{ fontSize: '0.75rem', color: '#94A3B8' }}>ms</span></div>
        </div>

        <div style={{ padding: '16px', backgroundColor: 'rgba(15, 23, 42, 0.4)', borderRadius: '12px' }}>
          <div style={{ fontSize: '0.75rem', color: '#64748B', textTransform: 'uppercase', fontWeight: 700, marginBottom: '4px' }}>DLQ Rate</div>
          <div style={{ fontSize: '1.5rem', fontWeight: 700, color: '#F43F5E' }}>{metrics.dlq_rate || "0.0"} <span style={{ fontSize: '0.75rem', color: '#94A3B8' }}>evt/s</span></div>
        </div>

        <div style={{ padding: '16px', backgroundColor: 'rgba(15, 23, 42, 0.4)', borderRadius: '12px' }}>
          <div style={{ fontSize: '0.75rem', color: '#64748B', textTransform: 'uppercase', fontWeight: 700, marginBottom: '4px' }}>Anomaly Rate</div>
          <div style={{ fontSize: '1.5rem', fontWeight: 700, color: '#F59E0B' }}>{metrics.anomaly_rate || "0.0"} <span style={{ fontSize: '0.75rem', color: '#94A3B8' }}>evt/m</span></div>
        </div>
      </div>
    </div>
  );
}
