# ThinkDeep — agents.md

## Product

ThinkDeep
“Every question is a chance to think deeper.”

---

## Core Principle

The system is a **guided thinking loop**, not a chatbot.

Flow:
input → question → answer → evaluation → repeat → report

---

## Modes

* reading → story comprehension
* science → conceptual reasoning (future)
* ethics → decision-making (future)

Mode only affects prompts, not architecture.

---

## Roles (Logical Agents)

### 1. Coach

**Purpose:** Ask one high-quality question per step

**Input:**

* current paragraph / concept / scenario
* mode
* age_band

**Output:**

* exactly ONE question

**Rules:**

* no explanations unless explicitly in vocab mode
* no multiple questions
* keep it age-appropriate
* encourage thinking, not recall

---

### 2. Evaluator

**Purpose:** Evaluate user answer

**Input:**

* question
* user answer
* context (paragraph)

**Output:**

* score (0–2)
* short feedback

**Rules:**

* 0 = incorrect / irrelevant
* 1 = partial
* 2 = strong answer
* feedback must guide improvement

---

### 3. Reporter

**Purpose:** Generate final session summary

**Input:**

* full interaction history
* scores

**Output:**

* 2–3 sentence personalized summary

**Rules:**

* must reference actual interaction
* no generic praise
* highlight thinking quality

---

## Node Mapping (LangGraph)

| Node           | Role      |
| -------------- | --------- |
| coach_node     | Coach     |
| evaluator_node | Evaluator |
| reporter_node  | Reporter  |

---

## State Object (shared)

SessionState:

* session_id
* mode
* paragraph
* question
* answer
* score
* feedback
* history
* final_summary

---

## Constraints

* No external APIs
* Use Gemma via Ollama only
* Keep responses concise
* One responsibility per node

---

## Philosophy

* Simplicity > cleverness
* One clear question > many weak ones
* Thinking > answering

---
