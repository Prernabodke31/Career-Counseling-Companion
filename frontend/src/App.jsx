import { BrowserRouter, Routes, Route, Navigate, useNavigate, useLocation } from 'react-router-dom'
import { Toaster } from 'react-hot-toast'
import { AuthProvider, useAuth } from './AuthContext'

import Login from './pages/Login'
import Register from './pages/Register'
import Dashboard from './pages/Dashboard'
import Profile from './pages/Profile'
import Assessment from './pages/Assessment'
import CareerPlan from './pages/CareerPlan'
import Chat from './pages/Chat'
import Market from './pages/Market'

// ── Nav Config ────────────────────────────────────────────────
const NAV_ITEMS = [
  { path: '/',           label: 'Dashboard',         icon: '🏠' },
  { path: '/profile',    label: 'My Profile',         icon: '👤' },
  { path: '/assessment', label: 'Self Assessment',    icon: '📝' },
  { path: '/career',     label: 'Career Plan',        icon: '🎯' },
  { path: '/chat',       label: 'AI Counselor Chat',  icon: '💬' },
  { path: '/market',     label: 'Market Insights',    icon: '📊' },
]

// ── Protected Shell Layout ────────────────────────────────────
function AppShell({ children }) {
  const { user, logout } = useAuth()
  const navigate = useNavigate()
  const location = useLocation()

  return (
    <div className="app-shell">
      {/* Sidebar */}
      <aside className="sidebar">
        <div className="sidebar-logo">
          <h2>CAREER COUNSELOR</h2>
          <p>IBM Granite · WatsonX.ai</p>
        </div>
        <nav className="sidebar-nav">
          {NAV_ITEMS.map(item => (
            <div
              key={item.path}
              className={`nav-item ${location.pathname === item.path ? 'active' : ''}`}
              onClick={() => navigate(item.path)}
            >
              <span style={{ fontSize: '1rem' }}>{item.icon}</span>
              <span>{item.label}</span>
            </div>
          ))}
        </nav>
        <div className="sidebar-footer">
          <div style={{ marginBottom: 8, color: '#c6c6c6', fontSize: '0.78rem' }}>
            Signed in as<br />
            <strong style={{ color: '#f4f4f4' }}>{user?.name}</strong>
          </div>
          <button
            onClick={logout}
            style={{
              background: 'transparent', border: '1px solid #525252',
              color: '#c6c6c6', padding: '5px 10px', borderRadius: 4,
              cursor: 'pointer', fontSize: '0.75rem', fontFamily: 'inherit', width: '100%',
            }}
          >
            Sign Out
          </button>
        </div>
      </aside>

      {/* Main Area */}
      <div className="main-content">
        <header className="topbar">
          <span className="topbar-title">
            {NAV_ITEMS.find(n => n.path === location.pathname)?.label || 'Career Counselor'}
          </span>
          <div className="topbar-right">
            <span className="user-badge">🤖 IBM Granite Active</span>
          </div>
        </header>
        <main>{children}</main>
      </div>
    </div>
  )
}

// ── Route Guard ───────────────────────────────────────────────
function PrivateRoute({ children }) {
  const { isLoggedIn } = useAuth()
  return isLoggedIn ? children : <Navigate to="/login" replace />
}

// ── App Root ──────────────────────────────────────────────────
export default function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Toaster
          position="top-right"
          toastOptions={{
            style: { fontSize: '0.875rem', maxWidth: 360 },
            success: { iconTheme: { primary: '#198038', secondary: '#fff' } },
          }}
        />
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />

          <Route path="/" element={
            <PrivateRoute>
              <AppShell><Dashboard /></AppShell>
            </PrivateRoute>
          } />
          <Route path="/profile" element={
            <PrivateRoute>
              <AppShell><Profile /></AppShell>
            </PrivateRoute>
          } />
          <Route path="/assessment" element={
            <PrivateRoute>
              <AppShell><Assessment /></AppShell>
            </PrivateRoute>
          } />
          <Route path="/career" element={
            <PrivateRoute>
              <AppShell><CareerPlan /></AppShell>
            </PrivateRoute>
          } />
          <Route path="/chat" element={
            <PrivateRoute>
              <AppShell><Chat /></AppShell>
            </PrivateRoute>
          } />
          <Route path="/market" element={
            <PrivateRoute>
              <AppShell><Market /></AppShell>
            </PrivateRoute>
          } />

          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  )
}
