# ThinkDeep — codex.md

## Objective

Build a simple, clean AI learning loop using LangGraph and Gemma 4 E4B (gemma4:e4b). 

---

## Development Rules

### 1. Keep architecture simple

* Do NOT introduce unnecessary abstractions
* Do NOT create extra agents or services
* Keep everything in a single Python app

---

### 2. Follow node-based design

Each step must be a pure function:

def coach_node(state) → state
def evaluator_node(state) → state
def reporter_node(state) → state

No side effects inside nodes.

---

### 3. Central state only

All data must flow through SessionState.

Do NOT use:

* global variables
* hidden state
* scattered memory

---

### 4. Prompt separation

Store prompts separately:

prompts/
coach.txt
evaluator.txt
reporter.txt

Never hardcode prompts inside logic.

---

### 5. Add tracing (@traceable)

All node functions must be traceable:

from langsmith import traceable

@traceable
def coach_node(state):
...

@traceable
def evaluator_node(state):
...

@traceable
def reporter_node(state):
...

Purpose:

* debug prompt behavior
* inspect outputs
* understand flow

---

### 6. LLM usage

* Use Gemma 4 E4B (gemma4:e4b) via Ollama
* Keep prompts deterministic and structured
* Avoid long verbose outputs

---

### 7. SQLite usage

Use SQLite ONLY for:

* session history
* interactions
* reports

Do NOT:

* over-design schema
* add complex queries

---

### 8. UI separation

app.py should:

* handle Streamlit UI
* call graph
* display results

Do NOT put business logic in UI.

---

## Code Style

* small functions
* clear names
* readable over clever

---

## Anti-Patterns (avoid)

* multiple competing flows
* mixing UI + logic
* premature optimization
* complex agent frameworks
---

## Success Definition
* user can complete full session
* system asks meaningful questions
* evaluation feels helpful
* report feels personalized

---

## Guiding Principle

“Build the simplest thing that works beautifully.”

---
