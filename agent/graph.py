"""
LangGraph StateGraph — wires all 7 nodes into the Smart Student Assistant.

Graph flow:
  START
    └─► router
          ├─► retriever ─► grader ─► generator ─► evaluator
          │                                            ├─► memory (faithful / give-up)
          │                                            └─► retriever  (retry loop)
          ├─► tool ─────────────────────────────────────► memory
          └─► generator (out_of_scope) ─────────────────► memory
                                                              └─► END
"""
from __future__ import annotations

from langgraph.graph import END, START, StateGraph

from agent.evaluator import check_faithfulness, evaluator_node
from agent.generator import generator_node
from agent.grader import grader_node
from agent.memory import memory_node
from agent.retriever import retriever_node
from agent.router import route_decision, router_node
from agent.state import AgentState
from agent.tools import tool_node


def build_graph():
    """Build and compile the LangGraph agent."""
    workflow = StateGraph(AgentState)

    # ── Register nodes ────────────────────────────────────────────────────────
    workflow.add_node("router", router_node)
    workflow.add_node("retriever", retriever_node)
    workflow.add_node("grader", grader_node)
    workflow.add_node("generator", generator_node)
    workflow.add_node("evaluator", evaluator_node)
    workflow.add_node("tool", tool_node)
    workflow.add_node("memory", memory_node)

    # ── Entry point ───────────────────────────────────────────────────────────
    workflow.add_edge(START, "router")

    # ── Router → conditional branch ───────────────────────────────────────────
    workflow.add_conditional_edges(
        "router",
        route_decision,
        {
            "retriever": "retriever",
            "tool": "tool",
            "generator": "generator",   # out_of_scope path
        },
    )

    # ── RAG pipeline ──────────────────────────────────────────────────────────
    workflow.add_edge("retriever", "grader")
    workflow.add_edge("grader", "generator")

    # ── Generator → evaluator OR memory (out_of_scope skips evaluator) ────────
    def post_generator(state: AgentState) -> str:
        return "evaluator" if state.get("route") == "rag" else "memory"

    workflow.add_conditional_edges(
        "generator",
        post_generator,
        {
            "evaluator": "evaluator",
            "memory": "memory",
        },
    )

    # ── Evaluator → memory (pass/give-up) OR retriever (retry) ───────────────
    workflow.add_conditional_edges(
        "evaluator",
        check_faithfulness,
        {
            "memory": "memory",
            "retriever": "retriever",
        },
    )

    # ── Tool / Memory → END ───────────────────────────────────────────────────
    workflow.add_edge("tool", "memory")
    workflow.add_edge("memory", END)

    return workflow.compile()


# Module-level compiled app (lazy — built on first import)
_graph = None


def get_graph():
    global _graph
    if _graph is None:
        _graph = build_graph()
    return _graph
