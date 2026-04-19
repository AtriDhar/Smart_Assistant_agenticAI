"""
generate_report.py — Generates the 4-5 page PDF capstone report using ReportLab.

Usage:
    python docs/generate_report.py
Output: docs/capstone_report.pdf
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import (
    HRFlowable,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

# ── Student Details ───────────────────────────────────────────────────────────
STUDENT_NAME    = "Atri Dhar"
ROLL_NUMBER     = "2329023"
BATCH_PROGRAM   = "B.Tech CSCE, 2023–2027"
INSTITUTION     = "KIIT University, Bhubaneswar, Odisha"
SUBJECT         = "Agentic AI — Capstone Project"
DATE            = "April 2026"

# ── Colors ────────────────────────────────────────────────────────────────────
INDIGO      = colors.HexColor("#4F46E5")
VIOLET      = colors.HexColor("#7C3AED")
DARK_BG     = colors.HexColor("#0F172A")
LIGHT_GRAY  = colors.HexColor("#F1F5F9")
MID_GRAY    = colors.HexColor("#64748B")
BLACK       = colors.black
WHITE       = colors.white

OUT_PATH = Path(__file__).resolve().parent / "capstone_report.pdf"


def build_styles():
    base = getSampleStyleSheet()
    styles = {}

    styles["cover_title"] = ParagraphStyle(
        "cover_title", fontSize=22, leading=28, alignment=TA_CENTER,
        textColor=INDIGO, fontName="Helvetica-Bold", spaceAfter=10,
    )
    styles["cover_subtitle"] = ParagraphStyle(
        "cover_subtitle", fontSize=13, leading=18, alignment=TA_CENTER,
        textColor=BLACK, fontName="Helvetica", spaceAfter=6,
    )
    styles["cover_meta"] = ParagraphStyle(
        "cover_meta", fontSize=10, leading=15, alignment=TA_CENTER,
        textColor=MID_GRAY, fontName="Helvetica",
    )
    styles["section_heading"] = ParagraphStyle(
        "section_heading", fontSize=13, leading=18, alignment=TA_LEFT,
        textColor=INDIGO, fontName="Helvetica-Bold", spaceBefore=14, spaceAfter=6,
    )
    styles["sub_heading"] = ParagraphStyle(
        "sub_heading", fontSize=10.5, leading=14, alignment=TA_LEFT,
        textColor=VIOLET, fontName="Helvetica-Bold", spaceBefore=8, spaceAfter=4,
    )
    styles["body"] = ParagraphStyle(
        "body", fontSize=9.5, leading=14.5, alignment=TA_JUSTIFY,
        textColor=BLACK, fontName="Helvetica", spaceAfter=5,
    )
    styles["bullet"] = ParagraphStyle(
        "bullet", fontSize=9.5, leading=14, alignment=TA_LEFT,
        textColor=BLACK, fontName="Helvetica", leftIndent=14, spaceAfter=3,
        bulletIndent=4, bulletFontName="Helvetica",
    )
    styles["code"] = ParagraphStyle(
        "code", fontSize=8.5, leading=12, alignment=TA_LEFT,
        textColor=colors.HexColor("#1E293B"), fontName="Courier",
        backColor=LIGHT_GRAY, borderPadding=(4, 6, 4, 6), spaceAfter=6,
    )
    styles["caption"] = ParagraphStyle(
        "caption", fontSize=8, leading=11, alignment=TA_CENTER,
        textColor=MID_GRAY, fontName="Helvetica-Oblique",
    )
    return styles


def hr(color=INDIGO, thickness=1):
    return HRFlowable(width="100%", thickness=thickness, color=color, spaceAfter=8, spaceBefore=4)


def h(txt, style): return Paragraph(txt, style)
def sp(n=6): return Spacer(1, n)


def build_pdf():
    S = build_styles()
    doc = SimpleDocTemplate(
        str(OUT_PATH), pagesize=A4,
        leftMargin=2.2*cm, rightMargin=2.2*cm,
        topMargin=2.2*cm, bottomMargin=2.2*cm,
        title="Smart Student Assistant — Capstone Report",
        author=STUDENT_NAME,
    )
    story = []

    # ═══════════════════════════════════════════════════════════════
    # PAGE 1: COVER
    # ═══════════════════════════════════════════════════════════════
    story += [
        sp(60),
        h("🎓 Smart Student Assistant", S["cover_title"]),
        h("for Course Notes and Academic FAQs", S["cover_subtitle"]),
        sp(4),
        hr(INDIGO, 1.5),
        sp(10),
        h("<b>Capstone Project Report</b>", S["cover_subtitle"]),
        sp(20),
        h(f"<b>Student Name :</b>  {STUDENT_NAME}", S["cover_meta"]),
        h(f"<b>Roll Number   :</b>  {ROLL_NUMBER}", S["cover_meta"]),
        h(f"<b>Program       :</b>  {BATCH_PROGRAM}", S["cover_meta"]),
        h(f"<b>Institution   :</b>  {INSTITUTION}", S["cover_meta"]),
        h(f"<b>Subject       :</b>  {SUBJECT}", S["cover_meta"]),
        h(f"<b>Date          :</b>  {DATE}", S["cover_meta"]),
        sp(30),
        hr(VIOLET, 0.8),
        sp(10),
        h(
            "A Retrieval-Augmented Generation (RAG) academic assistant built with "
            "LangGraph, Google Gemini 1.5 Flash, FAISS, and Streamlit — designed to "
            "answer B.Tech CSCE student queries reliably and without hallucination.",
            S["cover_meta"],
        ),
        PageBreak(),
    ]

    # ═══════════════════════════════════════════════════════════════
    # PAGE 2: ABSTRACT + PROBLEM STATEMENT
    # ═══════════════════════════════════════════════════════════════
    story += [
        h("1. Abstract", S["section_heading"]),
        hr(),
        h(
            "The <b>Smart Student Assistant</b> is a production-grade Retrieval-Augmented Generation (RAG) "
            "system developed as a capstone project for the Agentic AI course at KIIT University. "
            "It is designed to serve B.Tech CSCE students by answering academic questions — covering "
            "syllabus, unit-wise course notes, examination rules, assignment policies, grading criteria, "
            "revision strategies, and frequently asked questions — with <b>zero hallucination</b>. "
            "The system grounds every answer exclusively in a curated 12-document knowledge base. "
            "When no relevant information is found, it explicitly says so rather than fabricating a response. "
            "The assistant remembers prior turns within a session, supports live tool calls (date/time, calculators), "
            "and uses a faithfulness evaluation loop to detect and correct hallucinated answers before presenting them.",
            S["body"],
        ),
        sp(8),

        h("2. Problem Statement", S["section_heading"]),
        hr(),
        h(
            "B.Tech students frequently encounter confusion about academic policies — minimum attendance "
            "thresholds, exam formats, assignment deadlines, grading scales, and subject-specific concepts. "
            "General-purpose AI chatbots (e.g., ChatGPT) are prone to hallucinating institution-specific "
            "facts such as exact mark distributions, specific exam rules, and internal policies. "
            "This causes distrust and can lead students to act on incorrect information. "
            "Existing academic portals present information as scattered static pages, without conversational "
            "access or follow-up capability.",
            S["body"],
        ),
        sp(4),
        h("<b>Core challenges addressed:</b>", S["sub_heading"]),
        h("• Preventing hallucination of marks, rules, and deadlines that do not exist.", S["bullet"]),
        h("• Enabling natural follow-up questions within a session using memory.", S["bullet"]),
        h("• Covering heterogeneous content types — notes, rules, FAQs, tips — in one interface.", S["bullet"]),
        h("• Providing tool-based answers (current date/time, arithmetic) alongside knowledge retrieval.", S["bullet"]),
        h("• Building an architecture that is auditable, testable, and deployable.", S["bullet"]),
        sp(8),

        h("3. Solution Overview & Key Features", S["section_heading"]),
        hr(),
        h(
            "The solution implements a <b>Corrective RAG</b> agent using <b>LangGraph</b> — a stateful, "
            "cyclic graph framework. The agent's typed state flows through seven specialised nodes, "
            "with conditional edges enabling dynamic routing, retry loops, and memory accumulation.",
            S["body"],
        ),

        sp(6),
        h("<b>Key Features:</b>", S["sub_heading"]),
        h("• <b>12-document curated knowledge base</b> covering all major B.Tech CSCE academic topics.", S["bullet"]),
        h("• <b>Faithfulness guard</b>: an evaluator node runs an LLM-as-judge check on every generated answer.", S["bullet"]),
        h("• <b>Corrective retry loop</b>: if the answer is not faithful, retrieval is expanded and re-attempted (max 2 retries).", S["bullet"]),
        h("• <b>Session memory</b>: conversation history carried across turns using LangGraph's annotated state.", S["bullet"]),
        h("• <b>Tool routing</b>: date/time and calculator queries bypass RAG entirely and are handled by safe tools.", S["bullet"]),
        h("• <b>Graceful refusal</b>: out-of-scope questions receive a polite, non-fabricated explanation of limitations.", S["bullet"]),
        h("• <b>Source attribution</b>: every RAG answer shows the source filename(s) it was generated from.", S["bullet"]),
        h("• <b>Streamlit UI</b>: styled dark-mode chat interface with route badges and source pills.", S["bullet"]),
        h("• <b>Pytest retrieval suite</b>: 15 tests validate retrieval quality before deployment.", S["bullet"]),
        PageBreak(),
    ]

    # ═══════════════════════════════════════════════════════════════
    # PAGE 3: ARCHITECTURE
    # ═══════════════════════════════════════════════════════════════
    story += [
        h("4. System Architecture", S["section_heading"]),
        hr(),
        h(
            "The agent is built as a <b>LangGraph StateGraph</b> with a typed <code>AgentState</code> "
            "TypedDict as the single source of truth. Each node reads from and writes to this state object.",
            S["body"],
        ),
        sp(6),

        h("<b>Graph Flow Diagram (textual)</b>", S["sub_heading"]),
        h(
            "START → [Router] → rag → [Retriever] → [Grader] → [Generator] → [Evaluator]\n"
            "                                                                      ↓ faithful?\n"
            "                                                          YES → [Memory] → END\n"
            "                                                          NO  → [Retriever] (retry ≤2)\n"
            "                 → tool_datetime/calculator → [Tool] → [Memory] → END\n"
            "                 → out_of_scope → [Generator] → [Memory] → END",
            S["code"],
        ),
        sp(6),

        h("<b>Node Descriptions</b>", S["sub_heading"]),
        h("• <b>Router Node</b>: Uses Gemini to classify intent into rag / tool_datetime / tool_calculator / out_of_scope.", S["bullet"]),
        h("• <b>Retriever Node</b>: Queries FAISS with top-5 (top-7 on retry) using Google gemini-embedding-001.", S["bullet"]),
        h("• <b>Grader Node</b>: LLM-based relevance grader filters out irrelevant chunks; fallback keeps top-3.", S["bullet"]),
        h("• <b>Generator Node</b>: Strict system prompt forces answers to be grounded in context only.", S["bullet"]),
        h("• <b>Evaluator Node</b>: LLM-as-judge faithfulness check; increments retry_count on failure.", S["bullet"]),
        h("• <b>Tool Node</b>: Handles datetime (live IST time) and safe calculator (no eval()) without KB.", S["bullet"]),
        h("• <b>Memory Node</b>: Appends HumanMessage + AIMessage to the messages list (operator.add).", S["bullet"]),
        sp(8),

        h("5. Tech Stack", S["section_heading"]),
        hr(),
        sp(4),
    ]

    # Tech stack table
    ts_data = [
        ["Layer", "Technology", "Purpose"],
        ["Agent Framework", "LangGraph 0.2+", "Stateful cyclic graph with typed state"],
        ["LLM", "Google Gemini 1.5 Flash", "Routing, grading, generation, evaluation"],
        ["Embeddings", "Google gemini-embedding-001", "Semantic vector encoding of knowledge chunks"],
        ["Vector Store", "FAISS (CPU)", "Similarity search over embedded chunks"],
        ["Memory", "LangGraph AgentState msgs", "Session-scoped conversation history"],
        ["UI", "Streamlit 1.39+", "Dark-mode chat interface with source display"],
        ["PDF Report", "ReportLab 4.0+", "Programmatic PDF generation"],
        ["Testing", "pytest 8.0+", "14 retrieval quality assertions"],
        ["Config", "python-dotenv", "Secret management via .env file"],
    ]
    ts_table = Table(ts_data, colWidths=[4*cm, 4.5*cm, 8*cm])
    ts_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), INDIGO),
        ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, 0), 9),
        ("FONTSIZE", (0, 1), (-1, -1), 8.5),
        ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
        ("BACKGROUND", (0, 1), (-1, -1), LIGHT_GRAY),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [LIGHT_GRAY, WHITE]),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#CBD5E1")),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
    ]))
    story += [ts_table, sp(8), PageBreak()]

    # ═══════════════════════════════════════════════════════════════
    # PAGE 4: IMPLEMENTATION + UNIQUE POINTS + FUTURE
    # ═══════════════════════════════════════════════════════════════
    story += [
        h("6. Implementation Details", S["section_heading"]),
        hr(),

        h("<b>Knowledge Base Construction</b>", S["sub_heading"]),
        h(
            "12 plain-text documents were authored specifically for this project, covering: "
            "B.Tech CSCE program overview, 5 unit-wise subject notes (DSA, OS, DBMS, Networks, SE), "
            "detailed semester syllabus, exam rules, assignment policy, revision tips, 32+ FAQs, and the "
            "grading rubric. Each document is 400–600 words of structured, factual content with "
            "headings, tables, and bullet points.",
            S["body"],
        ),

        h("<b>Index Construction (build_index.py)</b>", S["sub_heading"]),
        h("  1. Load all 12 .txt files using LangChain TextLoader with UTF-8 encoding.", S["bullet"]),
        h("  2. Attach metadata: source filename and human-readable topic name.", S["bullet"]),
        h("  3. Split with RecursiveCharacterTextSplitter (chunk_size=800, overlap=100).", S["bullet"]),
        h("  4. Embed in batches of 50 using Google gemini-embedding-001 (rate-limit aware).", S["bullet"]),
        h("  5. Save FAISS index to disk (vector_store/ directory).", S["bullet"]),

        h("<b>Retrieval Testing (test_retrieval.py)</b>", S["sub_heading"]),
        h(
            "15 pytest tests verify that 12 specific questions retrieve documents containing "
            "expected keywords, all retrieved documents carry metadata, and that the index is not "
            "contaminated across topics (e.g., a query about Belady's Anomaly should retrieve "
            "OS-related documents).",
            S["body"],
        ),

        h("<b>Hallucination Prevention</b>", S["sub_heading"]),
        h("• Generator prompt explicitly forbids using knowledge outside the provided context.", S["bullet"]),
        h("• Evaluator uses LLM-as-judge to verify every factual claim against the retrieved text.", S["bullet"]),
        h("• On failure: retry_count incremented; retriever expands k from 5→7 for broader coverage.", S["bullet"]),
        h("• Maximum 2 retries; after that, the best-effort answer is returned with the context note.", S["bullet"]),

        sp(8),
        h("7. Unique Points & Innovations", S["section_heading"]),
        hr(),
        h("• <b>Corrective RAG loop</b>: Unlike vanilla RAG, this system can detect and self-correct hallucinated answers.", S["bullet"]),
        h("• <b>LLM-as-judge faithfulness gate</b>: The evaluator node adds a quantifiable quality check to every RAG turn.", S["bullet"]),
        h("• <b>Typed AgentState with operator.add</b>: Proper persistent memory across multi-turn conversations.", S["bullet"]),
        h("• <b>Safe calculator (no eval())</b>: Uses Python AST parsing for secure expression evaluation.", S["bullet"]),
        h("• <b>Document grader node</b>: Reduces noise in context by filtering irrelevant retrieved chunks before generation.", S["bullet"]),
        h("• <b>Metadata-enriched chunks</b>: Every chunk knows its source file, enabling precise attribution.", S["bullet"]),
        h("• <b>Graceful out-of-scope handling</b>: Hard boundary — the system never extrapolates beyond its knowledge base.", S["bullet"]),

        sp(8),
        h("8. Future Improvements", S["section_heading"]),
        hr(),
        h("• <b>Hybrid search (BM25 + FAISS)</b>: Combine keyword and semantic search for better precision on specific terms.", S["bullet"]),
        h("• <b>Multi-university support</b>: Extend knowledge base to cover multiple institutions and programs.", S["bullet"]),
        h("• <b>PDF/DOCX ingestion</b>: Add support for parsing actual uploaded lecture slide PDFs.", S["bullet"]),
        h("• <b>LangSmith tracing</b>: Integrate observability to monitor retrieval quality and latency in production.", S["bullet"]),
        h("• <b>User feedback loop</b>: Allow students to rate answers (👍/👎); use feedback to improve retrieval.", S["bullet"]),
        h("• <b>Authentication</b>: Add student login to personalise responses (e.g., semester-specific content).", S["bullet"]),
        h("• <b>Mobile-first UI</b>: Wrap Streamlit in a PWA or build a React Native app for on-the-go access.", S["bullet"]),
        h("• <b>Summarisation agent</b>: Add a dedicated node to generate unit-wise revision summaries on demand.", S["bullet"]),

        sp(8),
        h("9. Conclusion", S["section_heading"]),
        hr(),
        h(
            "The Smart Student Assistant successfully demonstrates a production-ready RAG architecture "
            "with six key capabilities: retrieval from a structured knowledge base, document grading, "
            "grounded answer generation, faithfulness evaluation, session memory, and tool routing. "
            "The system fulfils all capstone requirements: a typed LangGraph state machine, a tested "
            "FAISS retrieval system, an anti-hallucination evaluator, conversation memory, tool routes, "
            "and a polished Streamlit interface. It is fully deployable, original, and clearly documented.",
            S["body"],
        ),
    ]

    doc.build(story)
    print(f"✅ PDF report generated: {OUT_PATH}")


if __name__ == "__main__":
    build_pdf()
