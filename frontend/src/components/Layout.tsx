import { NavLink, Outlet } from 'react-router-dom';

import { useAuth } from '@/auth/AuthContext';

export function Layout() {
  const { user, logout } = useAuth();

  return (
    <div className="layout">
      <aside className="sidebar">
        <div className="sidebar__brand">AI Incident Investigator</div>
        <nav className="sidebar__nav">
          <NavLink to="/" end>
            Dashboard
          </NavLink>
          <NavLink to="/incidents">Incidents</NavLink>
        </nav>
        <div className="sidebar__footer">
          <span>{user?.email}</span>
          <button type="button" onClick={logout}>
            Sign out
          </button>
        </div>
      </aside>
      <main className="content">
        <Outlet />
      </main>
    </div>
  );
}
