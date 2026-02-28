import React, { useState } from 'react';
import { User, Lock, ArrowRight } from 'lucide-react';

const LoginPage = ({ onLogin }) => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');

    const handleLogin = (e) => {
        e.preventDefault();
        // Sample login details for 3 users
        const users = {
            'user1': 'pass1',
            'user2': 'pass2',
            'user3': 'pass3'
        };

        if (users[username] && users[username] === password) {
            onLogin(username);
        } else {
            setError('Invalid credentials. Try user1/pass1');
        }
    };

    return (
        <div className="login-container">
            <div className="login-card glass-panel">
                <div className="login-header">
                    <h1 className="text-gradient">Portfolio Login</h1>
                    <p className="subtitle">Welcome back to your dashboard</p>
                </div>

                <form onSubmit={handleLogin} className="login-form">
                    <div className="input-group">
                        <User className="input-icon" size={20} />
                        <input
                            type="text"
                            placeholder="Username"
                            value={username}
                            onChange={(e) => setUsername(e.target.value)}
                            className="glass-input"
                        />
                    </div>

                    <div className="input-group">
                        <Lock className="input-icon" size={20} />
                        <input
                            type="password"
                            placeholder="Password"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            className="glass-input"
                        />
                    </div>

                    {error && <div className="error-message">{error}</div>}

                    <button type="submit" className="login-btn">
                        <span>Sign In</span>
                        <ArrowRight size={20} />
                    </button>
                </form>

                <div className="demo-credentials">
                    <p>Demo Credentials:</p>
                    <div className="creds-list">
                        <span>user1 / pass1</span>
                        <span>user2 / pass2</span>
                        <span>user3 / pass3</span>
                    </div>
                </div>
            </div>

            <style jsx>{`
        .login-container {
          min-height: 100vh;
          display: flex;
          align-items: center;
          justify-content: center;
          background: radial-gradient(circle at top right, #1a2942 0%, #0a0e17 100%);
          color: white;
        }

        .login-card {
          width: 100%;
          max-width: 400px;
          padding: 3rem;
          border-radius: 24px;
          border: 1px solid rgba(255, 255, 255, 0.1);
          background: rgba(10, 14, 23, 0.7);
          backdrop-filter: blur(20px);
          box-shadow: 0 20px 40px rgba(0, 0, 0, 0.4);
        }

        .login-header {
          text-align: center;
          margin-bottom: 2.5rem;
        }

        .subtitle {
          color: #94a3b8;
          font-size: 0.9rem;
          margin-top: 0.5rem;
        }

        .login-form {
          display: flex;
          flex-direction: column;
          gap: 1.5rem;
        }

        .input-group {
          position: relative;
        }

        .input-icon {
          position: absolute;
          left: 1rem;
          top: 50%;
          transform: translateY(-50%);
          color: #64748b;
        }

        .glass-input {
          width: 100%;
          padding: 1rem 1rem 1rem 3rem;
          border-radius: 12px;
          border: 1px solid rgba(255, 255, 255, 0.1);
          background: rgba(255, 255, 255, 0.05);
          color: white;
          font-size: 1rem;
          transition: all 0.3s ease;
          outline: none;
        }

        .glass-input:focus {
          border-color: var(--accent-cyan);
          background: rgba(255, 255, 255, 0.1);
          box-shadow: 0 0 15px rgba(0, 240, 255, 0.2);
        }

        .login-btn {
          background: linear-gradient(135deg, var(--accent-cyan) 0%, var(--accent-blue) 100%);
          color: white;
          border: none;
          padding: 1rem;
          border-radius: 12px;
          font-weight: 600;
          font-size: 1rem;
          cursor: pointer;
          display: flex;
          align-items: center;
          justify-content: center;
          gap: 0.5rem;
          transition: transform 0.2s, box-shadow 0.2s;
        }

        .login-btn:hover {
          transform: translateY(-2px);
          box-shadow: 0 10px 20px rgba(0, 240, 255, 0.3);
        }

        .error-message {
          color: #ff6b6b;
          font-size: 0.9rem;
          text-align: center;
          background: rgba(255, 107, 107, 0.1);
          padding: 0.5rem;
          border-radius: 8px;
        }

        .demo-credentials {
          margin-top: 2rem;
          padding-top: 1.5rem;
          border-top: 1px solid rgba(255, 255, 255, 0.1);
          text-align: center;
          font-size: 0.8rem;
          color: #64748b;
        }

        .creds-list {
          display: flex;
          justify-content: center;
          gap: 1rem;
          margin-top: 0.5rem;
        }

        .creds-list span {
          background: rgba(255, 255, 255, 0.05);
          padding: 0.2rem 0.6rem;
          border-radius: 4px;
        }
      `}</style>
        </div>
    );
};

export default LoginPage;
