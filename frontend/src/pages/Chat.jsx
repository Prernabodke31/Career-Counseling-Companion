import { useState, useEffect, useRef } from 'react'
import api from '../api'
import { useAuth } from '../AuthContext'
import ReactMarkdown from 'react-markdown'

export default function Chat() {
  const { user } = useAuth()
  const [messages, setMessages] = useState([])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const [loadingHistory, setLoadingHistory] = useState(true)
  const bottomRef = useRef(null)

  useEffect(() => {
    api.get('/career/chat/history').then(({ data }) => {
      setMessages(data.messages || [])
    }).finally(() => setLoadingHistory(false))
  }, [])

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  const sendMessage = async (e) => {
    e?.preventDefault()
    if (!input.trim() || loading) return

    const userMsg = { role: 'user', content: input, timestamp: new Date().toISOString() }
    setMessages(prev => [...prev, userMsg])
    setInput('')
    setLoading(true)

    try {
      const { data } = await api.post('/career/chat', { content: userMsg.content })
      const aiMsg = { role: 'assistant', content: data.response, timestamp: new Date().toISOString() }
      setMessages(prev => [...prev, aiMsg])
    } catch {
      setMessages(prev => [...prev, {
        role: 'assistant',
        content: '⚠️ Sorry, I encountered an error. Please try again.',
        timestamp: new Date().toISOString(),
      }])
    } finally {
      setLoading(false)
    }
  }

  const STARTERS = [
    "What career paths match my academic profile?",
    "Which certifications should I pursue in tech?",
    "How do I transition from engineering to data science?",
    "What are the highest paying careers in 2025?",
    "Help me prepare for a software engineering interview",
  ]

  return (
    <div className="page-content" style={{ maxWidth: 800 }}>
      <div className="section-header">
        <h2 className="section-title">AI Career Counselor Chat</h2>
        <span className="badge badge-blue" style={{ fontSize: '0.75rem' }}>IBM Granite</span>
      </div>

      {/* Quick Starters */}
      {messages.length === 0 && !loadingHistory && (
        <div style={{ marginBottom: 16 }}>
          <p style={{ fontSize: '0.8rem', color: 'var(--text-muted)', marginBottom: 8 }}>
            💡 Try asking:
          </p>
          <div style={{ display: 'flex', flexWrap: 'wrap', gap: 6 }}>
            {STARTERS.map(s => (
              <button key={s} onClick={() => { setInput(s) }}
                style={{
                  background: 'var(--surface-0)', border: '1px solid var(--border)',
                  borderRadius: 20, padding: '5px 12px', fontSize: '0.78rem',
                  cursor: 'pointer', fontFamily: 'inherit', color: 'var(--ibm-blue)',
                }}>
                {s}
              </button>
            ))}
          </div>
        </div>
      )}

      <div className="chat-container">
        <div className="chat-messages">
          {loadingHistory && (
            <div style={{ textAlign: 'center', padding: 20 }}><span className="spinner" /></div>
          )}

          {!loadingHistory && messages.length === 0 && (
            <div style={{ textAlign: 'center', padding: 40 }}>
              <div style={{ fontSize: '2rem', marginBottom: 8 }}>🤖</div>
              <p style={{ color: 'var(--text-muted)', fontSize: '0.9rem' }}>
                Hi {user?.name?.split(' ')[0]}! I'm your IBM Granite-powered career counselor.<br />
                Ask me anything about careers, skills, or your professional future.
              </p>
            </div>
          )}

          {messages.map((msg, i) => (
            <div key={i} style={{ display: 'flex', flexDirection: 'column',
              alignItems: msg.role === 'user' ? 'flex-end' : 'flex-start' }}>
              <div className={`chat-bubble ${msg.role}`}>
                {msg.role === 'assistant'
                  ? <ReactMarkdown>{msg.content}</ReactMarkdown>
                  : msg.content}
              </div>
              <span style={{ fontSize: '0.68rem', color: 'var(--text-muted)', margin: '2px 4px' }}>
                {msg.role === 'user' ? 'You' : '🤖 IBM Granite'} · {new Date(msg.timestamp).toLocaleTimeString()}
              </span>
            </div>
          ))}

          {loading && (
            <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
              <div className="chat-bubble assistant">
                <span className="spinner" style={{ width: 16, height: 16, borderWidth: 2 }} />
              </div>
            </div>
          )}

          <div ref={bottomRef} />
        </div>

        <form className="chat-input-row" onSubmit={sendMessage}>
          <input className="chat-input" value={input}
            onChange={e => setInput(e.target.value)}
            placeholder="Ask about careers, skills, opportunities..."
            disabled={loading} />
          <button type="submit" className="btn btn-primary btn-sm" disabled={loading || !input.trim()}>
            Send →
          </button>
        </form>
      </div>
    </div>
  )
}
