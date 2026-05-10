import { useState, useEffect } from 'react'
import type { Entry, Reflection } from './types'
import { fetchProverb, fetchThemes } from './lib/api'
import { loadJournal, saveJournal, loadStreak, updateStreak, loadDaily, saveDaily } from './lib/storage'
import type { StreakData, DailyRecord } from './lib/storage'
import AmbientCanvas from './components/AmbientCanvas'
import Nav from './components/Nav'
import HomePage from './pages/HomePage'
import ReflectionView from './pages/ReflectionView'
import HistoryView from './pages/HistoryView'

type View = 'home' | 'reflection' | 'history'

export default function App() {
  const [view, setView]               = useState<View>('home')
  const [currentEntry, setCurrentEntry] = useState<Entry | null>(null)
  const [history, setHistory]         = useState<Reflection[]>([])
  const [streak, setStreak]           = useState<StreakData>({ current: 0, longest: 0, lastDate: '' })
  const [daily, setDaily]             = useState<DailyRecord | null>(null)
  const [loading, setLoading]         = useState(false)
  const [loadingTheme, setLoadingTheme] = useState('')

  // On mount: restore journal, streak, and fetch today's daily proverb
  useEffect(() => {
    setHistory(loadJournal())
    setStreak(loadStreak())

    const cached = loadDaily()
    if (cached) {
      setDaily(cached)
    } else {
      fetchThemes()
        .then(themes => {
          const theme = themes[Math.floor(Math.random() * themes.length)]
          return fetchProverb(theme)
        })
        .then(entry => setDaily(saveDaily(entry)))
        .catch(console.error)
    }
  }, [])

  async function handleSelectTheme(theme: string) {
    setLoading(true)
    setLoadingTheme(theme)
    try {
      const entry = await fetchProverb(theme)
      setCurrentEntry(entry)
      setView('reflection')
    } catch (err) {
      console.error('Failed to fetch proverb', err)
    } finally {
      setLoading(false)
      setLoadingTheme('')
    }
  }

  function handleStartDaily() {
    if (!daily) return
    setCurrentEntry(daily.entry)
    setView('reflection')
  }

  function handleReflectionComplete(reflection: Reflection) {
    const next = [...history, reflection]
    setHistory(next)
    saveJournal(next)
    setStreak(updateStreak())
    setView('home')
    setCurrentEntry(null)
  }

  function handleBackFromReflection() {
    setView('home')
    setCurrentEntry(null)
  }

  return (
    <>
      <AmbientCanvas />

      <div style={{ position: 'relative', zIndex: 1 }}>
        <Nav
          historyCount={history.length}
          streak={streak.current}
          onViewHistory={() => setView('history')}
          onHome={() => { setView('home'); setCurrentEntry(null) }}
        />

        {/* Theme loading overlay */}
        {loading && (
          <div style={{
            position: 'fixed', inset: 0, zIndex: 50,
            display: 'flex', alignItems: 'center', justifyContent: 'center',
            background: 'rgba(250,247,242,0.9)', backdropFilter: 'blur(4px)',
          }}>
            <div className="card" style={{ textAlign: 'center', padding: '40px 60px' }}>
              <p style={{ fontSize: 28, marginBottom: 12 }}>🌿</p>
              <p style={{ fontFamily: "'Lora', serif", fontStyle: 'italic', fontSize: 18, color: 'var(--dark)' }}>
                Finding wisdom in {loadingTheme}…
              </p>
            </div>
          </div>
        )}

        {view === 'home' && (
          <HomePage
            onSelectTheme={handleSelectTheme}
            historyCount={history.length}
            streak={streak}
            daily={daily}
            onViewHistory={() => setView('history')}
            onStartDaily={handleStartDaily}
          />
        )}

        {view === 'reflection' && currentEntry && (
          <ReflectionView
            entry={currentEntry}
            onBack={handleBackFromReflection}
            onComplete={handleReflectionComplete}
          />
        )}

        {view === 'history' && (
          <HistoryView
            history={history}
            onBack={() => setView('home')}
          />
        )}
      </div>
    </>
  )
}
