"""
Smart Student Assistant — Streamlit UI
B.Tech CSCE | KIIT University | 2023-2027 Batch

Powered strictly by Google Gemini.
Run: streamlit run app.py
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

# ── Bootstrap ────────────────────────────────────────────────────────────────
sys.path.insert(0, str(Path(__file__).resolve().parent))

from dotenv import load_dotenv
load_dotenv()

import streamlit as st

# ── Page Config  (must be first Streamlit call) ──────────────────────────────
st.set_page_config(
    page_title="Smart Student Assistant | KIIT CSCE",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

/* ── Base ── */
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    background: #0D1117;
    color: #E6EDF3;
}

/* ── Hide default Streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 1.5rem; padding-bottom: 3rem; }

/* ── Header banner ── */
.header-band {
    background: linear-gradient(135deg, #1c2334 0%, #0d1117 50%, #161b27 100%);
    border-bottom: 1px solid rgba(99, 102, 241, 0.35);
    padding: 1rem 1.5rem;
    margin-bottom: 1.25rem;
    border-radius: 12px;
    position: relative;
    overflow: hidden;
}
.header-band::before {
    content: '';
    position: absolute;
    top: 0; left: -100%;
    width: 200%; height: 100%;
    background: linear-gradient(90deg, transparent, rgba(129,140,248,0.06), transparent);
    animation: shimmer 4s infinite;
}
@keyframes shimmer { 100% { transform: translateX(50%); } }
.header-band h1 {
    font-size: 1.6rem;
    font-weight: 700;
    background: linear-gradient(90deg, #818CF8, #A78BFA, #C084FC);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin: 0;
}
.header-band p { color: #8B949E; font-size: 0.82rem; margin: 0.25rem 0 0; }

/* ── Chat bubbles ── */
.bubble-user {
    background: linear-gradient(135deg, #1d2d50, #243b5e);
    border: 1px solid rgba(99,102,241,0.3);
    border-radius: 16px 16px 4px 16px;
    padding: 0.85rem 1.1rem;
    margin: 0.5rem 0 0.5rem 3rem;
    color: #C9D1D9;
    font-size: 0.93rem;
    line-height: 1.55;
    box-shadow: 0 2px 12px rgba(0,0,0,0.3);
}
.bubble-ai {
    background: linear-gradient(135deg, #131d2e, #1a2640);
    border: 1px solid rgba(167,139,250,0.25);
    border-radius: 16px 16px 16px 4px;
    padding: 0.85rem 1.1rem;
    margin: 0.5rem 3rem 0.5rem 0;
    color: #E6EDF3;
    font-size: 0.93rem;
    line-height: 1.6;
    box-shadow: 0 2px 12px rgba(0,0,0,0.3);
}
.bubble-label-user { text-align: right; font-size: 0.72rem; color: #6366F1; font-weight: 600; margin-bottom: 2px; }
.bubble-label-ai   { text-align: left;  font-size: 0.72rem; color: #A78BFA; font-weight: 600; margin-bottom: 2px; }

/* ── Route badge ── */
.route-badge {
    display: inline-block; padding: 2px 9px; border-radius: 20px;
    font-size: 0.68rem; font-weight: 600; margin-left: 6px; vertical-align: middle;
}
.route-rag        { background: #0e3d2b; color: #34D399; border: 1px solid #34D39944; }
.route-tool       { background: #1c2d4a; color: #60A5FA; border: 1px solid #60A5FA44; }
.route-oos        { background: #3a1a1a; color: #F87171; border: 1px solid #F8717144; }

/* ── Source pill ── */
.source-pill {
    display: inline-block; background: #1e2a40; border: 1px solid #30363d;
    border-radius: 6px; padding: 2px 8px; font-size: 0.68rem; color: #8B949E;
    margin: 2px 3px; font-family: 'Courier New', monospace;
}

/* ── Sidebar styling ── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0d1117 0%, #131922 100%);
    border-right: 1px solid rgba(48,54,61,0.8);
}
[data-testid="stSidebar"] .stMarkdown p { font-size: 0.82rem; color: #8B949E; }

/* ── Input box ── */
[data-testid="stChatInputTextArea"] {
    background: #161b27 !important;
    border: 1px solid rgba(99,102,241,0.4) !important;
    border-radius: 12px !important;
    color: #E6EDF3 !important;
    font-family: 'Inter', sans-serif !important;
}

/* ── Expander ── */
[data-testid="stExpander"] {
    background: #0d1117;
    border: 1px solid #21262d;
    border-radius: 8px;
}

/* ── Scrollable chat area ── */
.chat-container { max-height: 62vh; overflow-y: auto; padding-right: 4px; }
.chat-container::-webkit-scrollbar { width: 5px; }
.chat-container::-webkit-scrollbar-track { background: transparent; }
.chat-container::-webkit-scrollbar-thumb { background: #30363d; border-radius: 10px; }

/* ── Loading spinner ── */
.stSpinner > div { border-top-color: #818CF8 !important; }

/* ── Welcome card ── */
.welcome-card {
    background: linear-gradient(135deg, #131922, #1a243a);
    border: 1px dashed rgba(99,102,241,0.4);
    border-radius: 14px;
    padding: 1.5rem;
    text-align: center;
    margin: 1rem 0;
    position: relative;
    overflow: hidden;
}
.welcome-card::before {
    content: '';
    position: absolute;
    top: -50%; left: -50%;
    width: 200%; height: 200%;
    background: radial-gradient(circle, rgba(99,102,241,0.04) 0%, transparent 70%);
    animation: pulse-bg 5s ease-in-out infinite;
}
@keyframes pulse-bg {
    0%, 100% { transform: scale(1); opacity: 0.5; }
    50% { transform: scale(1.1); opacity: 1; }
}
.welcome-card h3 { color: #A78BFA; font-size: 1.1rem; margin-bottom: 0.5rem; position: relative; }
.welcome-card p  { color: #8B949E; font-size: 0.83rem; position: relative; }
.suggestion-btn { color: #818CF8; background: #1d2d50; border: 1px solid #6366F133;
    border-radius: 8px; padding: 5px 12px; font-size: 0.78rem; margin: 3px; display:inline-block;
    transition: all 0.2s ease; cursor: default; }
.suggestion-btn:hover {
    background: #263a5e; border-color: #6366F166;
    transform: translateY(-1px); box-shadow: 0 2px 8px rgba(99,102,241,0.2);
}

/* ── Provider status ── */
.provider-badge {
    display: inline-block; padding: 3px 10px; border-radius: 20px;
    font-size: 0.7rem; font-weight: 600;
}
.provider-gemini { background: #2d1a3a; color: #c084fc; border: 1px solid #c084fc44; }
.provider-none   { background: #3a1a1a; color: #f87171; border: 1px solid #f8717144; }

/* ── Footer ── */
.app-footer {
    text-align: center; padding: 1rem 0 0.5rem;
    font-size: 0.7rem; color: #484f58;
    border-top: 1px solid #21262d;
    margin-top: 2rem;
}
.app-footer a { color: #6366F1; text-decoration: none; }
</style>
""",
    unsafe_allow_html=True,
)

# ── Helper: ensure vector store exists ───────────────────────────────────────
VS_PATH = Path(__file__).resolve().parent / "vector_store"


def _effective_google_key() -> str:
    """Return an API key without exposing secret values in visible inputs."""
    return (
        st.session_state.get("google_api_key", "")
        or st.session_state.get("runtime_google_api_key", "")
        or ""
    )

def _ensure_index():
    if not VS_PATH.exists() or not any(VS_PATH.iterdir()):
        with st.spinner("🔧 Building knowledge base index for the first time (< 2 min)…"):
            from scripts.build_index import build_index
            build_index()
        st.success("✅ Knowledge base ready!", icon="🎉")


# ── Session state init ────────────────────────────────────────────────────────
def _init_session():
    # Keep env-provided key internal so it is never shown in UI inputs.
    if "runtime_google_api_key" not in st.session_state:
        st.session_state.runtime_google_api_key = (
            os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY") or ""
        )

    # Session-entered key (intentionally starts blank in the UI).
    if "google_api_key" not in st.session_state:
        st.session_state.google_api_key = ""

    if "graph" not in st.session_state:
        # Avoid building graph if no key exists, as it fails embeddings
        if _effective_google_key():
            _ensure_index()
            from agent.graph import get_graph
            st.session_state.graph = get_graph()
        else:
            st.session_state.graph = None

    if "messages" not in st.session_state:
        st.session_state.messages = []          # conversation history (BaseMessage list)

    if "chat_display" not in st.session_state:
        st.session_state.chat_display = []      # list of dicts for UI rendering

    if "last_sources" not in st.session_state:
        st.session_state.last_sources = []

    if "last_route" not in st.session_state:
        st.session_state.last_route = ""


# ── Route badge HTML ──────────────────────────────────────────────────────────
def _route_badge(route: str) -> str:
    if route == "rag":
        return '<span class="route-badge route-rag">📚 RAG</span>'
    elif route.startswith("tool"):
        return '<span class="route-badge route-tool">🛠️ Tool</span>'
    elif route == "out_of_scope":
        return '<span class="route-badge route-oos">🚫 Out of Scope</span>'
    return ""


# ── Process a user question ───────────────────────────────────────────────────
def _process(question: str):
    graph = st.session_state.graph
    
    if not graph:
        # Re-attempt building graph if key was just added
        if _effective_google_key():
            _ensure_index()
            from agent.graph import get_graph
            st.session_state.graph = get_graph()
            graph = st.session_state.graph
        else:
            st.error("Google API Key missing. Set it in Streamlit Secrets or provide it in the sidebar.")
            return

    # Build the state for this turn (carry forward message history)
    state = {
        "messages": st.session_state.messages,
        "question": question,
        "retrieved_docs": [],
        "filtered_docs": [],
        "answer": "",
        "route": "",
        "tool_name": "",
        "faithfulness_ok": False,
        "retry_count": 0,
        "source_docs": [],
    }

    try:
        result = graph.invoke(state)
    except Exception as exc:
        err = str(exc)
        if "NOT_FOUND" in err and "model" in err.lower():
            fallback = (
                "⚠️ The configured Gemini chat model is not available for this API endpoint.\n\n"
                "Check your model setting in the environment and restart."
            )
        elif "RESOURCE_EXHAUSTED" in err or "429" in err:
            fallback = (
                "⚠️ API quota is temporarily exhausted.\n\n"
                "Please wait for quota reset, then retry."
            )
        elif "API_KEY_INVALID" in err or "API key not valid" in err or "authentication" in err.lower():
            fallback = (
                "⚠️ API key error. Please verify Streamlit Secrets (or sidebar key if entered)."
            )
        else:
            fallback = (
                "⚠️ The assistant encountered an error while processing your question.\n\n"
                "Please retry."
            )

        result = {
            "messages": st.session_state.messages,
            "answer": fallback,
            "route": "out_of_scope",
            "source_docs": [],
        }

    # Update persistent message history
    st.session_state.messages = result["messages"]

    # Save display record
    st.session_state.chat_display.append(
        {
            "role": "user",
            "content": question,
        }
    )
    st.session_state.chat_display.append(
        {
            "role": "assistant",
            "content": result.get("answer", ""),
            "route": result.get("route", ""),
            "sources": result.get("source_docs", []),
        }
    )
    st.session_state.last_sources = result.get("source_docs", [])
    st.session_state.last_route = result.get("route", "")


# ═══════════════════════════════════════════════════════════════════════════════
#  SIDEBAR
# ═══════════════════════════════════════════════════════════════════════════════
def _render_sidebar():
    with st.sidebar:
        st.markdown(
            """
<div style="text-align:center; padding: 0.5rem 0 1rem;">
  <div style="font-size:2.8rem;">🎓</div>
  <div style="font-size:1.05rem; font-weight:700; color:#A78BFA;">Smart Student<br>Assistant</div>
  <div style="font-size:0.72rem; color:#8B949E; margin-top:4px;">KIIT University · B.Tech CSCE</div>
</div>
""",
            unsafe_allow_html=True,
        )

        st.divider()

        # ── API Key Inputs ───────────────────────────────────────────────────
        st.markdown("**🔑 API Key Configuration**")

        google_key = st.text_input(
            "Google Gemini API Key",
            type="password",
            placeholder="AIza...",
            key="google_key_input",
            help="Optional: this is stored only in current session. For deployment, set Streamlit Secrets instead.",
        )
        if google_key != st.session_state.get("google_api_key", ""):
            st.session_state.google_api_key = google_key
            os.environ["GOOGLE_API_KEY"] = google_key
            
            # Immediately try to reconstruct graph with new key
            _ensure_index()
            from agent.graph import build_graph
            st.session_state.graph = build_graph()
            st.rerun()

        # ── Connection Status ────────────────────────────────────────────────
        if _effective_google_key():
            model_name = os.getenv("GEMINI_CHAT_MODEL", "gemini-2.5-flash")
            st.markdown(
                f'<div style="margin-top:4px;">'
                f'<span class="provider-badge provider-gemini">⚡ Gemini ({model_name})</span>'
                f'</div>',
                unsafe_allow_html=True,
            )
            if st.session_state.get("runtime_google_api_key") and not st.session_state.get("google_api_key"):
                st.caption("Using secure environment/Secrets configuration. API key is hidden.")
        else:
            st.markdown(
                f'<div style="margin-top:4px;">'
                f'<span class="provider-badge provider-none">❌ Not configured</span>'
                f'</div>',
                unsafe_allow_html=True,
            )

        st.divider()

        # ── Knowledge Base Topics ────────────────────────────────────────────
        st.markdown("**📚 Knowledge Base Topics**")
        topics = [
            ("01", "Course Overview & Program Structure"),
            ("02", "Unit 1 — Data Structures & Algorithms"),
            ("03", "Unit 2 — Operating Systems"),
            ("04", "Unit 3 — Database Management Systems"),
            ("05", "Unit 4 — Computer Networks"),
            ("06", "Unit 5 — Software Engineering"),
            ("07", "Semester Syllabus Details"),
            ("08", "Examination Rules & Regulations"),
            ("09", "Assignment & Plagiarism Policy"),
            ("10", "Revision Tips & Study Strategies"),
            ("11", "Frequently Asked Questions"),
            ("12", "Grading Rubric & GPA Calculation"),
        ]
        for num, name in topics:
            st.markdown(
                f'<div style="font-size:0.77rem; color:#8B949E; padding:2px 0;">'
                f'<span style="color:#6366F1; font-weight:600;">{num}</span> {name}</div>',
                unsafe_allow_html=True,
            )

        st.divider()

        st.markdown("**🔧 Tools Available**")
        st.markdown(
            '<div style="font-size:0.78rem; color:#8B949E;">'
            "📅 <b style='color:#60A5FA'>Date &amp; Time</b> — current IST time<br>"
            "🔢 <b style='color:#60A5FA'>Calculator</b> — math &amp; percentages"
            "</div>",
            unsafe_allow_html=True,
        )

        st.divider()

        # Last answer sources
        if st.session_state.get("last_sources"):
            st.markdown("**📎 Sources (last answer)**")
            for src in st.session_state.last_sources:
                st.markdown(
                    f'<span class="source-pill">{src}</span>',
                    unsafe_allow_html=True,
                )

        st.divider()

        # How it works
        with st.expander("⚙️ How It Works", expanded=False):
            st.markdown(
                """
<div style="font-size:0.76rem; color:#8B949E; line-height:1.7;">
<b style="color:#A78BFA">1. Router</b> — classifies your intent<br>
<b style="color:#A78BFA">2. Retriever</b> — finds relevant chunks from the FAISS index<br>
<b style="color:#A78BFA">3. Grader</b> — filters irrelevant documents<br>
<b style="color:#A78BFA">4. Generator</b> — creates a grounded answer<br>
<b style="color:#A78BFA">5. Evaluator</b> — checks answer faithfulness<br>
<b style="color:#A78BFA">6. Memory</b> — saves the exchange for follow-ups<br>
<br>
Built with <b>LangGraph</b>, <b>FAISS</b>, <b>Google Gemini</b>, <b>Streamlit</b>
</div>
""",
                unsafe_allow_html=True,
            )

        # Clear button
        st.divider()
        if st.button("🗑️ Clear Chat", use_container_width=True):
            st.session_state.chat_display = []
            st.session_state.messages = []
            st.session_state.last_sources = []
            st.session_state.last_route = ""
            st.rerun()


# ═══════════════════════════════════════════════════════════════════════════════
#  MAIN AREA
# ═══════════════════════════════════════════════════════════════════════════════
def _render_main():
    # Header
    st.markdown(
        """
<div class="header-band">
  <h1>🎓 Smart Student Assistant</h1>
    <p>B.Tech CSCE · KIIT University · Powered by RAG + LangGraph + Google Gemini</p>
</div>
""",
        unsafe_allow_html=True,
    )

    # ── API key warning ───────────────────────────────────────────────────────
    if not _effective_google_key():
        st.warning("⚠️ Google API Key required! Set Streamlit Secrets (or enter one in the sidebar) to start.", icon="🔑")

    # ── Chat display ──────────────────────────────────────────────────────────
    chat = st.session_state.chat_display

    if not chat:
        # Welcome card
        st.markdown(
            """
<div class="welcome-card">
  <h3>👋 Hello! I'm your Academic Assistant</h3>
  <p>I can answer questions about your B.Tech CSCE coursework, exams, assignments, grading, 
  and more — all from your uploaded course materials.<br><br>
  <b>Try asking me:</b></p>
  <span class="suggestion-btn">📋 What is my minimum attendance?</span>
  <span class="suggestion-btn">📚 Explain AVL tree rotations</span>
  <span class="suggestion-btn">📅 What day is today?</span>
  <span class="suggestion-btn">📊 What grade is 80 marks?</span>
  <span class="suggestion-btn">🧮 Calculate 15% of 350</span>
</div>
""",
            unsafe_allow_html=True,
        )
    else:
        # Render all turns
        for turn in chat:
            if turn["role"] == "user":
                st.markdown(
                    f'<div class="bubble-label-user">You</div>'
                    f'<div class="bubble-user">{turn["content"]}</div>',
                    unsafe_allow_html=True,
                )
            else:
                route_html = _route_badge(turn.get("route", ""))
                sources = turn.get("sources", [])
                source_html = ""
                if sources:
                    pills = "".join(f'<span class="source-pill">📎 {s}</span>' for s in sources)
                    source_html = f'<div style="margin-top:6px;">{pills}</div>'

                answer_html = turn["content"].replace("\n", "<br>")
                st.markdown(
                    f'<div class="bubble-label-ai">Assistant {route_html}</div>'
                    f'<div class="bubble-ai">{answer_html}{source_html}</div>',
                    unsafe_allow_html=True,
                )

    # ── Chat input ────────────────────────────────────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    question = st.chat_input(
        "Ask anything about your B.Tech CSCE course, exams, or try 'What time is it?'"
    )

    if question:
        if not _effective_google_key():
            st.error("Google API Key missing. Set Streamlit Secrets (or provide it in the sidebar).", icon="🔑")
        else:
            with st.spinner("🤔 Thinking…"):
                _process(question)
            st.rerun()

    # ── Footer ────────────────────────────────────────────────────────────────
    st.markdown(
        """
<div class="app-footer">
  Smart Student Assistant v2.0 · Built with ❤️ at KIIT University · 
  <a href="https://github.com">Source</a>
</div>
""",
        unsafe_allow_html=True,
    )


# ═══════════════════════════════════════════════════════════════════════════════
#  ENTRY POINT
# ═══════════════════════════════════════════════════════════════════════════════
_init_session()
_render_sidebar()
_render_main()
