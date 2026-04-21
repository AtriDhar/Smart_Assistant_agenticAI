"""Shared LLM configuration strictly using Google Gemini."""
from __future__ import annotations

import os

from langchain_google_genai import ChatGoogleGenerativeAI


def _get_google_key() -> str | None:
    """Get Google API key from session state or env."""
    try:
        import streamlit as st
        if hasattr(st, "session_state") and st.session_state.get("google_api_key"):
            return st.session_state.google_api_key
    except Exception:
        pass
    return os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")


def get_chat_llm(*, temperature: float = 0.0) -> ChatGoogleGenerativeAI:
    """
    Return a configured Gemini chat model.

    Environment override:
      GEMINI_CHAT_MODEL=gemini-2.5-flash
    """
    api_key = _get_google_key()
    if not api_key:
        raise EnvironmentError(
            "No Google API key configured. Set GOOGLE_API_KEY or GEMINI_API_KEY "
            "in .env or enter it in the sidebar."
        )

    model = os.getenv("GEMINI_CHAT_MODEL", "gemini-2.5-flash")
    return ChatGoogleGenerativeAI(
        model=model,
        temperature=temperature,
        google_api_key=api_key,
    )
