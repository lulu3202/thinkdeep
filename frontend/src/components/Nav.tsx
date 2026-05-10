type NavProps = {
  historyCount: number
  streak: number
  onViewHistory: () => void
  onHome: () => void
}

export default function Nav({ historyCount, streak, onViewHistory, onHome }: NavProps) {
  return (
    <nav className="nav">
      <span className="nav-logo" onClick={onHome}>
        Think<span>Deep</span>
      </span>

      <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
        {streak > 0 && (
          <span style={{
            display: 'inline-flex',
            alignItems: 'center',
            gap: 4,
            background: 'var(--cream)',
            border: '2px solid var(--dark)',
            borderRadius: 'var(--radius-pill)',
            padding: '4px 14px',
            fontWeight: 800,
            fontSize: 14,
            boxShadow: 'var(--shadow-sm)',
          }}>
            🔥 {streak} day{streak !== 1 ? 's' : ''}
          </span>
        )}
        {historyCount > 0 && (
          <button
            className="btn btn-peach"
            style={{ fontSize: 13, padding: '8px 20px' }}
            onClick={onViewHistory}
          >
            {historyCount} Reflection{historyCount !== 1 ? 's' : ''}
          </button>
        )}
      </div>
    </nav>
  )
}
