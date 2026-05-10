import { useState, useRef } from 'react'
import type { Entry, ExploreTurn, Reflection } from '../types'
import { streamSSE, exploreMessage } from '../lib/api'

const MAX_EXPLORE_TURNS = 3

type Phase     = 'reading' | 'reflected' | 'exploring'
type AiMode    = 'reflect' | 'socratic'

type ReflectionViewProps = {
  entry: Entry
  onBack: () => void
  onComplete: (reflection: Reflection) => void
}

export default function ReflectionView({ entry, onBack, onComplete }: ReflectionViewProps) {
  const [phase, setPhase]               = useState<Phase>('reading')
  const [aiMode, setAiMode]             = useState<AiMode>('reflect')
  const [showContext, setShowContext]   = useState(false)
  const [answer, setAnswer]             = useState('')
  const [savedAnswer, setSavedAnswer]   = useState('')
  const [aiResponse, setAiResponse]     = useState('')
  const [isStreaming, setIsStreaming]   = useState(false)
  const [exploreTurns, setExploreTurns] = useState<ExploreTurn[]>([])
  const [exploreInput, setExploreInput] = useState('')
  const [exploreLoading, setExploreLoading] = useState(false)
  const responseRef = useRef<HTMLDivElement>(null)

  async function handleSubmitAnswer() {
    if (!answer.trim()) return
    const trimmed = answer.trim()
    setSavedAnswer(trimmed)
    setIsStreaming(true)
    setAiResponse('')
    setPhase('reflected')

    const endpoint = aiMode === 'socratic' ? '/api/socratic' : '/api/reflect'
    await streamSSE(endpoint, {
      proverb: entry.proverb,
      question: entry.question,
      answer: trimmed,
    }, chunk => {
      setAiResponse(prev => prev + chunk)
      responseRef.current?.scrollIntoView({ behavior: 'smooth', block: 'end' })
    })
    setIsStreaming(false)
  }

  async function handleExploreSubmit() {
    if (!exploreInput.trim() || exploreLoading) return
    const msg = exploreInput.trim()
    setExploreInput('')
    setExploreLoading(true)
    const reply = await exploreMessage({
      proverb:            entry.proverb,
      question:           entry.question,
      original_answer:    savedAnswer,
      evaluator_feedback: aiResponse,
      explore_history:    exploreTurns,
      user_message:       msg,
    })
    setExploreTurns(prev => [...prev, { user: msg, ai: reply }])
    setExploreLoading(false)
  }

  function handleSaveAndNext() {
    onComplete({
      theme:           entry.theme,
      culture:         entry.culture,
      proverb:         entry.proverb,
      question:        entry.question,
      user_reflection: savedAnswer,
      ai_response:     aiResponse,
      timestamp:       new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
      explore_turns:   exploreTurns.length ? exploreTurns : undefined,
    })
  }

  const isSocratic = aiMode === 'socratic'

  return (
    <div style={{ minHeight: '100vh', padding: '88px 24px 60px' }}>
      <div style={{ maxWidth: 680, margin: '0 auto' }}>

        {/* Back + labels */}
        <div style={{ display: 'flex', alignItems: 'center', gap: 10, marginBottom: 24, flexWrap: 'wrap' }}>
          <button className="btn btn-white" style={{ padding: '7px 14px', fontSize: 13 }} onClick={onBack}>
            ← Themes
          </button>
          <span className="pill-label pill-mint">{entry.theme}</span>
          <span className="pill-label pill-cream">{entry.culture}</span>
        </div>

        {/* Proverb card */}
        <div style={{
          background: 'var(--parchment-dk)',
          border: 'var(--border)',
          borderRadius: 'var(--radius)',
          boxShadow: 'var(--shadow)',
          padding: '32px 36px',
          textAlign: 'center',
          marginBottom: 12,
        }}>
          <p className="proverb-text">"{entry.proverb}"</p>
        </div>

        {/* Cultural context toggle */}
        {entry.context && (
          <div style={{ marginBottom: 24 }}>
            <button
              onClick={() => setShowContext(v => !v)}
              style={{
                background: 'none',
                border: 'none',
                cursor: 'pointer',
                fontSize: 12,
                fontWeight: 700,
                letterSpacing: '0.08em',
                textTransform: 'uppercase',
                color: 'var(--sage)',
                padding: '4px 0',
                display: 'flex',
                alignItems: 'center',
                gap: 6,
              }}
            >
              {showContext ? '▲' : '▼'} About this tradition
            </button>
            {showContext && (
              <div style={{
                marginTop: 10,
                padding: '14px 18px',
                background: 'rgba(95,122,107,0.08)',
                borderLeft: '3px solid var(--sage)',
                borderRadius: '0 10px 10px 0',
                fontFamily: "'Lora', serif",
                fontSize: 14,
                lineHeight: 1.75,
                color: 'var(--ink-muted)',
              }}>
                {entry.context}
              </div>
            )}
          </div>
        )}

        {/* Question */}
        <p style={{
          fontFamily: "'Lora', serif",
          fontWeight: 600,
          fontSize: 18,
          color: 'var(--ink)',
          lineHeight: 1.55,
          marginBottom: 24,
        }}>
          {entry.question}
        </p>

        {/* PHASE: reading */}
        {phase === 'reading' && (
          <div>
            {/* Mode toggle */}
            <div style={{ marginBottom: 14, display: 'flex', alignItems: 'center', gap: 12, flexWrap: 'wrap' }}>
              <div className="mode-toggle">
                <button
                  className={aiMode === 'reflect' ? 'active' : ''}
                  onClick={() => setAiMode('reflect')}
                >
                  🪞 Reflect freely
                </button>
                <button
                  className={aiMode === 'socratic' ? 'active-sage' : ''}
                  onClick={() => setAiMode('socratic')}
                >
                  🏛️ Challenge me
                </button>
              </div>
              <span style={{ fontSize: 12, color: 'var(--ink-muted)', fontStyle: 'italic' }}>
                {aiMode === 'reflect'
                  ? 'AI will reflect warmly on what you share'
                  : 'AI will gently question your assumptions'}
              </span>
            </div>

            <textarea
              className="wisdom-input"
              placeholder="There's no right answer here — share what comes to mind."
              value={answer}
              onChange={e => setAnswer(e.target.value)}
              rows={5}
            />
            <button
              className="btn btn-peach"
              onClick={handleSubmitAnswer}
              disabled={!answer.trim()}
              style={{ marginTop: 14, width: '100%', justifyContent: 'center' }}
            >
              {isSocratic ? 'Submit for Socratic dialogue →' : 'Reflect →'}
            </button>
          </div>
        )}

        {/* PHASE: reflected / exploring */}
        {(phase === 'reflected' || phase === 'exploring') && (
          <div>
            {/* User's reflection */}
            <div style={{
              background: 'var(--paper)',
              border: 'var(--border)',
              borderRadius: 'var(--radius)',
              padding: '16px 20px',
              marginBottom: 14,
              fontSize: 16,
              lineHeight: 1.7,
              fontFamily: "'Lora', serif",
            }}>
              {savedAnswer}
            </div>

            {/* AI response — different card style per mode */}
            <div ref={responseRef}>
              {(aiResponse || isStreaming) && (
                <div
                  className={isSocratic ? 'ai-card-socratic' : 'ai-card'}
                  style={{ marginBottom: 14, position: 'relative' }}
                >
                  {isSocratic && (
                    <span style={{
                      display: 'inline-block',
                      fontSize: 10, fontWeight: 800,
                      letterSpacing: '0.1em', textTransform: 'uppercase',
                      color: 'var(--sage)', marginBottom: 8,
                    }}>
                      Socratic challenge
                    </span>
                  )}
                  <div>
                    {aiResponse || <span style={{ opacity: 0.4, fontStyle: 'italic' }}>Thinking…</span>}
                    {isStreaming && aiResponse && <span style={{ opacity: 0.35 }}>▍</span>}
                  </div>
                </div>
              )}
            </div>

            {/* Explore deeper conversation */}
            {phase === 'exploring' && !isStreaming && (
              <div style={{ marginTop: 8 }}>
                <div style={{ display: 'flex', flexDirection: 'column', gap: 12, marginBottom: 16 }}>
                  {exploreTurns.map((turn, i) => (
                    <div key={i}>
                      <div style={{
                        background: 'var(--paper)',
                        border: 'var(--border)',
                        borderRadius: 'var(--radius)',
                        padding: '12px 18px',
                        fontSize: 15,
                        fontFamily: "'Lora', serif",
                        marginBottom: 8,
                      }}>
                        {turn.user}
                      </div>
                      <div className="ai-card">{turn.ai}</div>
                    </div>
                  ))}
                </div>

                {exploreTurns.length < MAX_EXPLORE_TURNS ? (
                  <div>
                    <textarea
                      className="wisdom-input"
                      placeholder="Keep exploring…"
                      value={exploreInput}
                      onChange={e => setExploreInput(e.target.value)}
                      rows={3}
                      style={{ minHeight: 80 }}
                    />
                    <button
                      className="btn btn-mint"
                      style={{ marginTop: 12 }}
                      onClick={handleExploreSubmit}
                      disabled={!exploreInput.trim() || exploreLoading}
                    >
                      {exploreLoading ? 'Thinking…' : 'Continue →'}
                    </button>
                  </div>
                ) : (
                  <p style={{
                    fontFamily: "'Lora', serif",
                    fontStyle: 'italic',
                    color: 'var(--ink-muted)',
                    fontSize: 15,
                    textAlign: 'center',
                    padding: '16px 0',
                  }}>
                    You've explored this deeply. ✦
                  </p>
                )}
              </div>
            )}

            {/* Action buttons */}
            {!isStreaming && (
              <div style={{ display: 'flex', gap: 10, marginTop: 28, flexWrap: 'wrap' }}>
                {phase === 'reflected' && (
                  <button
                    className="btn btn-white"
                    onClick={() => setPhase('exploring')}
                  >
                    Explore Deeper ↓
                  </button>
                )}
                <button className="btn btn-peach" onClick={handleSaveAndNext}>
                  Save & Choose Another →
                </button>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  )
}
