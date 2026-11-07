import { useEffect, useState } from 'react'
import { useAuth } from '../AuthContext'
import api from '../api'
import toast from 'react-hot-toast'

export default function Dashboard() {
  const { user } = useAuth()
  const [profile, setProfile] = useState(null)
  const [market, setMarket] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    Promise.all([
      api.get('/students/me').catch(() => null),
      api.get('/market/overview').catch(() => null),
    ]).then(([p, m]) => {
      if (p) setProfile(p.data)
      if (m) setMarket(m.data)
    }).finally(() => setLoading(false))
  }, [])

  const completeness = profile ? (() => {
    let score = 0
    if (profile.grade_level) score += 20
    if (profile.field_of_study) score += 20
    if (profile.gpa) score += 15
    if (profile.interests?.length) score += 15
    if (profile.skills?.length) score += 15
    if (profile.academic_records?.length) score += 15
    return score
  })() : 0

  if (loading) return (
    <div className="page-content" style={{ display: 'flex', justifyContent: 'center', paddingTop: 80 }}>
      <span className="spinner" style={{ width: 36, height: 36 }} />
    </div>
  )

  return (
    <div className="page-content">
      {/* Welcome Banner */}
      <div className="card" style={{ background: 'linear-gradient(135deg, #001141, #0f3460)', color: '#fff', marginBottom: 24, border: 'none' }}>
        <h2 style={{ fontSize: '1.25rem', marginBottom: 6 }}>
          Welcome back, {user?.name?.split(' ')[0]} 👋
        </h2>
        <p style={{ opacity: 0.85, fontSize: '0.875rem' }}>
          Your AI career counselor is ready. IBM Granite is analyzing your profile to surface the best opportunities.
        </p>
      </div>

      {/* Stats Grid */}
      <div className="stat-grid">
        <div className="stat-card">
          <div className="stat-value">{profile?.academic_records?.length || 0}</div>
          <div className="stat-label">Academic Records</div>
        </div>
        <div className="stat-card">
          <div className="stat-value">{profile?.gpa ?? '—'}</div>
          <div className="stat-label">Current GPA</div>
        </div>
        <div className="stat-card">
          <div className="stat-value">{profile?.interests?.length || 0}</div>
          <div className="stat-label">Interests Added</div>
        </div>
        <div className="stat-card">
          <div className="stat-value">{profile?.skills?.length || 0}</div>
          <div className="stat-label">Skills Logged</div>
        </div>
      </div>

      {/* Profile Completeness */}
      <div className="card" style={{ marginBottom: 24 }}>
        <div className="section-header">
          <span className="card-title">Profile Completeness</span>
          <span className="badge badge-blue">{completeness}%</span>
        </div>
        <div className="progress-bar">
          <div className="progress-fill" style={{ width: `${completeness}%` }} />
        </div>
        <p style={{ fontSize: '0.8rem', color: 'var(--text-muted)', marginTop: 8 }}>
          {completeness < 100
            ? 'Complete your profile to get more accurate career recommendations from IBM Granite.'
            : 'Great! Your profile is fully set up.'}
        </p>
      </div>

      {/* Hot Skills & Top Roles */}
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 16, marginBottom: 24 }}>
        <div className="card">
          <div className="card-title">🔥 Top Skills in Demand</div>
          <div className="tags-wrap">
            {(market?.top_skills_in_demand || []).slice(0, 8).map(s => (
              <span key={s} className="tag">{s}</span>
            ))}
          </div>
        </div>
        <div className="card">
          <div className="card-title">📈 High-Demand Roles</div>
          <div className="tags-wrap">
            {(market?.hot_roles || []).slice(0, 8).map(r => (
              <span key={r} className="tag tag-purple">{r}</span>
            ))}
          </div>
        </div>
      </div>

      {/* Growth Rates */}
      <div className="card">
        <div className="card-title">📊 Sector Growth Outlook</div>
        <div style={{ display: 'flex', flexDirection: 'column', gap: 10, marginTop: 8 }}>
          {Object.entries(market?.growth_rates || {}).map(([sector, rate]) => (
            <div key={sector}>
              <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 4 }}>
                <span style={{ fontSize: '0.85rem' }}>{sector}</span>
                <span className="badge badge-green">{rate}</span>
              </div>
              <div className="progress-bar">
                <div className="progress-fill" style={{ width: `${parseInt(rate) * 2}%`, background: 'var(--ibm-teal)' }} />
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}
