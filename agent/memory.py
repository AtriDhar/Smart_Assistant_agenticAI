"""
Memory Node — appends the Q&A pair to the conversation message history.
The AgentState.messages list is accumulated via operator.add,
so returning a list from this node automatically appends to existing history.
"""
from __future__ import annotations

from langchain_core.messages import AIMessage, HumanMessage

from agent.state import AgentState


def memory_node(state: AgentState) -> dict:
    """Persist the current Q&A turn into the messages list."""
    question = state.get("question", "")
    answer = state.get("answer", "")

    new_messages = [
        HumanMessage(content=question),
        AIMessage(content=answer),
    ]

    # Returning messages as a list causes operator.add to APPEND to existing history.
    return {"messages": new_messages}
