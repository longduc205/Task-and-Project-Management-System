import { useState, useEffect } from 'react';
import { Mail } from 'lucide-react';
import { fetchUsers } from '../../shared/api';
import type { User } from '../../shared/types';

export function UserList() {
  const [users, setUsers] = useState<User[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchUsers()
      .then((data) => {
        // Strip passwords before storing in state
        setUsers(data.map(({ password: _, ...u }) => u));
      })
      .catch(() => setUsers([]))
      .finally(() => setLoading(false));
  }, []);

  if (loading) {
    return <p className="empty-state">Loading users…</p>;
  }

  if (users.length === 0) {
    return (
      <div className="empty-state empty-illustrated">
        <strong>No users found</strong>
        <p>Could not load team members from the API.</p>
      </div>
    );
  }

  return (
    <>
      <header className="page-header" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-end', marginBottom: '24px' }}>
        <div>
          <h1>Team Members</h1>
          <p className="lede">All users in your workspace.</p>
        </div>
        <div className="kanban-actions">
          <span>{users.length} members</span>
        </div>
      </header>

      <section className="dashboard-grid screen-grid">
        <article className="widget-panel">
          <div className="widget-content" style={{ padding: 0, gap: 0 }}>
            {users.map((user) => (
              <div key={user.id} className="task-row user-row">
                <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
                  <div className="user-avatar" style={{ backgroundColor: user.avatarColor ?? '#0C66E4' }}>
                    {user.name.charAt(0)}
                  </div>
                  <div className="task-row-main">
                    <strong>{user.name}</strong>
                    <span style={{ display: 'flex', alignItems: 'center', gap: '4px' }}>
                      <Mail size={12} />
                      {user.email}
                    </span>
                  </div>
                </div>
                <div className="task-row-meta">
                  <span className={`pill status-${user.role}`}>{user.role}</span>
                </div>
              </div>
            ))}
          </div>
        </article>
      </section>
    </>
  );
}
