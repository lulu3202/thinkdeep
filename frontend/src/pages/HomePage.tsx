import { useEffect, useState } from 'react'
import { fetchThemes } from '../lib/api'
import type { StreakData, DailyRecord } from '../lib/storage'
import { todayStr } from '../lib/storage'

type HomePageProps = {
  onSelectTheme: (theme: string) => void
  historyCount: number
  streak: StreakData
  daily: DailyRecord | null
  onViewHistory: () => void
  onStartDaily: () => void
}

const THEME_EMOJIS: Record<string, string> = {
  'Resilience': '🌿',
  'Patience':   '⏳',
  'Community':  '🤝',
  'Wisdom':     '✨',
  'Courage':    '🦁',
  'Gratitude':  '🌸',
  'Humility':   '🌾',
  'Justice':    '⚖️',
  'Change':     '🌊',
}

const CULTURES: { label: string; emoji: string; color: string }[] = [
  { label: 'Japanese',        emoji: '🌸', color: 'var(--peach)' },
  { label: 'African',         emoji: '🌍', color: 'var(--mint)' },
  { label: 'Chinese',         emoji: '🏮', color: 'var(--cream)' },
  { label: 'Indian',          emoji: '🌺', color: 'var(--lavender)' },
  { label: 'Ubuntu',          emoji: '🤝', color: 'var(--mint-light)' },
  { label: 'Tamil',           emoji: '🎋', color: 'var(--peach)' },
  { label: 'Zen',             emoji: '🍵', color: 'var(--cream)' },
  { label: 'Stoic',           emoji: '🏛️', color: 'var(--lavender)' },
  { label: 'Sufi',            emoji: '🌙', color: 'var(--mint)' },
  { label: 'Buddhist',        emoji: '🪷', color: 'var(--peach)' },
  { label: 'Native American', emoji: '🦅', color: 'var(--cream)' },
]

export default function HomePage({
  onSelectTheme, historyCount, streak, daily, onViewHistory, onStartDaily,
}: HomePageProps) {
  const [themes, setThemes] = useState<string[]>([])
  const reflectedToday = streak.lastDate === todayStr()

  useEffect(() => {
    fetchThemes().then(setThemes).catch(console.error)
  }, [])

  return (
    <div style={{ paddingTop: 100, minHeight: '100vh', position: 'relative' }}>

      {/* Floating deco */}
      <span className="deco" style={{ top: 120, left: '8%',  fontSize: 28, color: 'var(--peach-dark)', animationDelay: '0s'   }}>✦</span>
      <span className="deco" style={{ top: 180, right: '10%', fontSize: 20, color: 'var(--mint)',       animationDelay: '1.5s' }}>✧</span>
      <span className="deco" style={{ top: 300, left: '5%',  fontSize: 16, color: 'var(--cream)',      animationDelay: '3s',  border: '2px solid var(--dark)', borderRadius: '50%', width: 36, height: 36, display: 'flex', alignItems: 'center', justifyContent: 'center' }}>✿</span>
      <span className="deco" style={{ top: 260, right: '7%', fontSize: 32, color: 'var(--lavender)',   animationDelay: '2s'   }}>◆</span>

      {/* ── Hero ─────────────────────────────────────────────────────────── */}
      <div style={{ textAlign: 'center', padding: '0 24px 36px' }}>
        <div style={{ marginBottom: 16 }}>
          <span className="pill-label pill-peach">Wisdom · Reflection · Growth</span>
        </div>
        <h1 style={{ marginBottom: 16 }}>
          Think<span style={{ color: 'var(--peach-dark)' }}>Deep</span>
        </h1>
        <p style={{
          fontFamily: "'Lora', Georgia, serif",
          fontStyle: 'italic',
          fontSize: 'clamp(1rem, 2.5vw, 1.3rem)',
          color: '#6b5a5a',
          maxWidth: 480,
          margin: '0 auto 28px',
          lineHeight: 1.7,
        }}>
          Timeless wisdom. One proverb at a time.<br />Pause. Read. Reflect.
        </p>

        {/* Culture badges */}
        <div style={{ display: 'flex', flexWrap: 'wrap', gap: 10, justifyContent: 'center', maxWidth: 640, margin: '0 auto 32px' }}>
          {CULTURES.map(c => (
            <span key={c.label} style={{
              display: 'inline-flex', alignItems: 'center', gap: 5,
              background: c.color,
              border: '2px solid var(--dark)',
              borderRadius: 'var(--radius-pill)',
              padding: '5px 14px',
              fontSize: 13, fontWeight: 700,
              boxShadow: '2px 2px 0 var(--dark)',
              whiteSpace: 'nowrap',
            }}>
              {c.emoji} {c.label}
            </span>
          ))}
        </div>

        {historyCount > 0 && (
          <button className="btn btn-mint" onClick={onViewHistory} style={{ marginBottom: 8 }}>
            ✦ View My {historyCount} Reflection{historyCount !== 1 ? 's' : ''}
          </button>
        )}
      </div>

      {/* ── Daily Proverb card ────────────────────────────────────────────── */}
      {daily && (
        <div style={{ maxWidth: 680, margin: '0 auto 0', padding: '0 24px 48px' }}>
          <div style={{
            border: 'var(--border)',
            borderRadius: 'var(--radius)',
            overflow: 'hidden',
            boxShadow: 'var(--shadow)',
          }}>
            {/* Card header */}
            <div style={{
              background: reflectedToday ? 'var(--mint)' : 'var(--peach)',
              borderBottom: 'var(--border)',
              padding: '12px 24px',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'space-between',
            }}>
              <span style={{ fontWeight: 900, fontSize: 13, letterSpacing: '0.1em', textTransform: 'uppercase' }}>
                {reflectedToday ? '✓ Reflected today' : '✨ Today\'s Wisdom'}
              </span>
              <span style={{ fontWeight: 800, fontSize: 13 }}>
                {streak.current > 0
                  ? `🔥 ${streak.current} day streak`
                  : 'Start your streak today'}
              </span>
            </div>

            {/* Card body */}
            <div style={{ background: 'var(--white)', padding: '28px 32px' }}>
              <p style={{ fontSize: 11, fontWeight: 800, letterSpacing: '0.12em', textTransform: 'uppercase', color: '#999', marginBottom: 12 }}>
                {daily.entry.culture} · {daily.entry.theme}
              </p>
              <p style={{
                fontFamily: "'Lora', Georgia, serif",
                fontStyle: 'italic',
                fontSize: 'clamp(1.1rem, 2.5vw, 1.5rem)',
                lineHeight: 1.75,
                color: 'var(--dark)',
                marginBottom: 20,
              }}>
                "{daily.entry.proverb}"
              </p>

              {reflectedToday ? (
                <p style={{ fontFamily: "'Lora', serif", fontStyle: 'italic', color: '#6a9a96', fontSize: 15 }}>
                  Great work today. Come back tomorrow for a new one. 🌱
                </p>
              ) : (
                <button className="btn btn-peach" onClick={onStartDaily}>
                  Reflect on This →
                </button>
              )}
            </div>
          </div>
        </div>
      )}

      {/* ── How it works ─────────────────────────────────────────────────── */}
      <div style={{ background: 'var(--paper)', padding: '64px 24px', borderTop: 'var(--border)', borderBottom: 'var(--border)' }}>
        <div style={{ maxWidth: 860, margin: '0 auto' }}>
          <div style={{ textAlign: 'center', marginBottom: 48 }}>
            <span className="pill-label pill-cream" style={{ marginBottom: 16, display: 'inline-block' }}>How it works</span>
            <h2 style={{ fontSize: 'clamp(1.5rem, 3vw, 2.2rem)' }}>Four steps. One thought at a time.</h2>
          </div>

          <div style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(auto-fit, minmax(180px, 1fr))',
            gap: 0,
            alignItems: 'start',
          }}>
            {[
              {
                emoji: '📖',
                step: '01',
                title: 'Pick a proverb',
                desc: 'Choose a theme from 11 cultural traditions. A proverb surfaces. A context panel tells you where it comes from.',
              },
              {
                emoji: '✍️',
                step: '02',
                title: 'Write freely',
                desc: 'Answer the reflective question in your own words. No right answers. No grading. Just honest thinking.',
              },
              {
                emoji: '🧠',
                step: '03',
                title: 'Gemma 4 responds',
                desc: 'Choose Reflect for warmth, or Socratic to be challenged. The AI runs entirely on your device — nothing leaves.',
              },
              {
                emoji: '🔁',
                step: '04',
                title: 'Come back tomorrow',
                desc: 'Your streak grows. Your journal fills. A new proverb waits each morning. Critical thinking is a daily practice.',
              },
            ].map((s, i, arr) => (
              <div key={s.step} style={{ display: 'flex', alignItems: 'flex-start' }}>
                {/* Step card */}
                <div style={{ flex: 1, padding: '0 20px', textAlign: 'center' }}>
                  <div style={{
                    width: 64, height: 64,
                    background: 'var(--parchment)',
                    border: 'var(--border)',
                    borderRadius: '50%',
                    display: 'flex', alignItems: 'center', justifyContent: 'center',
                    fontSize: 26,
                    margin: '0 auto 16px',
                    boxShadow: 'var(--shadow-sm)',
                  }}>
                    {s.emoji}
                  </div>
                  <p style={{ fontSize: 10, fontWeight: 800, letterSpacing: '0.15em', textTransform: 'uppercase', color: 'var(--terra)', marginBottom: 6 }}>
                    {s.step}
                  </p>
                  <p style={{ fontFamily: "'Lora', serif", fontWeight: 600, fontSize: 16, marginBottom: 10, color: 'var(--ink)' }}>
                    {s.title}
                  </p>
                  <p style={{ fontSize: 13, lineHeight: 1.65, color: 'var(--ink-muted)' }}>
                    {s.desc}
                  </p>
                </div>

                {/* Arrow connector — hidden after last item */}
                {i < arr.length - 1 && (
                  <div style={{
                    flexShrink: 0,
                    fontSize: 20,
                    color: 'var(--terra)',
                    opacity: 0.4,
                    paddingTop: 20,
                    lineHeight: 1,
                  }}>
                    →
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* ── Wave divider ─────────────────────────────────────────────────── */}
      <div style={{ position: 'relative', marginBottom: -2 }}>
        <svg viewBox="0 0 1440 80" xmlns="http://www.w3.org/2000/svg" style={{ display: 'block', width: '100%' }}>
          <path d="M0,40 C240,80 480,0 720,40 C960,80 1200,0 1440,40 L1440,80 L0,80 Z" fill="var(--mint-light)" />
        </svg>
      </div>

      {/* ── Theme grid ───────────────────────────────────────────────────── */}
      <div style={{ background: 'var(--mint-light)', padding: '48px 24px 64px', borderBottom: 'var(--border)' }}>
        <p style={{
          textAlign: 'center',
          fontSize: 11, fontWeight: 800,
          letterSpacing: '0.15em', textTransform: 'uppercase',
          color: '#5a7a76', marginBottom: 32,
        }}>
          Or choose any theme
        </p>
        <div style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fill, minmax(160px, 1fr))',
          gap: 16, maxWidth: 800, margin: '0 auto',
        }}>
          {themes.length === 0
            ? Array.from({ length: 9 }).map((_, i) => (
                <div key={i} className="theme-pill" style={{ opacity: 0.3, height: 46 }} />
              ))
            : themes.map(theme => (
                <button key={theme} className="theme-pill" onClick={() => onSelectTheme(theme)}>
                  {THEME_EMOJIS[theme] ?? '🌿'} {theme}
                </button>
              ))
          }
        </div>
      </div>

      {/* ── For classrooms ───────────────────────────────────────────────── */}
      <div style={{ background: 'var(--parchment-dk)', padding: '56px 24px', borderTop: 'var(--border)' }}>
        <div style={{ maxWidth: 700, margin: '0 auto', textAlign: 'center' }}>
          <span className="pill-label pill-mint" style={{ marginBottom: 20, display: 'inline-block' }}>For educators</span>
          <h2 style={{ fontSize: 'clamp(1.4rem, 3vw, 2rem)', marginBottom: 16 }}>
            Built for curious minds everywhere
          </h2>
          <p style={{
            fontFamily: "'Lora', serif",
            fontStyle: 'italic',
            fontSize: 16,
            lineHeight: 1.8,
            color: 'var(--ink-muted)',
            maxWidth: 560,
            margin: '0 auto 36px',
          }}>
            ThinkDeep works as a daily critical thinking exercise for classrooms — no accounts, no tracking, no internet required for the AI. Students reflect on a proverb, the model challenges their thinking, and the conversation stays private on the device.
          </p>
          <div style={{ display: 'flex', gap: 16, justifyContent: 'center', flexWrap: 'wrap' }}>
            {[
              { icon: '🔒', text: 'Fully local · Gemma 4 on-device' },
              { icon: '🌍', text: '11 cultural traditions' },
              { icon: '🏛️', text: 'Socratic dialogue mode' },
              { icon: '📖', text: 'No accounts needed' },
            ].map(f => (
              <div key={f.text} style={{
                display: 'flex', alignItems: 'center', gap: 8,
                background: 'var(--paper)',
                border: 'var(--border)',
                borderRadius: 10,
                padding: '10px 18px',
                boxShadow: 'var(--shadow-sm)',
                fontSize: 14, fontWeight: 700,
              }}>
                <span>{f.icon}</span> {f.text}
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* ── Footer ───────────────────────────────────────────────────────── */}
      <div style={{ background: 'var(--ink)', padding: '36px 24px', textAlign: 'center' }}>
        <p style={{
          fontFamily: "'Lora', serif",
          fontStyle: 'italic',
          color: 'rgba(255,255,255,0.6)',
          fontSize: 15,
          marginBottom: 12,
        }}>
          "The more you think, the more you become."
        </p>
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', gap: 8 }}>
          <span style={{
            background: 'rgba(255,255,255,0.1)',
            border: '1px solid rgba(255,255,255,0.2)',
            borderRadius: 6,
            padding: '4px 12px',
            fontSize: 11,
            fontWeight: 700,
            letterSpacing: '0.08em',
            textTransform: 'uppercase',
            color: 'rgba(255,255,255,0.7)',
          }}>
            🔒 Powered by Gemma 4 · Runs entirely on your device
          </span>
        </div>
      </div>
    </div>
  )
}
