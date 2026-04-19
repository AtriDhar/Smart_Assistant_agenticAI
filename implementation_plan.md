# Smart Student Assistant — Capstone Implementation Plan

A RAG-based academic assistant for B.Tech students built with LangGraph, FAISS, Google Gemini, and Streamlit. All answers are grounded in a 12-document knowledge base; fabrication is actively prevented via a faithfulness evaluation node.

## Implementation Status

- Knowledge base: complete (12/12 documents present)
- Agent graph: complete (7 nodes wired with corrective retry loop)
- Streamlit UI: complete
- Tool routing: complete (datetime + calculator)
- Report generation: complete via `docs/generate_report.py`
- Retrieval tests: complete (`scripts/test_retrieval.py`, 15 tests)
- Vector index: generated in `vector_store/` after running `scripts/build_index.py`
- Deployment docs: complete (`docs/DEPLOYMENT.md`)
- Deployment files: complete (`Procfile`, `runtime.txt`, `.streamlit/config.toml`, `.gitignore`)

---

## Proposed Architecture Overview

```
User Question
     │
     ▼
[Router Node] ──────────────► [Tool Node]  (date/time, calculator)
     │                              │
     │ (RAG route)                  │
     ▼                              │
[Retrieval Node]                    │
     │                              │
     ▼                              │
[Document Grader Node]              │
     │ (relevant enough?)           │
     ▼                              │
[Answer Generation Node]            │
     │                              │
     ▼                              │
[Faithfulness Check Node] ◄─────────┘
     │  (hallucination detected?)
     │  yes → loop back to Retrieval (max 2 retries)
     │  no  ↓
[Save / Memory Node]
     │
     ▼
[Streamlit UI]
```

---

## Tech Stack

| Layer | Choice |
|---|---|
| Agent Framework | **LangGraph** (stateful cyclic graph) |
| LLM | **Google Gemini 1.5 Flash** (via `langchain-google-genai`) |
| Embeddings | **Google `gemini-embedding-001`** |
| Vector Store | **FAISS** (local, persisted to disk) |
| Memory | LangGraph `AgentState` with `messages` list (session-scoped) |
| UI | **Streamlit** |
| PDF generation | **ReportLab** |
| Testing | **pytest** |
| Packaging | ZIP + GitHub |

---

## Knowledge Base (12 Documents)

Each document is a carefully written `.txt` (or `.md`) file stored in `knowledge_base/`:

| # | Filename | Topic |
|---|---|---|
| 1 | `01_course_overview.txt` | Course structure, credits, outcomes |
| 2 | `02_unit1_notes.txt` | Unit 1 — Data Structures & Algorithms |
| 3 | `03_unit2_notes.txt` | Unit 2 — Operating Systems |
| 4 | `04_unit3_notes.txt` | Unit 3 — Database Management Systems |
| 5 | `05_unit4_notes.txt` | Unit 4 — Computer Networks |
| 6 | `06_unit5_notes.txt` | Unit 5 — Software Engineering |
| 7 | `07_syllabus_details.txt` | Full semester syllabus with weightage |
| 8 | `08_exam_rules.txt` | Examination rules, eligibility, hall ticket policy |
| 9 | `09_assignment_policy.txt` | Assignment deadlines, late submission, plagiarism |
| 10 | `10_revision_tips.txt` | Study strategies, revision schedule, memory techniques |
| 11 | `11_faqs.txt` | Frequently asked questions (30+ Q&A pairs) |
| 12 | `12_grading_rubric.txt` | Marks distribution, internal/external split, grade criteria |

---

## Project File Structure

```
capstone/
├── knowledge_base/               # 12 .txt documents
│   └── *.txt
├── vector_store/                 # FAISS index (auto-generated)
│   └── index.faiss / index.pkl
├── agent/
│   ├── __init__.py
│   ├── state.py                  # TypedDict AgentState
│   ├── router.py                 # Router node (RAG vs. tool)
│   ├── retriever.py              # Retrieval node + FAISS loader
│   ├── grader.py                 # Document relevance grader node
│   ├── generator.py              # Answer generation node
│   ├── evaluator.py              # Faithfulness check node
│   ├── tools.py                  # Tool node (datetime, calculator)
│   ├── memory.py                 # Save / memory node
│   └── graph.py                  # LangGraph StateGraph assembly
├── scripts/
│   ├── build_index.py            # One-time FAISS index builder
│   └── test_retrieval.py         # Retrieval quality tests (pytest)
├── app.py                        # Streamlit UI entry point
├── requirements.txt
├── .env.example
├── README.md
└── docs/
    └── capstone_report.pdf       # 4-5 page PDF documentation
```

---

## Proposed Changes

### Component 1 — Knowledge Base Documents
#### [NEW] `knowledge_base/` (12 .txt files)
Rich, realistic academic content covering all 12 topic areas above. Each file will contain 300–500 words of structured, factual content.

---

### Component 2 — Agent State & Graph
#### [NEW] `agent/state.py`
```python
class AgentState(TypedDict):
    messages: Annotated[List[BaseMessage], operator.add]
    question: str
    retrieved_docs: List[Document]
    answer: str
    route: str          # "rag" | "tool"
    tool_name: str      # "datetime" | "calculator" | ""
    faithfulness_ok: bool
    retry_count: int
    source_docs: List[str]
```

#### [NEW] `agent/graph.py`
LangGraph `StateGraph` wiring all 7 nodes with conditional edges.

---

### Component 3 — Index Builder
#### [NEW] `scripts/build_index.py`
Loads all 12 `.txt` files → chunks with `RecursiveCharacterTextSplitter` (chunk_size=800, overlap=100) → embeds with Gemini → saves FAISS index to `vector_store/`.

---

### Component 4 — Agent Nodes
#### [NEW] `agent/router.py` — classifies question intent
#### [NEW] `agent/retriever.py` — FAISS similarity search (top-5)
#### [NEW] `agent/grader.py` — LLM grades each doc for relevance
#### [NEW] `agent/generator.py` — constrained answer generation
#### [NEW] `agent/evaluator.py` — faithfulness / hallucination check
#### [NEW] `agent/tools.py` — datetime & calculator tools
#### [NEW] `agent/memory.py` — appends answer to messages list

---

### Component 5 — Streamlit UI
#### [NEW] `app.py`
- Chat window with message history (from `st.session_state`)
- Sidebar: knowledge base topics, how-it-works diagram
- Source document display (collapsible)
- Tool output clearly labelled
- Retry/loading spinner

---

### Component 6 — Testing & Scripts
#### [NEW] `scripts/test_retrieval.py`
pytest tests verifying retrieval correctness for 12 known Q&A pairs (+ 3 additional quality checks).

---

### Component 7 — Documentation
#### [NEW] `docs/capstone_report.pdf`
4–5 page technical report generated with ReportLab, containing:
- Title, student info, abstract
- Problem statement
- Solution architecture & features
- Screenshots
- Tech stack
- Unique points (Corrective RAG loop, faithfulness guard)
- Future improvements

---

## Open Questions (Resolved)

> [!IMPORTANT]
> **Student details used in documentation:**
> 1. **Student Name** — Atri Dhar
> 2. **Roll Number** — 2329023
> 3. **Batch / Program** — B.Tech CSCE, 2023–2027

> [!IMPORTANT]
> **Google Gemini API Key** — `.env.example` is present and the app loads `.env` at startup.

> [!NOTE]
> I will use **FAISS** (not ChromaDB) for the vector store to avoid the sqlite3 version issue on Windows. The index is pre-built and committed to the repo.

---

## Verification Plan

### Automated Tests
```bash
# Build the vector index
python scripts/build_index.py

# Run retrieval quality tests
pytest scripts/test_retrieval.py -v

# Launch the Streamlit app
streamlit run app.py
```

### Manual Verification
- Ask 5 in-KB questions → verify grounded, cited answers
- Ask 3 out-of-KB questions → verify "I don't know" responses
- Use tool queries ("What time is it?", "Calculate 15% of 350") → verify tool routing
- Ask follow-up questions → verify memory/context retention
- Trigger faithfulness guard → verify retry loop activates
