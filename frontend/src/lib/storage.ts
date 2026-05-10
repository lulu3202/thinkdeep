import type { Reflection, Entry } from '../types'

const JOURNAL_KEY  = 'thinkdeep_journal'
const STREAK_KEY   = 'thinkdeep_streak'
const DAILY_KEY    = 'thinkdeep_daily'

// ── Journal ──────────────────────────────────────────────────────────────────

export function loadJournal(): Reflection[] {
  try {
    const raw = localStorage.getItem(JOURNAL_KEY)
    return raw ? (JSON.parse(raw) as Reflection[]) : []
  } catch {
    return []
  }
}

export function saveJournal(reflections: Reflection[]): void {
  localStorage.setItem(JOURNAL_KEY, JSON.stringify(reflections))
}

// ── Streak ───────────────────────────────────────────────────────────────────

export type StreakData = {
  current: number
  longest: number
  lastDate: string   // 'YYYY-MM-DD'
}

export function loadStreak(): StreakData {
  try {
    const raw = localStorage.getItem(STREAK_KEY)
    return raw ? (JSON.parse(raw) as StreakData) : { current: 0, longest: 0, lastDate: '' }
  } catch {
    return { current: 0, longest: 0, lastDate: '' }
  }
}

export function updateStreak(): StreakData {
  const today     = todayStr()
  const streak    = loadStreak()
  if (streak.lastDate === today) return streak          // already reflected today

  const yesterday = new Date(Date.now() - 86_400_000).toISOString().slice(0, 10)
  const next      = streak.lastDate === yesterday ? streak.current + 1 : 1
  const updated: StreakData = {
    current:  next,
    longest:  Math.max(next, streak.longest),
    lastDate: today,
  }
  localStorage.setItem(STREAK_KEY, JSON.stringify(updated))
  return updated
}

// ── Daily proverb ─────────────────────────────────────────────────────────────

export type DailyRecord = {
  date:  string   // 'YYYY-MM-DD'
  entry: Entry
}

export function loadDaily(): DailyRecord | null {
  try {
    const raw = localStorage.getItem(DAILY_KEY)
    if (!raw) return null
    const rec = JSON.parse(raw) as DailyRecord
    return rec.date === todayStr() ? rec : null   // stale if not today
  } catch {
    return null
  }
}

export function saveDaily(entry: Entry): DailyRecord {
  const rec: DailyRecord = { date: todayStr(), entry }
  localStorage.setItem(DAILY_KEY, JSON.stringify(rec))
  return rec
}

// ── Helpers ──────────────────────────────────────────────────────────────────

export function todayStr(): string {
  return new Date().toISOString().slice(0, 10)
}
