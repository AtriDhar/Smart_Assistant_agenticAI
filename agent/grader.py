"""
Grader Node — scores each retrieved document for relevance to the question.
Irrelevant documents are filtered out before answer generation.
If all documents fail, keep the top-3 as a fallback.
"""
from __future__ import annotations

import os

from agent.llm_config import get_chat_llm
from agent.state import AgentState

_GRADE_PROMPT = """You are a relevance grader for an academic question-answering system.

Question: {question}

Retrieved Document:
\"\"\"
{document}
\"\"\"

Is this document excerpt relevant and useful for answering the question above?
Respond with ONLY "YES" or "NO" — no explanation.
"""


def _get_llm():
    return get_chat_llm(temperature=0)


def grader_node(state: AgentState) -> dict:
    """Filter retrieved_docs to those relevant to the question."""
    llm = _get_llm()
    question = state["question"]
    docs = state.get("retrieved_docs", [])

    relevant_docs = []
    source_docs: list[str] = []

    for doc in docs:
        prompt = _GRADE_PROMPT.format(
            question=question,
            document=doc.page_content[:1200],  # Truncate very long chunks
        )
        response = llm.invoke(prompt)
        if "yes" in response.content.strip().lower():
            relevant_docs.append(doc)
            src = doc.metadata.get("source", "Unknown")
            if src not in source_docs:
                source_docs.append(src)

    # Fallback: if nothing passed grading, keep top-3 retrieved docs
    if not relevant_docs:
        relevant_docs = docs[:3]
        source_docs = list(
            dict.fromkeys(
                doc.metadata.get("source", "Unknown") for doc in relevant_docs
            )
        )

    return {
        "filtered_docs": relevant_docs,
        "source_docs": source_docs,
    }
