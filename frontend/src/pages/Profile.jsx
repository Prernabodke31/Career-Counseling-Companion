import { useEffect, useState } from 'react'
import api from '../api'
import toast from 'react-hot-toast'

const INTERESTS = ['Technology', 'Healthcare', 'Business', 'Arts & Design', 'Engineering', 'Science', 'Law', 'Education', 'Finance', 'Social Work', 'Sports', 'Environment']
const SKILLS = ['Python', 'Java', 'JavaScript', 'SQL', 'Machine Learning', 'Data Analysis', 'Communication', 'Leadership', 'Project Management', 'Design (UI/UX)', 'Research', 'Public Speaking']

export default function Profile() {
  const [profile, setProfile] = useState(null)
  const [form, setForm] = useState({})
  const [newRecord, setNewRecord] = useState({ subject: '', grade: '', score: '', semester: '', academic_year: '' })
  const [saving, setSaving] = useState(false)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    api.get('/students/me').then(({ data }) => {
      setProfile(data)
      setForm({
        grade_level: data.grade_level || '',
        field_of_study: data.field_of_study || '',
        gpa: data.gpa || '',
        interests: data.interests || [],
        skills: data.skills || [],
        extracurriculars: data.extracurriculars || [],
        preferred_work_style: data.preferred_work_style || 'flexible',
        location_preference: data.location_preference || '',
        bio: data.bio || '',
      })
    }).finally(() => setLoading(false))
  }, [])

  const toggleItem = (field, item) => {
    setForm(f => ({
      ...f,
      [field]: f[field].includes(item) ? f[field].filter(x => x !== item) : [...f[field], item],
    }))
  }

  const saveProfile = async () => {
    setSaving(true)
    try {
      await api.put('/students/me', { ...form, gpa: form.gpa ? parseFloat(form.gpa) : null })
      toast.success('Profile saved!')
    } catch { toast.error('Failed to save profile.') }
    finally { setSaving(false) }
  }

  const addRecord = async (e) => {
    e.preventDefault()
    try {
      await api.post('/students/me/academic-records', {
        ...newRecord, score: newRecord.score ? parseFloat(newRecord.score) : null,
      })
      toast.success('Record added!')
      setNewRecord({ subject: '', grade: '', score: '', semester: '', academic_year: '' })
      const { data } = await api.get('/students/me')
      setProfile(data)
    } catch { toast.error('Failed to add record.') }
  }

  const deleteRecord = async (id) => {
    try {
      await api.delete(`/students/me/academic-records/${id}`)
      toast.success('Record removed.')
      const { data } = await api.get('/students/me')
      setProfile(data)
    } catch { toast.error('Failed to delete.') }
  }

  if (loading) return <div className="page-content"><span className="spinner" /></div>

  return (
    <div className="page-content">
      <div className="section-header">
        <h2 className="section-title">My Profile</h2>
        <button className="btn btn-primary btn-sm" onClick={saveProfile} disabled={saving}>
          {saving ? <span className="spinner" /> : 'Save Profile'}
        </button>
      </div>

      {/* Basic Info */}
      <div className="card" style={{ marginBottom: 16 }}>
        <div className="card-title">Academic Information</div>
        <div className="form-row">
          <div className="form-group">
            <label className="form-label">Grade / Year Level</label>
            <input className="form-input" value={form.grade_level}
              onChange={e => setForm({ ...form, grade_level: e.target.value })}
              placeholder="e.g. 12th Grade / Undergrad Year 2" />
          </div>
          <div className="form-group">
            <label className="form-label">Field of Study</label>
            <input className="form-input" value={form.field_of_study}
              onChange={e => setForm({ ...form, field_of_study: e.target.value })}
              placeholder="e.g. Computer Science" />
          </div>
        </div>
        <div className="form-row">
          <div className="form-group">
            <label className="form-label">GPA / CGPA</label>
            <input className="form-input" type="number" step="0.01" min="0" max="10" value={form.gpa}
              onChange={e => setForm({ ...form, gpa: e.target.value })} placeholder="e.g. 8.5" />
          </div>
          <div className="form-group">
            <label className="form-label">Location Preference</label>
            <input className="form-input" value={form.location_preference}
              onChange={e => setForm({ ...form, location_preference: e.target.value })}
              placeholder="e.g. Bangalore, Remote" />
          </div>
        </div>
        <div className="form-group">
          <label className="form-label">Preferred Work Style</label>
          <select className="form-select" value={form.preferred_work_style}
            onChange={e => setForm({ ...form, preferred_work_style: e.target.value })}>
            <option value="remote">Remote</option>
            <option value="hybrid">Hybrid</option>
            <option value="on-site">On-site</option>
            <option value="flexible">Flexible</option>
          </select>
        </div>
        <div className="form-group">
          <label className="form-label">Bio</label>
          <textarea className="form-textarea" value={form.bio}
            onChange={e => setForm({ ...form, bio: e.target.value })}
            placeholder="Tell us about yourself, your goals and aspirations..." />
        </div>
      </div>

      {/* Interests */}
      <div className="card" style={{ marginBottom: 16 }}>
        <div className="card-title">Interests <span style={{ fontWeight: 400, fontSize: '0.8rem', color: 'var(--text-muted)' }}>(select all that apply)</span></div>
        <div className="tags-wrap">
          {INTERESTS.map(item => (
            <button key={item} onClick={() => toggleItem('interests', item)}
              className="tag" style={{
                cursor: 'pointer', border: 'none',
                background: form.interests?.includes(item) ? 'var(--ibm-blue)' : 'var(--ibm-blue-light)',
                color: form.interests?.includes(item) ? '#fff' : 'var(--ibm-blue-dark)',
              }}>
              {item}
            </button>
          ))}
        </div>
      </div>

      {/* Skills */}
      <div className="card" style={{ marginBottom: 16 }}>
        <div className="card-title">Skills <span style={{ fontWeight: 400, fontSize: '0.8rem', color: 'var(--text-muted)' }}>(select all that apply)</span></div>
        <div className="tags-wrap">
          {SKILLS.map(item => (
            <button key={item} onClick={() => toggleItem('skills', item)}
              className="tag tag-purple" style={{
                cursor: 'pointer', border: 'none',
                background: form.skills?.includes(item) ? 'var(--ibm-purple)' : '#e8daff',
                color: form.skills?.includes(item) ? '#fff' : 'var(--ibm-purple)',
              }}>
              {item}
            </button>
          ))}
        </div>
      </div>

      {/* Academic Records */}
      <div className="card" style={{ marginBottom: 16 }}>
        <div className="card-title">Academic Records</div>
        <div style={{ overflowX: 'auto' }}>
          <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: '0.85rem' }}>
            <thead>
              <tr style={{ borderBottom: '1px solid var(--border)', textAlign: 'left' }}>
                {['Subject', 'Grade', 'Score', 'Semester', 'Year', ''].map(h => (
                  <th key={h} style={{ padding: '8px 10px', color: 'var(--text-muted)', fontWeight: 500 }}>{h}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {profile?.academic_records?.map(r => (
                <tr key={r.id} style={{ borderBottom: '1px solid var(--border)' }}>
                  <td style={{ padding: '8px 10px' }}>{r.subject}</td>
                  <td style={{ padding: '8px 10px' }}><span className="badge badge-blue">{r.grade}</span></td>
                  <td style={{ padding: '8px 10px' }}>{r.score ?? '—'}</td>
                  <td style={{ padding: '8px 10px' }}>{r.semester}</td>
                  <td style={{ padding: '8px 10px' }}>{r.academic_year}</td>
                  <td style={{ padding: '8px 10px' }}>
                    <button className="btn btn-danger btn-sm" onClick={() => deleteRecord(r.id)}>✕</button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
          {!profile?.academic_records?.length && (
            <p style={{ padding: '16px', color: 'var(--text-muted)', textAlign: 'center', fontSize: '0.85rem' }}>
              No academic records yet. Add your subjects below.
            </p>
          )}
        </div>

        {/* Add Record Form */}
        <hr className="divider" />
        <div className="card-title" style={{ marginBottom: 12 }}>Add New Record</div>
        <form onSubmit={addRecord}>
          <div className="form-row">
            <div className="form-group">
              <label className="form-label">Subject *</label>
              <input className="form-input" required value={newRecord.subject}
                onChange={e => setNewRecord({ ...newRecord, subject: e.target.value })} placeholder="e.g. Mathematics" />
            </div>
            <div className="form-group">
              <label className="form-label">Grade</label>
              <input className="form-input" value={newRecord.grade}
                onChange={e => setNewRecord({ ...newRecord, grade: e.target.value })} placeholder="A / A+ / 90" />
            </div>
          </div>
          <div className="form-row">
            <div className="form-group">
              <label className="form-label">Score (0–100)</label>
              <input className="form-input" type="number" value={newRecord.score}
                onChange={e => setNewRecord({ ...newRecord, score: e.target.value })} placeholder="85" />
            </div>
            <div className="form-group">
              <label className="form-label">Semester</label>
              <input className="form-input" value={newRecord.semester}
                onChange={e => setNewRecord({ ...newRecord, semester: e.target.value })} placeholder="Sem 3" />
            </div>
          </div>
          <div className="form-group">
            <label className="form-label">Academic Year</label>
            <input className="form-input" value={newRecord.academic_year}
              onChange={e => setNewRecord({ ...newRecord, academic_year: e.target.value })} placeholder="2024-25" />
          </div>
          <button type="submit" className="btn btn-secondary btn-sm">+ Add Record</button>
        </form>
      </div>
    </div>
  )
}
