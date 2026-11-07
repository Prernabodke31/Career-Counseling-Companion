import { useState } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import toast from 'react-hot-toast'
import api from '../api'
import { useAuth } from '../AuthContext'

export default function Register() {
  const { login } = useAuth()
  const nav = useNavigate()
  const [form, setForm] = useState({ full_name: '', email: '', password: '', confirm: '' })
  const [loading, setLoading] = useState(false)

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (form.password !== form.confirm) { toast.error('Passwords do not match.'); return }
    setLoading(true)
    try {
      const { data } = await api.post('/auth/register', {
        full_name: form.full_name,
        email: form.email,
        password: form.password,
        role: 'student',
      })
      login({ id: data.user_id, name: data.full_name, email: data.email, role: data.role }, data.access_token)
      toast.success('Account created! Welcome 🎉')
      nav('/')
    } catch (err) {
      toast.error(err.response?.data?.detail || 'Registration failed.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="auth-page">
      <div className="auth-card">
        <div className="auth-logo">
          <h1>🎓 Career Counselor</h1>
          <p>Create your account to get started</p>
          <div className="auth-ibm">Powered by IBM Granite · WatsonX.ai</div>
        </div>
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label className="form-label">Full Name</label>
            <input className="form-input" required value={form.full_name}
              onChange={e => setForm({ ...form, full_name: e.target.value })} placeholder="Priya Sharma" />
          </div>
          <div className="form-group">
            <label className="form-label">Email</label>
            <input className="form-input" type="email" required value={form.email}
              onChange={e => setForm({ ...form, email: e.target.value })} placeholder="you@university.edu" />
          </div>
          <div className="form-row">
            <div className="form-group">
              <label className="form-label">Password</label>
              <input className="form-input" type="password" required value={form.password}
                onChange={e => setForm({ ...form, password: e.target.value })} placeholder="••••••••" />
            </div>
            <div className="form-group">
              <label className="form-label">Confirm Password</label>
              <input className="form-input" type="password" required value={form.confirm}
                onChange={e => setForm({ ...form, confirm: e.target.value })} placeholder="••••••••" />
            </div>
          </div>
          <button className="btn btn-primary" style={{ width: '100%', justifyContent: 'center' }} disabled={loading}>
            {loading ? <span className="spinner" /> : 'Create Account'}
          </button>
        </form>
        <p style={{ textAlign: 'center', marginTop: '16px', fontSize: '0.85rem', color: 'var(--text-muted)' }}>
          Already have an account? <Link to="/login">Sign in</Link>
        </p>
      </div>
    </div>
  )
}
