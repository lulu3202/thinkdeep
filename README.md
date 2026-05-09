# ThinkDeep

> Every question is a chance to think deeper.

ThinkDeep is a local-first AI learning experience that guides you through stories using reflective questions. No cloud. No accounts. Just you, a story, and a thoughtful AI tutor running entirely on your machine.

---

## What it does

You pick a story. ThinkDeep breaks it into parts, asks you a question about each one, and gives you honest feedback on your answer. It's designed to slow reading down and make thinking visible.

**Current mode: Story Mode**

- Browse a catalog of classic short stories
- Read one chunk at a time
- Answer a reflective question per chunk
- Get scored feedback (0–2) before moving on
- Track your progress through the story

---

## Stories included

| Title | Author |
|---|---|
| The Selfish Giant | Oscar Wilde |
| The Happy Prince | Oscar Wilde |
| The Nightingale and the Rose | Oscar Wilde |

---

## Tech stack

| Layer | Tool |
|---|---|
| UI | Streamlit |
| AI orchestration | LangGraph |
| Local LLM | Ollama (`gemma4:e4b`) |
| State management | Pydantic (`SessionState`) |
| Story storage | Plain `.txt` files |

Everything runs locally. No API keys required.

---

## Setup

**1. Clone the repo**

```bash
git clone <your-repo-url>
cd thinkdeep
```

**2. Install dependencies**

Requires Python 3.11+ and [uv](https://docs.astral.sh/uv/).

```bash
uv sync
```

**3. Install Ollama**

Download from [ollama.com](https://ollama.com) and pull the model:

```bash
ollama pull gemma4:e4b
```

---

## Run

**Start Ollama** (if not already running):

```bash
ollama serve
```

**Start the app:**

```bash
uv run streamlit run app.py
```

Open [http://localhost:8501](http://localhost:8501) in your browser.

---

## Project structure

```
thinkdeep/
├── app.py              # Streamlit UI
├── state.py            # SessionState — single source of truth
├── graph.py            # LangGraph workflow
├── config.py           # Model config
├── stories.py          # Story catalog + chunking logic
├── nodes/
│   ├── coach.py        # Generates one question per chunk
│   ├── evaluator.py    # Scores and gives feedback on answers
│   └── reporter.py     # Session summary (end of story)
└── stories/
    ├── selfish_giant.txt
    ├── happy_prince.txt
    └── nightingale_rose.txt
```

---

## Adding a new story

1. Drop a `.txt` file into `stories/`
2. Add an entry to `STORIES` in `stories.py`:

```python
"my_story": {
    "title": "My Story Title",
    "file": "stories/my_story.txt",
    "cover": "images/my_story.jpeg",
    "description": "A short description.",
}
```

3. Drop a cover image into `images/`

That's it.

---

## Roadmap

- [ ] Science Mode — question-driven exploration of science concepts
- [ ] Ethics Mode — open-ended moral reasoning prompts
- [ ] Session history — track answers and scores across sessions
- [ ] LangSmith tracing — observability for each node run
- [ ] Upload your own stories

---

## Philosophy

ThinkDeep is built on one idea: reading without reflection is just scanning. The goal isn't to test knowledge — it's to slow the reader down and create space for genuine thinking.

Local-first by design. Your learning stays on your machine.
