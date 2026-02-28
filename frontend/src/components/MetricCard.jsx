import React from 'react';

const MetricCard = ({ title, value, change, icon: Icon, trend }) => {
    const isPositive = trend === 'up';
    const isNeutral = trend === 'neutral';

    return (
        <div className="metric-card glass-panel">
            <div className="card-header">
                <span className="card-title">{title}</span>
                {Icon && <Icon size={18} className="card-icon" />}
            </div>
            <div className="card-body">
                <h3 className="card-value">{value}</h3>
                {change && (
                    <span className={`card-change ${isPositive ? 'positive' : isNeutral ? 'neutral' : 'negative'}`}>
                        {change}
                    </span>
                )}
            </div>

            <style jsx>{`
        .metric-card {
          padding: 1.5rem;
          border-radius: var(--radius-md);
          display: flex;
          flex-direction: column;
          gap: 0.5rem;
          transition: transform 0.2s;
        }
        
        .metric-card:hover {
          transform: translateY(-2px);
          border-color: rgba(255,255,255,0.2);
        }

        .card-header {
          display: flex;
          justify-content: space-between;
          align-items: center;
          color: var(--text-secondary);
        }

        .card-title {
          font-size: 0.9rem;
          font-weight: 500;
        }

        .card-icon {
          opacity: 0.7;
        }

        .card-value {
          font-size: 1.8rem;
          font-weight: 700;
          color: var(--text-primary);
        }

        .card-change {
          font-size: 0.85rem;
          font-weight: 600;
          padding: 4px 8px;
          border-radius: 20px;
          margin-top: 4px;
          display: inline-block;
        }

        .positive {
          color: var(--accent-green);
          background: rgba(0, 255, 157, 0.1);
        }

        .negative {
          color: var(--accent-red);
          background: rgba(255, 77, 77, 0.1);
        }
        
        .neutral {
          color: var(--text-secondary);
          background: rgba(255, 255, 255, 0.05);
        }
      `}</style>
        </div>
    );
};

export default MetricCard;
