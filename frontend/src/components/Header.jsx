import React from 'react';
import { TrendingUp, Activity } from 'lucide-react';

const Header = () => {
  return (
    <header className="header glass-panel">
      <div className="logo-section">
        <div className="icon-wrapper">
          <TrendingUp size={28} color="var(--accent-cyan)" />
        </div>
        <div>
          <h1 className="app-title text-gradient">Portfolio<span style={{ color: 'var(--text-primary)' }}>Manager</span></h1>
          <p className="app-subtitle">Risk-Aware Forecasting</p>
        </div>
      </div>

      <div className="header-actions">
        <button className="icon-btn">
          <Activity size={20} color="var(--text-secondary)" />
        </button>
      </div>

      <style jsx>{`
        .header {
          display: flex;
          align-items: center;
          justify-content: space-between;
          padding: 1rem 2rem;
          position: sticky;
          top: 0;
          z-index: 100;
          border-bottom: var(--glass-border);
          border-radius: 0 0 var(--radius-lg) var(--radius-lg);
          margin-bottom: 2rem;
        }
        
        .logo-section {
          display: flex;
          align-items: center;
          gap: 1rem;
        }

        .icon-wrapper {
          background: rgba(0, 240, 255, 0.1);
          padding: 10px;
          border-radius: 12px;
          display: flex;
          align-items: center;
          justify-content: center;
        }

        .app-title {
          font-size: 1.5rem;
          font-weight: 700;
          letter-spacing: -0.5px;
          line-height: 1.1;
        }

        .app-subtitle {
          font-size: 0.8rem;
          color: var(--text-secondary);
          letter-spacing: 0.5px;
          text-transform: uppercase;
          font-weight: 500;
        }
      `}</style>
    </header>
  );
};

export default Header;
