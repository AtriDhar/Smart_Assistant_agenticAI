"""
Tools Node — handles tool-based queries:
  - tool_datetime  : Returns current date, time, and day.
  - tool_calculator: Safely evaluates mathematical expressions.
"""
from __future__ import annotations

import ast
import datetime
import operator as op
import re

from agent.state import AgentState

# ── Safe math evaluator ──────────────────────────────────────────────────────
_OPERATORS = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.Pow: op.pow,
    ast.USub: op.neg,
    ast.UAdd: op.pos,
    ast.Mod: op.mod,
    ast.FloorDiv: op.floordiv,
}


def _safe_eval(expr: str) -> float:
    """Evaluate a numeric expression without using eval()."""
    tree = ast.parse(expr.strip(), mode="eval")

    def _eval(node):
        if isinstance(node, ast.Expression):
            return _eval(node.body)
        elif isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
            return node.value
        elif isinstance(node, ast.BinOp):
            return _OPERATORS[type(node.op)](_eval(node.left), _eval(node.right))
        elif isinstance(node, ast.UnaryOp):
            return _OPERATORS[type(node.op)](_eval(node.operand))
        else:
            raise ValueError(f"Unsupported expression element: {type(node)}")

    return _eval(tree)


# ── Datetime tool ─────────────────────────────────────────────────────────────
def _datetime_answer() -> str:
    now = datetime.datetime.now()
    return (
        "📅 **Current Date & Time** (IST — Indian Standard Time)\n\n"
        f"- **Date:** {now.strftime('%d %B %Y')}\n"
        f"- **Day:** {now.strftime('%A')}\n"
        f"- **Time:** {now.strftime('%I:%M %p')}\n"
        f"- **Week:** Week {now.strftime('%U')} of {now.year}\n\n"
        "_This is the live system time on the server running this assistant._"
    )


# ── Calculator tool ───────────────────────────────────────────────────────────
def _calculator_answer(question: str) -> str:
    # Pattern 1: "X% of Y"
    pct_match = re.search(
        r"(\d+(?:\.\d+)?)\s*%\s*of\s*(\d+(?:\.\d+)?)", question, re.IGNORECASE
    )
    if pct_match:
        pct = float(pct_match.group(1))
        base = float(pct_match.group(2))
        result = (pct / 100) * base
        return (
            f"🔢 **Calculation Result**\n\n"
            f"**{pct}% of {base}** = **{result:.4g}**"
        )

    # Pattern 2: Extract numeric expression from the question
    # Strip common English words and keep math chars
    expr = re.sub(r"[^0-9+\-*/().\s%]", " ", question)
    expr = re.sub(r"\s+", " ", expr).strip()

    # Handle standalone "X % Y" (modulo)
    try:
        result = _safe_eval(expr)
        return (
            f"🔢 **Calculation Result**\n\n"
            f"**{expr}** = **{result:.6g}**"
        )
    except Exception:
        pass

    return (
        "⚠️ I couldn't extract a valid mathematical expression from your question.\n\n"
        "Please rephrase it clearly. Examples:\n"
        "- _Calculate 15% of 400_\n"
        "- _What is 2 ** 10?_\n"
        "- _Compute (45 + 12) * 3_"
    )


# ── Node ──────────────────────────────────────────────────────────────────────
def tool_node(state: AgentState) -> dict:
    """Dispatch to the appropriate tool based on the route."""
    route = state.get("route", "")
    question = state.get("question", "")

    if route == "tool_datetime":
        answer = _datetime_answer()
    elif route == "tool_calculator":
        answer = _calculator_answer(question)
    else:
        # Fallback: try to guess
        q_lower = question.lower()
        if any(w in q_lower for w in ("time", "date", "day", "today", "year")):
            answer = _datetime_answer()
        else:
            answer = _calculator_answer(question)

    return {"answer": answer, "source_docs": []}
