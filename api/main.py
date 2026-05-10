# api/main.py
#
# FastAPI backend for ThinkDeep.
# Exposes streaming SSE endpoints consumed by the React frontend.
# The Python AI logic (nodes/) is imported from the parent directory.
#
# Run with:  uv run uvicorn api.main:app --reload --port 8000
#
# Future: add auth, rate limiting, session persistence.

import sys
import json
import random

sys.path.insert(0, "..")   # allow importing from thinkdeep root

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

from state import SessionState
from nodes.evaluator import stream_wisdom_evaluator
from nodes.explore import explore_node
from nodes.wisdom_reporter import stream_wisdom_report
from nodes.socratic import stream_socratic
from wisdom.wisdom_entries import get_themes, get_entries_by_theme
from session import get_summary_context

app = FastAPI(title="ThinkDeep API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],   # Vite dev server
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------------------------------------------------------
# Request / Response models
# ---------------------------------------------------------------------------

class ReflectRequest(BaseModel):
    proverb: str
    question: str
    answer: str


class ExploreRequest(BaseModel):
    proverb: str
    question: str
    original_answer: str
    evaluator_feedback: str
    explore_history: list   # [{"user": "...", "ai": "..."}]
    user_message: str


class ReportRequest(BaseModel):
    history: list           # list of reflection dicts from the frontend


# ---------------------------------------------------------------------------
# Catalog endpoints
# ---------------------------------------------------------------------------

@app.get("/api/themes")
def themes():
    """Returns all available wisdom themes."""
    return {"themes": get_themes()}


@app.get("/api/proverb/{theme}")
def proverb(theme: str):
    """Returns a random wisdom entry for the given theme."""
    entries = get_entries_by_theme(theme)
    if not entries:
        return {"error": "Theme not found"}, 404
    return random.choice(entries)


# ---------------------------------------------------------------------------
# Streaming endpoints (Server-Sent Events)
# ---------------------------------------------------------------------------

def sse(generator):
    """Wraps a text generator into SSE format for the frontend."""
    def stream():
        for chunk in generator:
            if chunk:
                yield f"data: {json.dumps({'text': chunk})}\n\n"
        yield "data: [DONE]\n\n"
    return StreamingResponse(stream(), media_type="text/event-stream")


@app.post("/api/reflect")
def reflect(req: ReflectRequest):
    """
    Streams the AI's reflective response to the user's answer.
    Uses stream_wisdom_evaluator — mode-aware, conversational, no scoring.
    """
    state = SessionState(
        session_id="api-session",
        mode="wisdom",
        paragraph=req.proverb,
        question=req.question,
        answer=req.answer,
    )
    return sse(stream_wisdom_evaluator(state))


@app.post("/api/socratic")
def socratic(req: ReflectRequest):
    """Streams a Socratic challenge — gently questions the user's reflection."""
    state = SessionState(
        session_id="api-session",
        mode="wisdom",
        paragraph=req.proverb,
        question=req.question,
        answer=req.answer,
    )
    return sse(stream_socratic(state))


@app.post("/api/explore")
def explore(req: ExploreRequest):
    """
    Returns one contextual follow-up response (non-streaming for simplicity).
    Max 3 turns enforced on the frontend.
    """
    reply = explore_node(
        mode="wisdom",
        paragraph=req.proverb,
        question=req.question,
        original_answer=req.original_answer,
        evaluator_feedback=req.evaluator_feedback,
        explore_history=req.explore_history,
        user_message=req.user_message,
    )
    return {"reply": reply}


@app.post("/api/report")
def report(req: ReportRequest):
    """Streams a personalised reflection summary from the session history."""
    context = get_summary_context(req.history)
    return sse(stream_wisdom_report(context))


@app.get("/api/health")
def health():
    return {"status": "ok"}
