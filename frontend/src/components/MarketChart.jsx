import React from 'react';

export default function MarketChart({ trades = [] }) {
  // Sort trades by timestamp
  const sorted = [...trades].sort((a, b) => new Date(a.event_time) - new Date(b.event_time));
  
  // Calculate SVG dimensions
  const width = 500;
  const height = 180;
  const padding = 20;
  
  let points = "";
  let latestPrice = 0;
  let pctChange = 0.0;
  
  if (sorted.length > 1) {
    const prices = sorted.map(t => t.price);
    const minPrice = Math.min(...prices) * 0.999;
    const maxPrice = Math.max(...prices) * 1.001;
    const priceRange = maxPrice - minPrice || 1.0;
    
    latestPrice = prices[prices.length - 1];
    const initialPrice = prices[0];
    pctChange = ((latestPrice - initialPrice) / initialPrice) * 100;
    
    points = sorted.map((t, idx) => {
      const x = padding + (idx / (sorted.length - 1)) * (width - 2 * padding);
      const y = height - padding - ((t.price - minPrice) / priceRange) * (height - 2 * padding);
      return `${x},${y}`;
    }).join(" ");
  }

  const isUp = pctChange >= 0;

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
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '16px' }}>
        <div>
          <h2 style={{ fontSize: '1.25rem', fontWeight: 600, margin: 0, letterSpacing: '-0.025em' }}>Simulated Real-Time Price Stream</h2>
          <div style={{ fontSize: '0.75rem', color: '#64748B', marginTop: '2px' }}>Aggregated Nasdaq/NYSE feed</div>
        </div>
        <div style={{ textAlign: 'right' }}>
          <div style={{ fontSize: '1.5rem', fontWeight: 700, color: '#F8FAFC' }}>
            ${latestPrice > 0 ? latestPrice.toFixed(2) : "---"}
          </div>
          <div style={{ fontSize: '0.85rem', fontWeight: 600, color: isUp ? '#34D399' : '#F87171' }}>
            {isUp ? "+" : ""}{pctChange.toFixed(2)}%
          </div>
        </div>
      </div>

      <div style={{ position: 'relative', width: '100%', display: 'flex', justifyContent: 'center' }}>
        {sorted.length > 1 ? (
          <svg viewBox={`0 0 ${width} ${height}`} style={{ width: '100%', height: 'auto', overflow: 'visible' }}>
            <defs>
              <linearGradient id="chartGrad" x1="0" y1="0" x2="0" y2="1">
                <stop offset="0%" stopColor={isUp ? "#10B981" : "#EF4444"} stopOpacity="0.2"/>
                <stop offset="100%" stopColor={isUp ? "#10B981" : "#EF4444"} stopOpacity="0"/>
              </linearGradient>
            </defs>
            {/* Draw Area */}
            <polygon
              points={`${padding},${height - padding} ${points} ${width - padding},${height - padding}`}
              fill="url(#chartGrad)"
            />
            {/* Draw Line */}
            <polyline
              fill="none"
              stroke={isUp ? "#10B981" : "#EF4444"}
              strokeWidth="2.5"
              points={points}
            />
          </svg>
        ) : (
          <div style={{ height: '140px', display: 'flex', alignItems: 'center', color: '#64748B' }}>
            Awaiting streaming events to render chart...
          </div>
        )}
      </div>
    </div>
  );
}
