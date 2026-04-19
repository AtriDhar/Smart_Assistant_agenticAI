"""
Typed State definition for the Smart Student Assistant LangGraph agent.
"""
from __future__ import annotations

import operator
from typing import Annotated, List, TypedDict

from langchain_core.documents import Document
from langchain_core.messages import BaseMessage


class AgentState(TypedDict):
    """
    Single source-of-truth for the agent graph.

    Fields
    ------
    messages        : Conversation history (human + AI turns). Accumulated via operator.add.
    question        : The current user question being processed.
    retrieved_docs  : Raw documents retrieved from FAISS.
    filtered_docs   : Documents that passed the relevance-grader.
    answer          : Final answer string to return to the user.
    route           : Routing decision — "rag" | "tool_datetime" | "tool_calculator" | "out_of_scope"
    tool_name       : Active tool name (populated when route starts with "tool_").
    faithfulness_ok : Whether the evaluator approved the answer.
    retry_count     : Number of times the retriever has been called for this question.
    source_docs     : Filenames of source documents used for the answer.
    """

    messages: Annotated[List[BaseMessage], operator.add]
    question: str
    retrieved_docs: List[Document]
    filtered_docs: List[Document]
    answer: str
    route: str
    tool_name: str
    faithfulness_ok: bool
    retry_count: int
    source_docs: List[str]
