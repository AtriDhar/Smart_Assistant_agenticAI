"""
Evaluator Node — faithfulness / hallucination check.
Verifies that every factual claim in the answer is grounded in the retrieved context.
If not faithful and retry budget remains, signals the graph to re-retrieve.
"""
from __future__ import annotations

import os

from agent.llm_config import get_chat_llm
from agent.state import AgentState

_MAX_RETRIES = 2

_EVAL_PROMPT = """You are a faithfulness evaluator for an AI academic assistant.

Your job: Check whether every factual claim in the ANSWER is directly supported by the CONTEXT.

CONTEXT:
{context}

ANSWER:
{answer}

Evaluation criteria:
- A claim is "supported" only if the specific fact (number, rule, date, percentage, name) 
  appears explicitly in the CONTEXT.
- If the ANSWER says "I don't have enough information", that is always FAITHFUL.
- Ignore phrasing and style; focus on factual claims only.

Respond with exactly one word:
- FAITHFUL     — if ALL claims are supported by the context.
- NOT_FAITHFUL — if ANY claim, fact, number, rule, or date is NOT in the context.

Your one-word response:"""


def _get_llm():
    return get_chat_llm(temperature=0)


def evaluator_node(state: AgentState) -> dict:
    """Check faithfulness; increment retry_count if not faithful."""
    route = state.get("route", "rag")

    # Skip evaluation for non-RAG routes
    if route != "rag":
        return {"faithfulness_ok": True}

    answer = state.get("answer", "")
    docs = state.get("filtered_docs") or state.get("retrieved_docs") or []

    # If no docs to compare against, trust the answer
    if not docs:
        return {"faithfulness_ok": True}

    # "I don't know" type answers are always faithful
    no_info_phrases = [
        "don't have enough information",
        "couldn't find relevant",
        "not in my knowledge base",
        "outside my knowledge",
    ]
    if any(p in answer.lower() for p in no_info_phrases):
        return {"faithfulness_ok": True}

    # Limit context to top-3 docs for efficiency
    context = "\n\n".join(doc.page_content for doc in docs[:3])

    llm = _get_llm()
    prompt = _EVAL_PROMPT.format(context=context, answer=answer)
    response = llm.invoke(prompt)

    raw = response.content.strip().upper()
    faithful = "NOT_FAITHFUL" not in raw and "FAITHFUL" in raw

    if faithful:
        return {"faithfulness_ok": True}
    else:
        current_retry = state.get("retry_count", 0)
        return {
            "faithfulness_ok": False,
            "retry_count": current_retry + 1,
        }


# ── Conditional edge helper ──────────────────────────────────────────────────

def check_faithfulness(state: AgentState) -> str:
    """Used by the graph's conditional edge after the evaluator node."""
    if state.get("faithfulness_ok", True):
        return "memory"
    elif state.get("retry_count", 0) >= _MAX_RETRIES:
        # Append a disclaimer and move on
        return "memory"
    else:
        return "retriever"
