"""
test_retrieval.py — pytest suite for validating retrieval quality.

Run with:
    pytest scripts/test_retrieval.py -v

Tests that each sample question retrieves at least one relevant document
containing the expected keywords from the knowledge base.
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

import pytest

# Allow imports from project root
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from dotenv import load_dotenv

load_dotenv()


@pytest.fixture(scope="module")
def retriever():
    """Load the FAISS retriever once for all tests in this module."""
    from agent.retriever import get_retriever
    return get_retriever(k=5)


# ── Test cases: (question, [expected_keywords_in_retrieved_docs]) ─────────────
TEST_CASES = [
    (
        "What is the minimum attendance required to appear in the end semester exam?",
        ["75%", "attendance", "debarred"],
    ),
    (
        "How many total credits are needed to graduate in B.Tech CSCE?",
        ["160", "credits"],
    ),
    (
        "What topics are covered in Unit 1 of Data Structures?",
        ["linked list", "stack", "queue"],
    ),
    (
        "Explain AVL tree rotations.",
        ["avl", "rotation", "balance"],
    ),
    (
        "What are the ACID properties of a transaction?",
        ["atomicity", "consistency", "isolation", "durability"],
    ),
    (
        "What are the layers of the OSI model?",
        ["application", "transport", "network", "data link", "physical"],
    ),
    (
        "What happens if I submit an assignment late?",
        ["late", "penalty", "deduction"],
    ),
    (
        "What is the grading scale at KIIT? What grade corresponds to 80-89 marks?",
        ["grade", "excellent", "80"],
    ),
    (
        "Give me revision tips for Operating Systems.",
        ["operating system", "scheduling", "memory"],
    ),
    (
        "What documents do I need for the end semester exam?",
        ["hall ticket", "id card"],
    ),
    (
        "What is the passing criteria for each subject?",
        ["40", "45", "pass"],
    ),
    (
        "Explain CPU scheduling algorithms like Round Robin and SJF.",
        ["round robin", "sjf", "scheduling"],
    ),
]


@pytest.mark.parametrize("question,expected_keywords", TEST_CASES)
def test_retrieval_returns_relevant_docs(retriever, question, expected_keywords):
    """Each question must retrieve at least one doc containing expected keywords."""
    docs = retriever.invoke(question)

    assert len(docs) > 0, (
        f"No documents retrieved for question: '{question}'"
    )

    combined_content = " ".join(doc.page_content for doc in docs).lower()

    missing = [kw for kw in expected_keywords if kw.lower() not in combined_content]
    assert not missing, (
        f"Missing keywords {missing} in retrieved docs for question: '{question}'\n"
        f"Retrieved {len(docs)} docs. First doc excerpt:\n{docs[0].page_content[:300]}"
    )


def test_retrieval_returns_multiple_docs(retriever):
    """Ensure retrieval always returns more than 1 document."""
    docs = retriever.invoke("Tell me about KIIT CSCE program")
    assert len(docs) >= 3, f"Expected at least 3 docs, got {len(docs)}"


def test_retrieved_docs_have_metadata(retriever):
    """Each retrieved document must have 'source' metadata."""
    docs = retriever.invoke("What are the exam rules?")
    for doc in docs:
        assert "source" in doc.metadata, (
            f"Document missing 'source' metadata: {doc.page_content[:100]}"
        )
        assert doc.metadata["source"].endswith(".txt"), (
            f"Unexpected source filename: {doc.metadata['source']}"
        )


def test_retrieval_does_not_cross_contaminate(retriever):
    """A very specific query should return docs from the correct source file."""
    docs = retriever.invoke("What is Belady's Anomaly?")
    sources = [doc.metadata.get("source", "") for doc in docs]
    # Belady's Anomaly is in Operating Systems notes
    assert any("unit2" in s or "unit1" in s or "faqs" in s for s in sources), (
        f"Expected OS-related document but got sources: {sources}"
    )
