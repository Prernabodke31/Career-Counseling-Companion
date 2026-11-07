import { useState, useEffect } from 'react'
import api from '../api'
import toast from 'react-hot-toast'

const TYPES = ['interest', 'aptitude', 'personality']

export default function Assessment() {
  const [activeType, setActiveType] = useState('interest')
  const [questions, setQuestions] = useState([])
  const [responses, setResponses] = useState({})
  const [submitting, setSubmitting] = useState(false)
  const [result, setResult] = useState(null)
  const [history, setHistory] = useState([])

  useEffect(() => {
    api.get(`/assessment/questions/${activeType}`).then(({ data }) => {
      setQuestions(data.questions || [])
      setResponses({})
      setResult(null)
    })
    api.get('/assessment/history').then(({ data }) => setHistory(data))
  }, [activeType])

  const handleSubmit = async () => {
    const unanswered = questions.filter(q => !responses[q.id])
    if (unanswered.length) { toast.error(`Please answer all ${unanswered.length} remaining questions.`); return }
    setSubmitting(true)
    try {
      const { data } = await api.post('/assessment/submit', {
        assessment_type: activeType,
        responses,
      })
      setResult(data)
      toast.success('Assessment completed!')
      const hist = await api.get('/assessment/history')
      setHistory(hist.data)
    } catch { toast.error('Submission failed.') }
    finally { setSubmitting(false) }
  }

  const scaleLabels = ['Strongly Disagree', 'Disagree', 'Neutral', 'Agree', 'Strongly Agree']

  return (
    <div className="page-content">
      <div className="section-header">
        <h2 className="section-title">Self Assessments</h2>
      </div>

      <div className="alert alert-info" style={{ marginBottom: 16 }}>
        Complete all three assessments (Interest, Aptitude, Personality) for the most accurate IBM Granite recommendations.
      </div>

      {/* Type Tabs */}
      <div style={{ display: 'flex', gap: 8, marginBottom: 20 }}>
        {TYPES.map(t => (
          <button key={t} onClick={() => setActiveType(t)}
            className={`btn ${activeType === t ? 'btn-primary' : 'btn-secondary'}`}>
            {t.charAt(0).toUpperCase() + t.slice(1)} Assessment
          </button>
        ))}
      </div>

      {/* Questions */}
      <div className="card" style={{ marginBottom: 20 }}>
        <div className="card-title">
          {activeType.charAt(0).toUpperCase() + activeType.slice(1)} Assessment
          <span style={{ fontWeight: 400, fontSize: '0.8rem', color: 'var(--text-muted)', marginLeft: 8 }}>
            ({Object.keys(responses).length}/{questions.length} answered)
          </span>
        </div>
        {questions.map((q, idx) => (
          <div key={q.id} style={{ marginBottom: 20, padding: '12px 0', borderBottom: '1px solid var(--border)' }}>
            <p style={{ fontWeight: 500, marginBottom: 10, fontSize: '0.9rem' }}>
              {idx + 1}. {q.question}
            </p>
            <div style={{ display: 'flex', gap: 8, flexWrap: 'wrap' }}>
              {[1, 2, 3, 4, 5].map(val => (
                <button key={val} onClick={() => setResponses({ ...responses, [q.id]: val })}
                  style={{
                    padding: '6px 14px', borderRadius: 20, fontSize: '0.78rem',
                    border: '1px solid var(--border)',
                    background: responses[q.id] === val ? 'var(--ibm-blue)' : 'var(--surface-1)',
                    color: responses[q.id] === val ? '#fff' : 'var(--text-primary)',
                    cursor: 'pointer', fontFamily: 'inherit',
                    transition: 'all 0.15s',
                  }}>
                  {val} — {scaleLabels[val - 1]}
                </button>
              ))}
            </div>
          </div>
        ))}
        <button className="btn btn-primary" onClick={handleSubmit} disabled={submitting}>
          {submitting ? <span className="spinner" /> : 'Submit Assessment'}
        </button>
      </div>

      {/* Result */}
      {result && (
        <div className="card alert-success" style={{ marginBottom: 20 }}>
          <div className="card-title">✅ Assessment Results</div>
          <p style={{ marginBottom: 12 }}>{result.summary}</p>
          <div className="tags-wrap">
            {Object.entries(result.scores || {}).map(([dim, score]) => (
              <span key={dim} className="tag tag-green" style={{ fontSize: '0.8rem' }}>
                {dim}: {score}
              </span>
            ))}
          </div>
        </div>
      )}

      {/* History */}
      <div className="card">
        <div className="card-title">Assessment History</div>
        {history.length === 0
          ? <p style={{ color: 'var(--text-muted)', fontSize: '0.85rem' }}>No assessments taken yet.</p>
          : history.map(a => (
            <div key={a.id} style={{ padding: '10px 0', borderBottom: '1px solid var(--border)' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 6 }}>
                <span className="badge badge-blue">{a.type}</span>
                <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>
                  {new Date(a.taken_at).toLocaleDateString()}
                </span>
              </div>
              <p style={{ fontSize: '0.82rem', color: 'var(--text-secondary)' }}>{a.summary}</p>
            </div>
          ))
        }
      </div>
    </div>
  )
}
