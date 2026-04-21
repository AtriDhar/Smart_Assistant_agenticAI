"""
Generator Node — produces grounded answers strictly from the filtered documents.
For "out_of_scope" route, returns a polite refusal without hallucinating.
"""
from __future__ import annotations

import os

from langchain_core.messages import AIMessage, HumanMessage

from agent.llm_config import get_chat_llm
from agent.state import AgentState

_OUT_OF_SCOPE_MSG = (
    "I'm sorry, but I can only answer questions related to the B.Tech CSCE program "
    "at KIIT University — such as syllabus, course notes (DSA, OS, DBMS, Networks, SE), "
    "exam rules, assignments, grading, attendance policy, revision tips, and FAQs. "
    "Your question appears to be outside my knowledge base. "
    "Please feel free to ask anything related to your academics!"
)

_RAG_SYSTEM = """You are a Smart Student Assistant for B.Tech CSCE students at KIIT University.
Answer the student's question using ONLY the context documents provided below.

STRICT RULES — follow these without exception:
1. Use ONLY information present in the context. Do NOT use your general training knowledge.
2. If the context does not contain enough information, say exactly:
   "I don't have enough information in my knowledge base to fully answer this."
3. NEVER guess, fabricate, or estimate any dates, marks, percentages, rules, names, or facts.
4. Be clear, specific, and helpful. Use bullet points or numbered lists when appropriate.
5. When quoting specific facts (marks, percentages, deadlines), say which source document 
   supports it, e.g. "According to the exam rules: ...".
6. Keep the answer focused and concise (under 300 words unless detail is essential).

Previous conversation (for follow-up context only — do NOT treat as new facts):
{history}

Context Documents:
{context}

Student Question: {question}

Answer:"""


def _get_llm():
    return get_chat_llm(temperature=0.1)


def _build_history(messages) -> str:
    if not messages:
        return "No prior conversation."
    parts = []
    for msg in messages[-6:]:  # Last 3 exchanges
        if isinstance(msg, HumanMessage):
            parts.append(f"Student: {msg.content}")
        elif isinstance(msg, AIMessage):
            parts.append(f"Assistant: {msg.content}")
    return "\n".join(parts)


def generator_node(state: AgentState) -> dict:
    """Generate a grounded answer or a polite refusal."""
    route = state.get("route", "rag")

    # ── Out-of-scope: refuse politely ───────────────────────────────────────
    if route == "out_of_scope":
        return {"answer": _OUT_OF_SCOPE_MSG, "source_docs": []}

    # ── RAG: generate from context ──────────────────────────────────────────
    docs = state.get("filtered_docs") or state.get("retrieved_docs") or []
    if not docs:
        return {
            "answer": (
                "I couldn't find relevant information in my knowledge base to answer "
                "this question. Please try rephrasing or ask about a topic covered in "
                "the B.Tech CSCE course materials."
            ),
            "source_docs": [],
        }

    context = "\n\n---\n\n".join(
        f"[Source: {doc.metadata.get('source', 'Unknown')}]\n{doc.page_content}"
        for doc in docs
    )
    history = _build_history(state.get("messages", []))

    prompt = _RAG_SYSTEM.format(
        history=history,
        context=context,
        question=state["question"],
    )

    llm = _get_llm()
    response = llm.invoke(prompt)
    return {"answer": response.content.strip()}
