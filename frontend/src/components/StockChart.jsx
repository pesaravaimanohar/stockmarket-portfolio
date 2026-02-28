import React from 'react';
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend } from 'recharts';

const StockChart = ({ data, title }) => {
    return (
        <div className="chart-container glass-panel">
            <h3 className="chart-title">{title}</h3>
            <div className="chart-wrapper">
                <ResponsiveContainer width="100%" height="100%">
                    <AreaChart
                        data={data}
                        margin={{ top: 10, right: 30, left: 0, bottom: 0 }}
                    >
                        <defs>
                            <linearGradient id="colorActual" x1="0" y1="0" x2="0" y2="1">
                                <stop offset="5%" stopColor="#38bdf8" stopOpacity={0.3} />
                                <stop offset="95%" stopColor="#38bdf8" stopOpacity={0} />
                            </linearGradient>
                            <linearGradient id="colorPred" x1="0" y1="0" x2="0" y2="1">
                                <stop offset="5%" stopColor="#bd00ff" stopOpacity={0.3} />
                                <stop offset="95%" stopColor="#bd00ff" stopOpacity={0} />
                            </linearGradient>
                        </defs>
                        <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" vertical={false} />
                        <XAxis
                            dataKey="date"
                            stroke="#64748b"
                            fontSize={12}
                            tickLine={false}
                            axisLine={false}
                        />
                        <YAxis
                            stroke="#64748b"
                            fontSize={12}
                            tickLine={false}
                            axisLine={false}
                            tickFormatter={(value) => `$${value}`}
                        />
                        <Tooltip
                            contentStyle={{ backgroundColor: '#0f172a', border: '1px solid #1e293b', borderRadius: '8px' }}
                            itemStyle={{ color: '#f1f5f9' }}
                        />
                        <Legend verticalAlign="top" height={36} />
                        <Area
                            type="monotone"
                            dataKey="actual"
                            name="Actual Price"
                            stroke="#38bdf8"
                            fillOpacity={1}
                            fill="url(#colorActual)"
                            strokeWidth={2}
                        />
                        <Area
                            type="monotone"
                            dataKey="predicted"
                            name="Predicted Price"
                            stroke="#bd00ff"
                            fillOpacity={1}
                            fill="url(#colorPred)"
                            strokeWidth={2}
                        />
                    </AreaChart>
                </ResponsiveContainer>
            </div>

            <style jsx>{`
        .chart-container {
          padding: 1.5rem;
          border-radius: var(--radius-md);
          height: 400px;
          display: flex;
          flex-direction: column;
        }

        .chart-title {
          font-size: 1.1rem;
          font-weight: 600;
          margin-bottom: 1rem;
          color: var(--text-primary);
        }

        .chart-wrapper {
          flex: 1;
          width: 100%;
          min-height: 0;
        }
      `}</style>
        </div>
    );
};

export default StockChart;
