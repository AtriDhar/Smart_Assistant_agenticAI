###############################################################################
# Smart Student Assistant — Dockerfile
# Build:  docker build -t smart-student-assistant .
# Run:    docker run -p 8501:8501 --env-file .env smart-student-assistant
###############################################################################
FROM python:3.11-slim AS base

# Prevent Python from writing .pyc and enable unbuffered stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# ── Install system dependencies ──────────────────────────────────────────────
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl && \
    rm -rf /var/lib/apt/lists/*

# ── Install Python dependencies ──────────────────────────────────────────────
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ── Copy application code ────────────────────────────────────────────────────
COPY . .

# ── Create non-root user ─────────────────────────────────────────────────────
RUN useradd --create-home appuser && chown -R appuser:appuser /app
USER appuser

# ── Expose Streamlit port ────────────────────────────────────────────────────
EXPOSE 8501

# ── Health check ─────────────────────────────────────────────────────────────
HEALTHCHECK --interval=30s --timeout=10s --start-period=15s --retries=3 \
    CMD python healthcheck.py

# ── Start the app ────────────────────────────────────────────────────────────
# Respect platform-assigned PORT when available (Railway/Fly.io/Render Docker).
CMD ["sh", "-c", "streamlit run app.py --server.address=0.0.0.0 --server.port=${PORT:-8501} --server.enableCORS=false --server.enableXsrfProtection=false"]
