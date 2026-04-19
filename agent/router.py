"""
Router Node — classifies the user's intent and sets the routing decision.
Routes: "rag" | "tool_datetime" | "tool_calculator" | "out_of_scope"
"""
from __future__ import annotations

import os

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_google_genai import ChatGoogleGenerativeAI

from agent.state import AgentState

_SYSTEM_PROMPT = """You are a smart router for an academic student assistant at KIIT University.

Classify the student's question into EXACTLY one of these categories:

1. "rag"             — Question about academic content: syllabus, course notes, unit topics,
                        exam rules, assignments, grading, attendance, revision tips, FAQs,
                        B.Tech CSCE program, any subject (DSA, OS, DBMS, Networks, SE).
2. "tool_datetime"   — Question asking about the current date, time, day of week, or year.
3. "tool_calculator" — Question asking for a mathematical calculation or numeric computation
                       (percentages, arithmetic, formula evaluation).
4. "out_of_scope"    — Question completely unrelated to academics or the available tools
                       (e.g., sports news, cooking, politics, entertainment).

Rules:
- Respond with ONLY the category label — nothing else.
- When in doubt, prefer "rag" over "out_of_scope".

Examples:
"What is the minimum attendance?" -> rag
"Explain AVL tree rotations." -> rag
"What time is it right now?" -> tool_datetime
"What day is today?" -> tool_datetime
"Calculate 15% of 400" -> tool_calculator
"What is 2 to the power of 10?" -> tool_calculator
"Who won the IPL 2024?" -> out_of_scope
"""


def router_node(state: AgentState) -> dict:
    """Determine the route for the current question."""
    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-flash",
        temperature=0,
        google_api_key=os.getenv("GOOGLE_API_KEY"),
    )

    response = llm.invoke(
        [
            SystemMessage(content=_SYSTEM_PROMPT),
            HumanMessage(content=state["question"]),
        ]
    )

    raw = response.content.strip().lower()

    # Normalise to one of the four categories
    if "tool_datetime" in raw or raw in {"tool_date", "tool_time"}:
        route = "tool_datetime"
        tool_name = "datetime"
    elif "tool_calculator" in raw or "tool_calc" in raw:
        route = "tool_calculator"
        tool_name = "calculator"
    elif "out_of_scope" in raw or "out-of-scope" in raw:
        route = "out_of_scope"
        tool_name = ""
    else:
        route = "rag"
        tool_name = ""

    return {
        "route": route,
        "tool_name": tool_name,
        "retry_count": 0,
        "source_docs": [],
        "filtered_docs": [],
        "retrieved_docs": [],
        "answer": "",
        "faithfulness_ok": False,
    }


# ── Conditional edge helper ──────────────────────────────────────────────────

def route_decision(state: AgentState) -> str:
    """Used by the graph's conditional edge after the router node."""
    route = state.get("route", "rag")
    if route == "rag":
        return "retriever"
    elif route in {"tool_datetime", "tool_calculator"}:
        return "tool"
    else:
        return "generator"   # out_of_scope → generator handles it
