import { LogOut, Shield, Mail, User as UserIcon } from 'lucide-react';
import type { User } from '../../shared/types';

type AuthInfoViewProps = {
  user: User;
  onLogout: () => void;
};

// TODO(security): Add MFA configuration, OAuth provider linking, and session history for production.

export function AuthInfoView({ user, onLogout }: AuthInfoViewProps) {
  return (
    <>
      <header className="page-header" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-end', marginBottom: '24px' }}>
        <div>
          <h1>Account</h1>
          <p className="lede">Your profile and session information.</p>
        </div>
      </header>

      <section className="dashboard-grid screen-grid">
        <article className="widget-panel">
          <div className="panel-header">
            <h2>Profile</h2>
          </div>
          <div className="widget-content" style={{ padding: '24px' }}>
            <div className="auth-profile">
              <div className="user-avatar-lg" style={{ backgroundColor: user.avatarColor ?? '#0C66E4' }}>
                {user.name.charAt(0)}
              </div>
              <div className="auth-profile-info">
                <h3>{user.name}</h3>
                <div className="auth-detail">
                  <Mail size={14} />
                  <span>{user.email}</span>
                </div>
                <div className="auth-detail">
                  <Shield size={14} />
                  <span className={`pill status-${user.role}`}>{user.role}</span>
                </div>
                <div className="auth-detail">
                  <UserIcon size={14} />
                  <span>User ID: {user.id}</span>
                </div>
              </div>
            </div>
          </div>
        </article>

        <article className="widget-panel">
          <div className="panel-header">
            <h2>Session</h2>
          </div>
          <div className="widget-content" style={{ padding: '24px' }}>
            <div className="auth-session">
              <div className="auth-detail">
                <span className="session-status-dot" />
                <span>Active session</span>
              </div>
              <p className="auth-session-note">
                You are currently signed in. Your session persists within this browser tab.
              </p>
              <button type="button" className="logout-button" onClick={onLogout}>
                <LogOut size={16} />
                Sign out
              </button>
            </div>
          </div>
        </article>
      </section>
    </>
  );
}
