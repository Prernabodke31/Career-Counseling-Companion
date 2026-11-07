import { useEffect, useState } from 'react'
import api from '../api'

export default function Market() {
  const [market, setMarket] = useState(null)
  const [jobs, setJobs] = useState([])
  const [search, setSearch] = useState({ role: 'Software Engineer', location: 'Remote' })
  const [jobLoading, setJobLoading] = useState(false)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    api.get('/market/overview').then(({ data }) => setMarket(data)).finally(() => setLoading(false))
  }, [])

  const searchJobs = async (e) => {
    e?.preventDefault()
    setJobLoading(true)
    try {
      const { data } = await api.get('/market/jobs', { params: search })
      setJobs(data.listings || [])
    } finally { setJobLoading(false) }
  }

  if (loading) return <div className="page-content"><span className="spinner" /></div>

  return (
    <div className="page-content">
      <h2 className="section-title" style={{ marginBottom: 20 }}>Labor Market Intelligence</h2>

      {/* Source Badge */}
      <div className="alert alert-info" style={{ marginBottom: 20 }}>
        📡 Data source: <strong>{market?.source}</strong> · Last updated: {market?.last_updated}
      </div>

      {/* Market Sentiment */}
      <div className="stat-grid" style={{ marginBottom: 20 }}>
        <div className="stat-card" style={{ gridColumn: 'span 2' }}>
          <div className="stat-label">Market Sentiment</div>
          <div style={{ fontSize: '1rem', fontWeight: 600, color: 'var(--ibm-green)', marginTop: 4 }}>
            {market?.sentiment}
          </div>
        </div>
        {Object.entries(market?.growth_rates || {}).slice(0, 3).map(([sector, rate]) => (
          <div key={sector} className="stat-card">
            <div className="stat-value" style={{ fontSize: '1.4rem' }}>{parseInt(rate)}%</div>
            <div className="stat-label">{sector} growth</div>
          </div>
        ))}
      </div>

      {/* Top Skills */}
      <div className="card" style={{ marginBottom: 16 }}>
        <div className="card-title">🔧 Top Skills in Demand</div>
        <div className="tags-wrap">
          {(market?.top_skills_in_demand || []).map(s => <span key={s} className="tag">{s}</span>)}
        </div>
      </div>

      {/* Salary Ranges */}
      <div className="card" style={{ marginBottom: 16 }}>
        <div className="card-title">💰 Salary Ranges by Role</div>
        <div style={{ overflowX: 'auto' }}>
          <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: '0.85rem' }}>
            <thead>
              <tr style={{ borderBottom: '1px solid var(--border)', textAlign: 'left' }}>
                {['Role', 'Min Salary', 'Max Salary', 'Currency'].map(h => (
                  <th key={h} style={{ padding: '8px 10px', color: 'var(--text-muted)', fontWeight: 500 }}>{h}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {Object.entries(market?.salary_ranges || {}).map(([role, s]) => (
                <tr key={role} style={{ borderBottom: '1px solid var(--border)' }}>
                  <td style={{ padding: '8px 10px', fontWeight: 500 }}>{role}</td>
                  <td style={{ padding: '8px 10px', color: 'var(--ibm-green)' }}>${s.min.toLocaleString()}</td>
                  <td style={{ padding: '8px 10px', color: 'var(--ibm-blue)' }}>${s.max.toLocaleString()}</td>
                  <td style={{ padding: '8px 10px', color: 'var(--text-muted)' }}>{s.currency}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Top Hiring Companies */}
      <div className="card" style={{ marginBottom: 16 }}>
        <div className="card-title">🏢 Top Hiring Companies</div>
        <div className="tags-wrap">
          {(market?.top_hiring_companies || []).map(c => <span key={c} className="tag tag-teal">{c}</span>)}
        </div>
      </div>

      {/* Job Search */}
      <div className="card">
        <div className="card-title">🔍 Live Job Search</div>
        <form onSubmit={searchJobs} style={{ display: 'flex', gap: 10, marginBottom: 16, flexWrap: 'wrap' }}>
          <input className="form-input" style={{ flex: 1, minWidth: 200 }} placeholder="Role (e.g. Data Scientist)"
            value={search.role} onChange={e => setSearch({ ...search, role: e.target.value })} />
          <input className="form-input" style={{ flex: 1, minWidth: 160 }} placeholder="Location / Remote"
            value={search.location} onChange={e => setSearch({ ...search, location: e.target.value })} />
          <button type="submit" className="btn btn-primary btn-sm" disabled={jobLoading}>
            {jobLoading ? <span className="spinner" /> : 'Search Jobs'}
          </button>
        </form>
        {jobs.length > 0 && (
          <div style={{ display: 'flex', flexDirection: 'column', gap: 10 }}>
            {jobs.map((job, i) => (
              <div key={i} style={{
                padding: 12, background: 'var(--surface-1)', borderRadius: 6,
                border: '1px solid var(--border)', display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start',
              }}>
                <div>
                  <div style={{ fontWeight: 600, fontSize: '0.9rem' }}>{job.title}</div>
                  <div style={{ fontSize: '0.8rem', color: 'var(--text-muted)', marginTop: 2 }}>
                    {job.company} · {job.location} {job.salary ? `· ${job.salary}` : ''}
                  </div>
                </div>
                {job.url && (
                  <a href={job.url} target="_blank" rel="noreferrer" className="btn btn-secondary btn-sm">
                    Apply →
                  </a>
                )}
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}
