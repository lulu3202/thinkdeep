export type Entry = {
  proverb: string
  culture: string
  theme: string
  question: string
  context?: string
}

export type ExploreTurn = {
  user: string
  ai: string
}

export type Reflection = {
  theme: string
  culture: string
  proverb: string
  question: string
  user_reflection: string
  ai_response: string
  timestamp: string
  explore_turns?: ExploreTurn[]
}
