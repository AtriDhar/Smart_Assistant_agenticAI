"""
Retriever Node — fetches relevant chunks from the FAISS vector store.
Uses a singleton vectorstore to avoid reloading on every question.
"""
from __future__ import annotations

import os
from pathlib import Path

from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings

from agent.state import AgentState

_BASE_DIR = Path(__file__).resolve().parent.parent
_VS_PATH = str(_BASE_DIR / "vector_store")

_vectorstore: FAISS | None = None


def _get_vectorstore() -> FAISS:
    """Lazy-load and cache the FAISS vectorstore."""
    global _vectorstore
    if _vectorstore is None:
        embeddings = GoogleGenerativeAIEmbeddings(
            model="gemini-embedding-001",
            google_api_key=os.getenv("GOOGLE_API_KEY"),
        )
        _vectorstore = FAISS.load_local(
            _VS_PATH,
            embeddings,
            allow_dangerous_deserialization=True,
        )
    return _vectorstore


def get_retriever(k: int = 5):
    """Return a retriever instance (used by tests)."""
    return _get_vectorstore().as_retriever(search_kwargs={"k": k})


def retriever_node(state: AgentState) -> dict:
    """
    Retrieve top-k documents from the vector store.
    On retry (retry_count > 0), expands k to 7 for broader coverage.
    """
    retry_count = state.get("retry_count", 0)
    k = 7 if retry_count > 0 else 5

    retriever = _get_vectorstore().as_retriever(search_kwargs={"k": k})
    docs = retriever.invoke(state["question"])

    return {"retrieved_docs": docs}
