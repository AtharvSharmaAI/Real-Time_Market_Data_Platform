import React from 'react';

export default function VWAPPanel({ vwapData = [] }) {
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
      <h2 style={{ fontSize: '1.25rem', fontWeight: 600, margin: '0 0 20px 0', letterSpacing: '-0.025em' }}>VWAP Analytics (5s Tumbling Windows)</h2>
      
      <div style={{ overflowX: 'auto' }}>
        <table style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'left' }}>
          <thead>
            <tr style={{ borderBottom: '1px solid rgba(255, 255, 255, 0.1)' }}>
              <th style={{ padding: '12px 8px', fontSize: '0.75rem', color: '#94A3B8', textTransform: 'uppercase', fontWeight: 700 }}>Ticker</th>
              <th style={{ padding: '12px 8px', fontSize: '0.75rem', color: '#94A3B8', textTransform: 'uppercase', fontWeight: 700 }}>VWAP</th>
              <th style={{ padding: '12px 8px', fontSize: '0.75rem', color: '#94A3B8', textTransform: 'uppercase', fontWeight: 700 }}>Volume</th>
              <th style={{ padding: '12px 8px', fontSize: '0.75rem', color: '#94A3B8', textTransform: 'uppercase', fontWeight: 700 }}>Window Period</th>
            </tr>
          </thead>
          <tbody>
            {vwapData.map((row, idx) => (
              <tr key={idx} style={{ borderBottom: '1px solid rgba(255, 255, 255, 0.05)', verticalAlign: 'middle' }}>
                <td style={{ padding: '12px 8px', fontWeight: 700, color: '#38BDF8' }}>{row.symbol}</td>
                <td style={{ padding: '12px 8px', fontFamily: 'monospace', fontSize: '1rem', color: '#F1F5F9' }}>${row.vwap?.toFixed(2)}</td>
                <td style={{ padding: '12px 8px', color: '#CBD5E1' }}>{row.volume?.toLocaleString()}</td>
                <td style={{ padding: '12px 8px', fontSize: '0.85rem', color: '#94A3B8' }}>
                  {row.window_start} - {row.window_end}
                </td>
              </tr>
            ))}
            {vwapData.length === 0 && (
              <tr>
                <td colSpan={4} style={{ textAlign: 'center', padding: '24px', color: '#64748B' }}>No active window aggregates computed yet.</td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}
