"""
build_index.py — One-time script to build the FAISS vector index from the knowledge base.

Usage:
    python scripts/build_index.py

Reads all *.txt files from knowledge_base/, chunks them with overlap,
embeds with Google Gemini embeddings, and saves the FAISS index to vector_store/.
"""
from __future__ import annotations

import os
import re
import sys
import time
from pathlib import Path

# Allow imports from project root
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from dotenv import load_dotenv

load_dotenv()

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings

BASE_DIR = Path(__file__).resolve().parent.parent
KB_PATH = BASE_DIR / "knowledge_base"
VS_PATH = BASE_DIR / "vector_store"


def _extract_retry_seconds(error_text: str, default_wait: float = 45.0) -> float:
    """Parse Gemini retry hint from 429 error text, fallback to default seconds."""
    match = re.search(r"retry in\s+([0-9]+(?:\.[0-9]+)?)s", error_text, re.IGNORECASE)
    if match:
        return max(float(match.group(1)) + 2.0, 5.0)
    return default_wait


def _embed_batch_with_retry(vectorstore, batch, embeddings, max_retries: int = 6):
    """Create or extend FAISS index with retry-on-quota behavior."""
    for attempt in range(max_retries):
        try:
            if vectorstore is None:
                return FAISS.from_documents(batch, embeddings)
            vectorstore.add_documents(batch)
            return vectorstore
        except Exception as exc:
            message = str(exc)
            is_quota_error = "RESOURCE_EXHAUSTED" in message or "429" in message
            if not is_quota_error or attempt == max_retries - 1:
                raise

            wait_s = _extract_retry_seconds(message)
            print(
                f"   ⚠️ Quota hit while embedding; waiting {wait_s:.1f}s before retry "
                f"({attempt + 1}/{max_retries}) ..."
            )
            time.sleep(wait_s)

    return vectorstore


def build_index() -> None:
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise EnvironmentError(
            "GOOGLE_API_KEY is not set. Create a .env file with GOOGLE_API_KEY=<your-key>."
        )

    # ── 1. Load all .txt documents ────────────────────────────────────────────
    print(f"\n📂 Loading documents from: {KB_PATH}")
    txt_files = sorted(KB_PATH.glob("*.txt"))
    if not txt_files:
        raise FileNotFoundError(f"No .txt files found in {KB_PATH}")

    all_docs = []
    for f in txt_files:
        loader = TextLoader(str(f), encoding="utf-8")
        docs = loader.load()
        for doc in docs:
            doc.metadata["source"] = f.name
            doc.metadata["topic"] = (
                f.stem.split("_", 1)[-1].replace("_", " ").title()
                if "_" in f.stem
                else f.stem.title()
            )
        all_docs.extend(docs)
        print(f"  ✅ Loaded: {f.name}")

    print(f"\n📄 Total documents loaded: {len(all_docs)}")

    # ── 2. Split into chunks ──────────────────────────────────────────────────
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=100,
        separators=["\n\n", "\n", ". ", " ", ""],
    )
    chunks = splitter.split_documents(all_docs)
    print(f"✂️  Total chunks created: {len(chunks)}")

    # ── 3. Embed with Google embeddings ──────────────────────────────────────
    print("\n🔗 Embedding chunks with Google gemini-embedding-001 ...")
    embeddings = GoogleGenerativeAIEmbeddings(
        model="gemini-embedding-001",
        google_api_key=api_key,
    )

    # Build in batches to avoid rate-limit bursts
    BATCH = 30
    vectorstore = None
    for i in range(0, len(chunks), BATCH):
        batch = chunks[i : i + BATCH]
        print(f"   Embedding batch {i // BATCH + 1}/{(len(chunks) - 1) // BATCH + 1} ...")
        vectorstore = _embed_batch_with_retry(vectorstore, batch, embeddings)
        time.sleep(1)  # Be polite to the API

    # ── 4. Save FAISS index ───────────────────────────────────────────────────
    VS_PATH.mkdir(parents=True, exist_ok=True)
    vectorstore.save_local(str(VS_PATH))
    print(f"\n💾 FAISS index saved to: {VS_PATH}")
    print("✨ Index build complete!")


if __name__ == "__main__":
    build_index()
