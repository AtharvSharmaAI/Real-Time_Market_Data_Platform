import React, { useState } from 'react';
import Dashboard from './pages/Dashboard';
import Anomalies from './pages/Anomalies';

export default function App() {
  const [currentTab, setCurrentTab] = useState('dashboard');

  return (
    <div style={{ minHeight: '100vh', backgroundColor: '#0F172A', fontFamily: 'system-ui, -apple-system, sans-serif' }}>
      {/* Navigation header */}
      <nav style={{
        background: 'rgba(15, 23, 42, 0.8)',
        backdropFilter: 'blur(8px)',
        borderBottom: '1px solid rgba(255, 255, 255, 0.05)',
        position: 'sticky',
        top: 0,
        zIndex: 50,
        padding: '0 24px'
      }}>
        <div style={{
          maxWidth: '1440px',
          margin: '0 auto',
          height: '64px',
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center'
        }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
            <span style={{ fontSize: '1.5rem', fontWeight: 900, color: '#38BDF8', letterSpacing: '-0.05em' }}>M</span>
            <span style={{ fontWeight: 700, color: '#F8FAFC', fontSize: '1.1rem' }}>MarketFlow</span>
          </div>

          <div style={{ display: 'flex', gap: '4px' }}>
            <button
              onClick={() => setCurrentTab('dashboard')}
              style={{
                background: currentTab === 'dashboard' ? 'rgba(56, 189, 248, 0.1)' : 'transparent',
                border: 'none',
                color: currentTab === 'dashboard' ? '#38BDF8' : '#94A3B8',
                padding: '8px 16px',
                borderRadius: '8px',
                cursor: 'pointer',
                fontWeight: 600,
                transition: 'all 0.2s'
              }}
            >
              Dashboard
            </button>
            <button
              onClick={() => setCurrentTab('anomalies')}
              style={{
                background: currentTab === 'anomalies' ? 'rgba(56, 189, 248, 0.1)' : 'transparent',
                border: 'none',
                color: currentTab === 'anomalies' ? '#38BDF8' : '#94A3B8',
                padding: '8px 16px',
                borderRadius: '8px',
                cursor: 'pointer',
                fontWeight: 600,
                transition: 'all 0.2s'
              }}
            >
              Anomaly Center
            </button>
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <main>
        {currentTab === 'dashboard' ? <Dashboard /> : <Anomalies />}
      </main>
    </div>
  );
}
