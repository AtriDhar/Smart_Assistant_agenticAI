# Smart Student Assistant for Course Notes and Academic FAQs

> **Capstone Project | Agentic AI | KIIT University**
> Student: **Atri Dhar** | Roll: **2329023** | B.Tech CSCE 2023-2027

## Overview

A production-ready Retrieval-Augmented Generation (RAG) academic assistant for B.Tech CSCE students at KIIT University.
Built with LangGraph, Google Gemini 1.5 Flash, FAISS, and Streamlit.

The assistant answers questions about syllabus, unit notes, exam rules, assignments, grading, and more, grounded in a curated 12-document knowledge base with anti-hallucination checks.

## Architecture

```text
START -> Router -> rag        -> Retriever -> Grader -> Generator -> Evaluator
                                    | faithful?
                                YES -> Memory -> END
                                NO  -> Retriever (retry <= 2)
          -> tool_*      -> Tool -> Memory -> END
          -> out_of_scope-> Generator -> Memory -> END
```

LangGraph nodes: Router, Retriever, Grader, Generator, Evaluator, Tool, Memory

## Knowledge Base (12 Documents)

| # | File | Topic |
|---|------|-------|
| 01 | `01_course_overview.txt` | B.Tech CSCE program structure and outcomes |
| 02 | `02_unit1_notes.txt` | Data Structures and Algorithms |
| 03 | `03_unit2_notes.txt` | Operating Systems |
| 04 | `04_unit3_notes.txt` | Database Management Systems |
| 05 | `05_unit4_notes.txt` | Computer Networks |
| 06 | `06_unit5_notes.txt` | Software Engineering |
| 07 | `07_syllabus_details.txt` | Semester-wise detailed syllabus |
| 08 | `08_exam_rules.txt` | Examination rules and hall ticket policy |
| 09 | `09_assignment_policy.txt` | Assignment and plagiarism policy |
| 10 | `10_revision_tips.txt` | Study strategies and revision tips |
| 11 | `11_faqs.txt` | Frequently asked questions |
| 12 | `12_grading_rubric.txt` | Grading scale, GPA, passing criteria |

## Quick Start

### Prerequisites

- Python 3.10+
- Google Gemini API key (from https://aistudio.google.com)

### Setup

```bash
# 1) Enter project directory
cd capstone

# 2) Create and activate virtual environment
python -m venv .venv
.venv\Scripts\activate

# 3) Install dependencies
pip install -r requirements.txt

# 4) Add API key
# Create .env and set GOOGLE_API_KEY=<your-key>

# 5) Build FAISS index
python scripts/build_index.py

# 6) Run retrieval tests
pytest scripts/test_retrieval.py -v

# 7) Launch Streamlit app
streamlit run app.py
```

### Generate PDF Report

```bash
python docs/generate_report.py
```

Output file: `docs/capstone_report.pdf`

### Deployment Guide

See full deployment instructions in `docs/DEPLOYMENT.md`.

## Project Structure

```text
capstone/
|-- knowledge_base/          # 12 topic-specific .txt documents
|-- vector_store/            # FAISS index (generated after build)
|-- agent/
|   |-- state.py             # Typed AgentState (TypedDict)
|   |-- router.py            # Router node + conditional edges
|   |-- retriever.py         # FAISS retrieval node (lazy singleton)
|   |-- grader.py            # Document relevance grader node
|   |-- generator.py         # Grounded answer generator node
|   |-- evaluator.py         # Faithfulness evaluator node
|   |-- tools.py             # Datetime and safe calculator tools
|   |-- memory.py            # Conversation memory node
|   `-- graph.py             # LangGraph StateGraph assembly
|-- scripts/
|   |-- build_index.py       # FAISS index builder
|   `-- test_retrieval.py    # pytest retrieval quality suite (15 tests)
|-- docs/
|   |-- generate_report.py   # ReportLab PDF generator
|   |-- DEPLOYMENT.md        # Step-by-step deployment guide
|   `-- capstone_report.pdf  # Generated 4-5 page report
|-- app.py                   # Streamlit UI entry point
|-- requirements.txt
|-- Procfile                 # Web start command (Render/Procfile platforms)
|-- runtime.txt              # Pinned Python version for cloud builds
|-- .streamlit/config.toml   # Streamlit server/theme config
|-- .env.example
`-- README.md
```

## Tech Stack

| Layer | Technology |
|---|---|
| Agent Framework | LangGraph (StateGraph) |
| LLM | Google Gemini 1.5 Flash |
| Embeddings | Google gemini-embedding-001 |
| Vector Store | FAISS (CPU, local) |
| Memory | LangGraph AgentState (`operator.add`) |
| UI | Streamlit |
| PDF | ReportLab |
| Testing | pytest |

## Features

- RAG-grounded answers with source document attribution
- Faithfulness evaluation loop with retry (max 2)
- Session memory for follow-up questions
- Tool routing for current date/time and calculations
- Graceful out-of-scope handling
- Retrieval quality checks with 15 pytest tests
- PDF report generation with ReportLab

## License

MIT License (educational/capstone use)
