import React from 'react';
import { DollarSign, TrendingUp, TrendingDown, Briefcase } from 'lucide-react';

const PortfolioGrid = ({ user, onSelectStock }) => {
    // Mock data for each user
    const userPortfolios = {
        'user1': [
            { symbol: 'AAPL', name: 'Apple Inc.', qty: 15, avgPrice: 145.20, currentPrice: 172.50, change: '+18.8%' },
            { symbol: 'MSFT', name: 'Microsoft', qty: 10, avgPrice: 280.50, currentPrice: 315.20, change: '+12.4%' },
            { symbol: 'GOOGL', name: 'Alphabet Inc.', qty: 8, avgPrice: 130.00, currentPrice: 138.40, change: '+6.5%' },
            { symbol: 'AMZN', name: 'Amazon', qty: 20, avgPrice: 135.00, currentPrice: 129.50, change: '-4.1%' },
        ],
        'user2': [
            { symbol: 'TSLA', name: 'Tesla Inc.', qty: 50, avgPrice: 210.00, currentPrice: 245.30, change: '+16.8%' },
            { symbol: 'NVDA', name: 'NVIDIA', qty: 12, avgPrice: 350.00, currentPrice: 460.10, change: '+31.4%' },
        ],
        'user3': [
            { symbol: 'BTC', name: 'Bitcoin', qty: 0.5, avgPrice: 35000, currentPrice: 42000, change: '+20.0%' },
            { symbol: 'ETH', name: 'Ethereum', qty: 5, avgPrice: 2100, currentPrice: 2250, change: '+7.1%' },
            { symbol: 'COIN', name: 'Coinbase', qty: 100, avgPrice: 85.00, currentPrice: 140.20, change: '+64.9%' },
        ]
    };

    const stocks = userPortfolios[user] || [];

    return (
        <div className="portfolio-section">
            <div className="section-header">
                <Briefcase className="section-icon" />
                <h2>Your Portfolio</h2>
            </div>

            <div className="grid-container">
                {stocks.map((stock, index) => {
                    const isPositive = stock.change.startsWith('+');
                    return (
                        <div key={index} className="stock-card glass-panel" onClick={() => onSelectStock && onSelectStock(stock.symbol)}>
                            <div className="card-header">
                                <div>
                                    <h3 className="symbol">{stock.symbol}</h3>
                                    <p className="name">{stock.name}</p>
                                </div>
                                <div className={`trend-badge ${isPositive ? 'positive' : 'negative'}`}>
                                    {isPositive ? <TrendingUp size={16} /> : <TrendingDown size={16} />}
                                    {stock.change}
                                </div>
                            </div>

                            <div className="card-stats">
                                <div className="stat-row">
                                    <span className="label">Quantity</span>
                                    <span className="value">{stock.qty}</span>
                                </div>
                                <div className="stat-row">
                                    <span className="label">Avg. Price</span>
                                    <span className="value system-font">${stock.avgPrice.toFixed(2)}</span>
                                </div>
                                <div className="stat-row highlight">
                                    <span className="label">Current</span>
                                    <span className="value system-font">${stock.currentPrice.toFixed(2)}</span>
                                </div>
                            </div>

                            <div className="card-footer">
                                <div className="total-value">
                                    <DollarSign size={14} className="currency-icon" />
                                    <span>{(stock.qty * stock.currentPrice).toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}</span>
                                </div>
                                <span className="total-label">Total Value</span>
                            </div>
                        </div>
                    );
                })}
            </div>

            <style jsx>{`
        .portfolio-section {
          margin-bottom: 3rem;
        }

        .section-header {
          display: flex;
          align-items: center;
          gap: 0.8rem;
          margin-bottom: 1.5rem;
          color: var(--text-primary);
        }

        .section-icon {
          color: var(--accent-cyan);
        }

        .grid-container {
          display: grid;
          grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
          gap: 1.5rem;
        }

        .stock-card {
          background: var(--glass-bg);
          border: var(--glass-border);
          border-radius: 16px;
          padding: 1.5rem;
          transition: transform 0.2s, box-shadow 0.2s;
          cursor: pointer;
          position: relative;
          overflow: hidden;
        }

        .stock-card:hover {
          transform: translateY(-5px);
          box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
          border-color: rgba(255, 255, 255, 0.2);
        }

        .stock-card::before {
          content: '';
          position: absolute;
          top: 0;
          left: 0;
          right: 0;
          height: 4px;
          background: linear-gradient(90deg, var(--accent-cyan), var(--accent-blue));
          opacity: 0;
          transition: opacity 0.2s;
        }

        .stock-card:hover::before {
          opacity: 1;
        }

        .card-header {
          display: flex;
          justify-content: space-between;
          align-items: flex-start;
          margin-bottom: 1.5rem;
        }

        .symbol {
          font-size: 1.5rem;
          font-weight: 700;
          color: white;
          margin: 0;
        }

        .name {
          color: var(--text-secondary);
          font-size: 0.85rem;
          margin-top: 0.2rem;
        }

        .trend-badge {
          display: flex;
          align-items: center;
          gap: 4px;
          padding: 4px 8px;
          border-radius: 8px;
          font-size: 0.85rem;
          font-weight: 600;
        }

        .trend-badge.positive {
          background: rgba(16, 185, 129, 0.2);
          color: #34d399;
        }

        .trend-badge.negative {
          background: rgba(239, 68, 68, 0.2);
          color: #f87171;
        }

        .card-stats {
          display: flex;
          flex-direction: column;
          gap: 0.8rem;
          margin-bottom: 1.5rem;
        }

        .stat-row {
          display: flex;
          justify-content: space-between;
          align-items: center;
          font-size: 0.9rem;
        }

        .label {
          color: var(--text-secondary);
        }

        .value {
          color: var(--text-primary);
          font-weight: 500;
        }

        .highlight .value {
          color: white;
          font-weight: 600;
        }

        .card-footer {
          border-top: 1px solid rgba(255, 255, 255, 0.05);
          padding-top: 1rem;
          display: flex;
          justify-content: space-between;
          align-items: center;
        }

        .total-value {
          font-size: 1.2rem;
          font-weight: 700;
          color: white;
          display: flex;
          align-items: center;
          gap: 2px;
          font-family: 'JetBrains Mono', monospace;
        }

        .currency-icon {
          color: var(--text-secondary);
        }

        .total-label {
          font-size: 0.75rem;
          color: var(--text-secondary);
          text-transform: uppercase;
          letter-spacing: 0.5px;
        }
      `}</style>
        </div>
    );
};

export default PortfolioGrid;
