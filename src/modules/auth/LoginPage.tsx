import { useState } from 'react';
import { Mail, Lock, Loader2 } from 'lucide-react';
import { useAuth } from '../../shared/AuthContext';

export function LoginPage() {
  const { login, error, isLoading } = useAuth();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!email.trim() || !password.trim()) return;
    await login(email.trim(), password);
  };

  return (
    <div className="login-page">
      <div className="login-card">
        <div className="login-header">
          <div className="login-logo">
            <span>TS</span>
          </div>
          <h1>Task Studio</h1>
          <p>Sign in to your workspace</p>
        </div>

        <form className="login-form" onSubmit={handleSubmit}>
          {error ? <div className="login-error">{error}</div> : null}

          <label className="login-field">
            <Mail size={18} className="login-field-icon" />
            <input
              type="email"
              placeholder="Email address"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              autoComplete="email"
              autoFocus
              required
            />
          </label>

          <label className="login-field">
            <Lock size={18} className="login-field-icon" />
            <input
              type="password"
              placeholder="Password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              autoComplete="current-password"
              required
            />
          </label>

          <button type="submit" className="login-button" disabled={isLoading}>
            {isLoading ? (
              <><Loader2 size={18} className="spin" /> Signing in…</>
            ) : (
              'Sign in'
            )}
          </button>
        </form>

        <div className="login-footer">
          <p>Demo credentials</p>
          <code>duc@taskstudio.io / demo1234</code>
        </div>
      </div>
    </div>
  );
}
