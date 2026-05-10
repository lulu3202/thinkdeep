# ThinkDeep

**AI-powered cross-cultural wisdom for critical thinking — runs entirely on Gemma 4, offline-capable, privacy-first.**

> *Submitted to the [Gemma 4 Good Hackathon](https://www.kaggle.com/competitions/gemma-4-good-hackathon)*
> *Categories: Future of Education · Digital Equity & Inclusivity*

---

## The Problem

Critical thinking is one of the most important skills a person can develop — and one of the hardest to teach at scale. Most AI tools in education follow a question-answer format: they deliver information, test recall, and move on. They do not teach you to *think*.

Meanwhile, the world's philosophical traditions have spent thousands of years developing exactly this skill. Stoic philosophy, Zen teachings, Ubuntu ethics, Tamil wisdom — these traditions use carefully constructed proverbs and questions to make people examine their own assumptions. The problem: this kind of reflective practice is locked behind language barriers, academic paywalls, and cultural distance.

There is also a second problem: most AI tools require a cloud connection, send user data to remote servers, and are inaccessible in low-bandwidth environments like rural schools, community centres, or areas with limited infrastructure.

---

## The Solution

**ThinkDeep** is a daily reflection and critical thinking tool built around proverbs from 11 cultural traditions, powered entirely by Gemma 4 running locally via Ollama.

Every day, the app surfaces a proverb — from Japanese Zen, West African oral tradition, Stoic philosophy, Ubuntu ethics, Tamil literature, Sufi poetry, Native American wisdom, Buddhist teaching, or Chinese Daoism. The user reads it, reflects on it, and writes a response. Gemma 4 then responds in one of two modes:

- **Reflect** — the AI engages warmly, drawing connections between the user's experience and the wider wisdom tradition
- **Socratic Challenge** — the AI identifies an assumption in the user's thinking and asks a probing counter-question, pushing them to go deeper

No data leaves the device. No account is needed. No internet is required after setup. A student in a school with poor connectivity reflects on the same depth of philosophical tradition as anyone else.

---

## How It Works

**Four steps. One thought at a time.**

```
📖 Pick a proverb  →  ✍️ Write freely  →  🧠 Gemma 4 responds  →  🔁 Come back tomorrow
```

**1 · 📖 Pick a proverb**
Choose from 9 themes across 11 cultural traditions. A proverb surfaces — from Stoic philosophy, West African oral tradition, Tamil literature, Zen teaching, and more. A cultural context panel tells you where it comes from and why it matters. Read it once.

**2 · ✍️ Write freely**
A reflective question appears beneath the proverb. Answer it in your own words. No right answers. No grading. No word count. Just your honest thinking.

**3 · 🧠 Gemma 4 responds — on your device**
Before submitting, choose your mode:
- **Reflect** — Gemma 4 engages warmly, drawing threads between your experience and the wisdom tradition it came from.
- **Socratic Challenge** — Gemma 4 identifies one assumption in your thinking and asks a probing counter-question. You go deeper.

The response streams live from the local model. Nothing leaves your machine.

**4 · 🔁 Come back tomorrow**
Your streak grows. Your journal fills. A new proverb waits each morning. After several reflections, ask for a session summary — Gemma 4 synthesises what your thinking reveals about you.

---

## Why Gemma 4

| Capability | How ThinkDeep uses it |
|---|---|
| **On-device inference** | Gemma 4 runs via Ollama — fully local, zero cloud dependency |
| **Instruction following** | Socratic and reflective prompts require nuanced instruction-following to stay philosophical without being preachy |
| **Low resource deployment** | Works on a standard laptop;|
| **Privacy-first** | Reflections stored only in browser localStorage — nothing transmitted |
| **Multilingual potential** | Gemma 4's multilingual capability positions this for future localisation into Tamil, Arabic, Japanese, Swahili |

---

## Cultural Traditions

ThinkDeep draws from 11 traditions across 6 continents — this is not a Western-centric AI:

| Tradition | Region | Example theme |
|---|---|---|
| 🌸 Japanese Wisdom | East Asia | Resilience |
| 🌍 African Proverb | Sub-Saharan Africa | Truth, Wisdom |
| 🤝 Ubuntu Philosophy | Southern Africa | Kindness |
| 🎋 Tamil Wisdom (Thirukural) | South Asia | Kindness, Wisdom |
| 🌺 Indian Wisdom | South Asia | Patience, Anger |
| 🏮 Chinese Wisdom | East Asia | Patience |
| 🍵 Zen Teaching | East Asia | Humility, Perspective |
| 🏛️ Stoic Philosophy | Ancient Greece / Rome | Courage, Truth |
| 🌙 Sufi Wisdom | Middle East / Central Asia | Courage |
| 🪷 Buddhist Teaching | South / Southeast Asia | Anger |
| 🦅 Native American Wisdom | North America | Perspective |

Every proverb includes a **cultural context panel** — a 2-sentence historical background explaining the intellectual tradition it comes from.

---

## Features

- **Daily proverb** — one proverb surfaces each day, automatically rotating. Cached locally so it stays consistent all day
- **Streak tracking** — a daily habit counter (current streak, longest streak) that persists in localStorage
- **Two AI modes** — Reflect (warm, connective) and Socratic Challenge (assumption-questioning, probing)
- **Cultural context** — expandable panel beneath every proverb with historical background
- **Explore Deeper** — up to 3 follow-up dialogue turns with Gemma 4 after the initial reflection
- **Wisdom Journal** — all reflections saved to localStorage; sessions survive browser restarts
- **Session summary** — Gemma 4 generates a personalised insight across all reflections in a session
- **No login, no tracking, no cloud** — everything runs locally

---

## Architecture

```
Browser  (React 18 + Vite + TypeScript)
  │
  ├── AmbientCanvas     React Three Fiber — slow terracotta / sage particles
  ├── Nav               streak counter, reflections count
  ├── HomePage          daily proverb card, culture badge row, theme grid
  ├── ReflectionView    proverb, context panel, mode toggle, streaming AI
  └── HistoryView       journal accordion, streaming session summary
  │
  │   HTTP + Server-Sent Events  (Vite proxy → localhost:8000)
  ▼
FastAPI  (Python · Uvicorn)
  │
  ├── GET  /api/themes
  ├── GET  /api/proverb/{theme}     wisdom_entries.py  (18 entries, 9 themes)
  ├── POST /api/reflect             evaluator.py    →  SSE stream
  ├── POST /api/socratic            socratic.py     →  SSE stream
  ├── POST /api/explore             explore.py      →  JSON reply
  └── POST /api/report              wisdom_reporter →  SSE stream
  │
  │   ollama.chat(stream=True)
  ▼
Ollama  →  gemma4:e2b  (local)
            └── LangSmith tracing (@traceable on all nodes)
```

**State and persistence:**
- `localStorage` — journal, streak data, daily proverb (keyed by calendar date)
- No server-side state, no database, no user accounts

---

## Setup

### Prerequisites

- Python 3.11+, [`uv`](https://docs.astral.sh/uv/) package manager
- Node.js 18+
- [Ollama](https://ollama.com) installed and running

### 1 — Pull the model

```bash
ollama pull gemma4:e2b
```

Runs on CPU on a standard laptop — no GPU required.

### 2 — Backend

```bash
# From the project root
uv sync
uv run uvicorn api.main:app --reload --port 8000
```

Optional — add a `.env` file to enable LangSmith tracing:

```
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=your_key_here
LANGCHAIN_PROJECT=thinkdeep
```

### 3 — Frontend

```bash
cd frontend
npm install
npm run dev
```

Open **http://localhost:5173**

---

## Project Structure

```
thinkdeep/
├── api/
│   └── main.py              FastAPI — all HTTP + SSE endpoints
├── nodes/
│   ├── evaluator.py         Reflective AI response (streaming)
│   ├── socratic.py          Socratic challenge mode (streaming)
│   ├── explore.py           Follow-up dialogue turns
│   └── wisdom_reporter.py   Personalised session summary (streaming)
├── wisdom/
│   └── wisdom_entries.py    18 proverbs · 9 themes · 11 traditions
├── frontend/src/
│   ├── pages/               HomePage · ReflectionView · HistoryView
│   ├── components/          Nav · AmbientCanvas
│   └── lib/                 api.ts (SSE client) · storage.ts (localStorage)
├── config.py                Gemma 4 model name
├── state.py                 SessionState (Pydantic)
└── session.py               Journal helpers (framework-free)
```

---

## Hackathon Alignment

### Future of Education
ThinkDeep teaches critical thinking through Socratic dialogue, not content delivery. A student who uses it daily practises the skill of examining their own assumptions — transferable across every subject and curriculum. The daily streak mechanic builds a long-term reflection habit rather than a one-off experience.

### Digital Equity & Inclusivity
The entire AI pipeline runs locally on a consumer laptop after a one-time model download. There is no difference in experience between a student with high-speed broadband and one in a low-connectivity classroom. The content draws from 11 global philosophical traditions, deliberately non-Western-centric.

### What makes this distinct from generic AI tutors
- Socratic mode **actively challenges** the user's thinking rather than affirming it
- 11 non-Western traditions make the content globally relevant, not just accessible
- Fully offline after setup — works in schools with unreliable or no internet
- No accounts, no data collection, no cloud dependency at runtime

---

## Possible Extensions

- Voice input using Gemma 4's multimodal capability — accessibility for low-literacy users
- Tamil, Arabic, and Japanese UI translations using Gemma 4's multilingual support
- Teacher mode: class-level theme summary with no individual data shared
- Export journal as a personal commonplace book (PDF)

---

*Built with Gemma 4 · FastAPI · React 18 · React Three Fiber · Ollama · LangSmith*

---
## Youtube Demo Link: 
https://youtu.be/y0lHirbVDJc
