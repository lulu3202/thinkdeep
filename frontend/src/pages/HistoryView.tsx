import { useState } from 'react'
import type { Reflection } from '../types'
import { streamSSE } from '../lib/api'

type HistoryViewProps = {
  history: Reflection[]
  onBack: () => void
}

export default function HistoryView({ history, onBack }: HistoryViewProps) {
  const [report, setReport] = useState('')
  const [generating, setGenerating] = useState(false)
  const [expanded, setExpanded] = useState<number | null>(0)

  async function generateReport() {
    setGenerating(true)
    setReport('')
    await streamSSE('/api/report', { history }, chunk => {
      setReport(prev => prev + chunk)
    })
    setGenerating(false)
  }

  const themes = [...new Set(history.map(r => r.theme))]

  return (
    <div style={{ paddingTop: 100, minHeight: '100vh', padding: '100px 24px 60px' }}>
      <div style={{ maxWidth: 700, margin: '0 auto' }}>

        {/* Header */}
        <div style={{ marginBottom: 32 }}>
          <button className="btn btn-white" onClick={onBack} style={{ marginBottom: 20 }}>
            ← Back
          </button>
          <h2 style={{ marginBottom: 8 }}>Your Reflections</h2>
          <div style={{ display: 'flex', gap: 10, flexWrap: 'wrap', alignItems: 'center' }}>
            <span className="pill-label pill-peach">{history.length} reflection{history.length !== 1 ? 's' : ''}</span>
            {themes.map(t => (
              <span key={t} className="pill-label pill-mint">{t}</span>
            ))}
          </div>
        </div>

        {/* Reflection cards */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: 16, marginBottom: 40 }}>
          {[...history].reverse().map((r, i) => (
            <div key={i} className="card" style={{ cursor: 'pointer' }} onClick={() => setExpanded(expanded === i ? null : i)}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', gap: 12 }}>
                <div>
                  <span className="pill-label pill-mint" style={{ marginBottom: 8, display: 'inline-block' }}>{r.theme}</span>
                  <p style={{
                    fontFamily: "'Lora', serif",
                    fontStyle: 'italic',
                    fontSize: 15,
                    color: 'var(--dark)',
                    lineHeight: 1.5,
                  }}>
                    "{r.proverb.length > 80 ? r.proverb.slice(0, 80) + '…' : r.proverb}"
                  </p>
                </div>
                <span style={{ fontSize: 18, flexShrink: 0 }}>{expanded === i ? '▲' : '▼'}</span>
              </div>

              {expanded === i && (
                <div style={{ marginTop: 20, borderTop: '2px solid #eee', paddingTop: 16 }}>
                  <p style={{ fontSize: 11, fontWeight: 800, letterSpacing: '0.1em', textTransform: 'uppercase', color: '#999', marginBottom: 12 }}>
                    {r.culture} · {r.timestamp}
                  </p>
                  <p style={{ fontFamily: "'Lora', serif", fontStyle: 'italic', fontSize: 16, marginBottom: 16, lineHeight: 1.7 }}>
                    "{r.proverb}"
                  </p>
                  <p style={{ fontWeight: 700, fontSize: 13, marginBottom: 6, color: '#555' }}>{r.question}</p>

                  <div style={{
                    background: 'var(--offwhite)',
                    border: 'var(--border)',
                    borderRadius: 'var(--radius)',
                    padding: '14px 18px',
                    fontSize: 15,
                    lineHeight: 1.6,
                    marginBottom: 12,
                  }}>
                    {r.user_reflection}
                  </div>

                  <div className="ai-card">
                    {r.ai_response}
                  </div>

                  {r.explore_turns && r.explore_turns.length > 0 && (
                    <div style={{ marginTop: 16 }}>
                      <p style={{ fontSize: 11, fontWeight: 800, letterSpacing: '0.1em', textTransform: 'uppercase', color: '#999', marginBottom: 10 }}>Explore conversation</p>
                      {r.explore_turns.map((turn, ti) => (
                        <div key={ti} style={{ marginBottom: 12 }}>
                          <div style={{
                            background: 'var(--offwhite)',
                            border: 'var(--border)',
                            borderRadius: 'var(--radius)',
                            padding: '10px 16px',
                            fontSize: 14,
                            marginBottom: 6,
                          }}>
                            {turn.user}
                          </div>
                          <div className="ai-card" style={{ fontSize: 14 }}>
                            {turn.ai}
                          </div>
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              )}
            </div>
          ))}
        </div>

        {/* Summary report */}
        <div className="card-mint" style={{ marginBottom: 32 }}>
          <h3 style={{ marginBottom: 8, fontSize: '1.1rem' }}>✨ Reflection Summary</h3>
          <p style={{ fontSize: 14, color: '#5a7a76', marginBottom: 20 }}>
            A personalised insight into the themes and ideas you've explored.
          </p>

          {generating ? (
            report
              ? <div className="ai-card">{report}<span style={{ opacity: 0.4 }}>▍</span></div>
              : <p style={{ fontFamily: "'Lora', serif", fontStyle: 'italic', color: '#888', fontSize: 15 }}>Reflecting on your journey…</p>
          ) : report ? (
            <>
              <div className="ai-card">{report}</div>
              <button className="btn btn-white" style={{ marginTop: 16 }} onClick={() => { setReport(''); generateReport() }}>
                Regenerate
              </button>
            </>
          ) : (
            <button className="btn btn-peach" onClick={generateReport}>
              Generate My Summary
            </button>
          )}
        </div>

        <button className="btn btn-dark" onClick={onBack}>
          ← Explore More Wisdom
        </button>
      </div>
    </div>
  )
}
