import React, { useState } from 'react';
import { Search, Calendar } from 'lucide-react';

const StockInput = ({ onAnalyze, isLoading }) => {
    const [ticker, setTicker] = useState('AAPL');
    const [startDate, setStartDate] = useState('2020-01-01');
    const [endDate, setEndDate] = useState('2023-01-01');

    const handleSubmit = (e) => {
        e.preventDefault();
        onAnalyze({ ticker, startDate, endDate });
    };

    return (
        <form onSubmit={handleSubmit} className="stock-form glass-panel">
            <div className="input-group">
                <label>Ticker Symbol</label>
                <div className="input-wrapper">
                    <Search size={18} className="input-icon" />
                    <input
                        type="text"
                        value={ticker}
                        onChange={(e) => setTicker(e.target.value.toUpperCase())}
                        placeholder="e.g. AAPL"
                    />
                </div>
            </div>

            <div className="input-group">
                <label>Start Date</label>
                <div className="input-wrapper">
                    <Calendar size={18} className="input-icon" />
                    <input
                        type="date"
                        value={startDate}
                        onChange={(e) => setStartDate(e.target.value)}
                    />
                </div>
            </div>

            <div className="input-group">
                <label>End Date</label>
                <div className="input-wrapper">
                    <Calendar size={18} className="input-icon" />
                    <input
                        type="date"
                        value={endDate}
                        onChange={(e) => setEndDate(e.target.value)}
                    />
                </div>
            </div>

            <div className="action-group">
                <button type="submit" disabled={isLoading} className="analyze-btn">
                    {isLoading ? 'Analyzing...' : 'Analyze Stock'}
                </button>
            </div>

            <style jsx>{`
        .stock-form {
          padding: 1.5rem;
          border-radius: var(--radius-md);
          display: grid;
          grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
          gap: 1.5rem;
          align-items: end;
          margin-bottom: 2rem;
        }

        .input-group {
          display: flex;
          flex-direction: column;
          gap: 0.5rem;
        }

        label {
          font-size: 0.85rem;
          color: var(--text-secondary);
          font-weight: 500;
        }

        .input-wrapper {
          position: relative;
          display: flex;
          align-items: center;
        }

        .input-icon {
          position: absolute;
          left: 12px;
          color: var(--text-secondary);
        }

        input {
          width: 100%;
          background: rgba(0, 0, 0, 0.2);
          border: 1px solid rgba(255, 255, 255, 0.1);
          padding: 12px 12px 12px 40px;
          border-radius: 8px;
          color: var(--text-primary);
          font-size: 1rem;
          transition: all 0.2s;
        }

        input:focus {
          outline: none;
          border-color: var(--accent-cyan);
          background: rgba(0, 0, 0, 0.4);
        }

        .analyze-btn {
          width: 100%;
          background: linear-gradient(135deg, var(--accent-cyan), var(--accent-purple));
          color: white;
          padding: 12px;
          border-radius: 8px;
          font-weight: 600;
          font-size: 1rem;
          transition: opacity 0.2s;
        }

        .analyze-btn:hover {
          opacity: 0.9;
        }

        .analyze-btn:disabled {
          opacity: 0.5;
          cursor: not-allowed;
        }
      `}</style>
        </form>
    );
};

export default StockInput;
