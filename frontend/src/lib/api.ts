export async function fetchThemes(): Promise<string[]> {
  const res = await fetch('/api/themes')
  const data = await res.json()
  return data.themes
}

export async function fetchProverb(theme: string) {
  const res = await fetch(`/api/proverb/${encodeURIComponent(theme)}`)
  return res.json()
}

export async function streamSSE(
  url: string,
  body: object,
  onChunk: (text: string) => void,
): Promise<void> {
  const res = await fetch(url, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  })
  if (!res.body) return
  const reader = res.body.getReader()
  const decoder = new TextDecoder()
  let buffer = ''
  while (true) {
    const { done, value } = await reader.read()
    if (done) break
    buffer += decoder.decode(value, { stream: true })
    const lines = buffer.split('\n')
    buffer = lines.pop() ?? ''
    for (const line of lines) {
      if (!line.startsWith('data: ')) continue
      const payload = line.slice(6)
      if (payload === '[DONE]') return
      try {
        const parsed = JSON.parse(payload)
        if (parsed.text) onChunk(parsed.text)
      } catch {
        // ignore malformed SSE line
      }
    }
  }
}

export async function exploreMessage(body: {
  proverb: string
  question: string
  original_answer: string
  evaluator_feedback: string
  explore_history: { user: string; ai: string }[]
  user_message: string
}): Promise<string> {
  const res = await fetch('/api/explore', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  })
  const data = await res.json()
  return data.reply
}
