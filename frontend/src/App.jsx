import React, { useState } from 'react';
import Header from './components/Header';
import StockInput from './components/StockInput';
import StockChart from './components/StockChart';
import MetricCard from './components/MetricCard';
import PortfolioGrid from './components/PortfolioGrid';
import LoginPage from './components/LoginPage';
import { DollarSign, TrendingUp, AlertTriangle, Activity, LogOut } from 'lucide-react';

function App() {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(false);
  const [data, setData] = useState([]);
  const [metrics, setMetrics] = useState({
    currentPrice: 0,
    predictedHigh: 0,
    riskScore: 0,
    volatility: '-'
  });
  const [error, setError] = useState(null);

  const handleLogin = (username) => {
    setUser(username);
  };

  const handleLogout = () => {
    setUser(null);
    setData([]);
    setMetrics({
      currentPrice: 0,
      predictedHigh: 0,
      riskScore: 0,
      volatility: '-'
    });
  };

  const handleAnalyze = async (params) => {
    setLoading(true);
    setError(null);
    try {
      const response = await fetch('http://localhost:8081/predict', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          ticker: params.ticker,
          start_date: params.startDate,
          end_date: params.endDate
        }),
      });

      if (!response.ok) {
        throw new Error('Failed to fetch prediction data');
      }

      const result = await response.json();

      // Update Chart Data
      setData(result.chart_data);

      // Update Metrics
      setMetrics({
        currentPrice: result.current_price.toFixed(2),
        predictedHigh: result.predicted_high.toFixed(2),
        riskScore: result.metrics.Decision_Score.toFixed(1),
        volatility: result.metrics.Volatility
      });

    } catch (err) {
      console.error(err);
      setError("Failed to load data. Please check if backend is running.");
    } finally {
      setLoading(false);
    }
  };

  const handleSelectStock = (ticker) => {
    // Auto-analyze selected stock from portfolio for the last year
    const endDate = new Date().toISOString().split('T')[0];
    const startDate = new Date();
    startDate.setFullYear(startDate.getFullYear() - 1);

    handleAnalyze({
      ticker: ticker,
      startDate: startDate.toISOString().split('T')[0],
      endDate: endDate
    });
  };

  if (!user) {
    return <LoginPage onLogin={handleLogin} />;
  }

  return (
    <div className="app-container animate-fade-in">
      <div className="header-wrapper">
        <Header />
        <button className="logout-btn" onClick={handleLogout} title="Logout">
          <LogOut size={20} />
        </button>
      </div>

      <main className="main-content">
        <div className="container">

          <PortfolioGrid user={user} onSelectStock={handleSelectStock} />

          <section className="controls-section">
            <div className="section-divider">
              <span>Market Analysis</span>
            </div>
            <StockInput onAnalyze={handleAnalyze} isLoading={loading} />
            {error && <div style={{ color: 'var(--accent-red)', marginTop: '1rem', background: 'rgba(255,0,0,0.1)', padding: '10px', borderRadius: '8px' }}>{error}</div>}
          </section>

          <section className="metrics-grid">
            <MetricCard
              title="Current Price"
              value={`$${metrics.currentPrice}`}
              change="+2.4%"
              trend="up"
              icon={DollarSign}
            />
            <MetricCard
              title="Predicted High"
              value={`$${metrics.predictedHigh}`}
              change="+4.1%"
              trend="up"
              icon={TrendingUp}
            />
            <MetricCard
              title="Risk Score"
              value={metrics.riskScore}
              change="Moderate"
              trend="neutral"
              icon={AlertTriangle}
            />
            <MetricCard
              title="Volatility"
              value={metrics.volatility}
              trend="down"
              icon={Activity}
            />
          </section>

          <section className="charts-section">
            <StockChart data={data} title="Price Forecast vs Actual" />
          </section>
        </div>
      </main>

      <style jsx>{`
        .header-wrapper {
          position: relative;
        }

        .logout-btn {
          position: absolute;
          top: 1.5rem;
          right: 2rem;
          background: rgba(255, 255, 255, 0.1);
          border: 1px solid rgba(255, 255, 255, 0.1);
          color: white;
          width: 40px;
          height: 40px;
          border-radius: 10px;
          display: flex;
          align-items: center;
          justify-content: center;
          cursor: pointer;
          z-index: 101;
          transition: all 0.2s;
        }

        .logout-btn:hover {
          background: rgba(255, 68, 68, 0.2);
          color: #ff4444;
          border-color: rgba(255, 68, 68, 0.3);
        }

        .main-content {
          padding: 0 1rem 2rem;
        }

        .container {
          max-width: 1200px;
          margin: 0 auto;
          display: flex;
          flex-direction: column;
          gap: 2rem;
        }

        .section-divider {
            display: flex;
            align-items: center;
            margin: 1rem 0;
            color: var(--text-secondary);
            font-size: 0.9rem;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        
        .section-divider::before,
        .section-divider::after {
            content: '';
            flex: 1;
            height: 1px;
            background: rgba(255, 255, 255, 0.1);
        }

        .section-divider span {
            padding: 0 1rem;
        }

        .metrics-grid {
          display: grid;
          grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
          gap: 1.5rem;
        }

        .charts-section {
          display: flex;
          flex-direction: column;
          gap: 1.5rem;
        }
      `}</style>
    </div>
  );
}

export default App;
