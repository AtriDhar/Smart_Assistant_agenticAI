# Deployment Guide - Smart Student Assistant

This guide gives you a reliable path to deploy the app from this repository.

## 1) Pre-deploy checklist

- Obtain a Google API key from Google AI Studio.
- `.env` exists locally with:

```env
GOOGLE_API_KEY=your_actual_google_key
GEMINI_CHAT_MODEL=gemini-2.5-flash
```

- Dependencies installed:

```bash
pip install -r requirements.txt
```

- Retrieval tests pass:

```bash
python -m pytest scripts/test_retrieval.py -v
```

## 2) Local deployment (recommended first)

Run the app locally in the project root:

```bash
streamlit run app.py
```

Open the URL shown in terminal (usually `http://localhost:8501`).

### Local deployment with Docker

You can also run the app using Docker Compose:

```bash
docker compose up --build
```

## 3) Deploy on Streamlit Community Cloud

1. Push this project to GitHub.
2. Go to Streamlit Community Cloud and create a new app.
3. Set:
   - Repository: your GitHub repo
   - Branch: `main` (or your deployment branch)
   - Main file path: `app.py`
4. In app settings, add secrets:

```toml
GOOGLE_API_KEY="your_actual_google_key"
GEMINI_CHAT_MODEL="gemini-2.5-flash"
```

5. Deploy.

### Notes

- Keep `vector_store/` in the repo to avoid rebuilding the index.
- If `vector_store/` is not committed, the first launch may take longer because the app will build index automatically.
- The sidebar allows users to enter their Google API key if environment variables are not set.

## 4) Deploy on Render / Railway (Docker / Procfile)

This repo includes both a `Dockerfile` and a `Procfile`.

### Option A: Docker (Recommended for Railway/Fly.io)
Platforms like Railway or Fly.io can directly build from the provided Dockerfile.
1. Create a new service from your GitHub repo.
2. The platform will automatically detect the `Dockerfile`.
3. Set environment variables (`GOOGLE_API_KEY`, `GEMINI_CHAT_MODEL`).
4. Expose port `8501`.
5. Deploy.

### Option B: Procfile (Recommended for Render)
Render setup via Native Environment:
1. Create a new Web Service from your GitHub repo.
2. Environment:
   - Runtime: Python
   - Build Command: `pip install -r requirements.txt`
   - Start Command: auto-detected from `Procfile`
3. Add environment variables:
   - `GOOGLE_API_KEY=your_actual_key`
   - `GEMINI_CHAT_MODEL=gemini-2.5-flash`
4. Deploy.

## 5) Post-deploy verification

After deployment, verify these flows in the live app:

- In-knowledge-base question returns grounded answer with source labels.
- Out-of-scope question returns graceful refusal.
- Date/time query routes to tool response.
- Calculator query routes to tool response.
- Follow-up question uses memory context.

Suggested smoke tests:

1. "What is minimum attendance required?"
2. "What day is today?"
3. "Calculate 15% of 350"
4. "Who won last night's match?"
5. "Can you summarize Unit 2?"

## 6) Common deployment issues

### Error: API key required
Users can either set `GOOGLE_API_KEY` globally in platform secrets or enter it via the sidebar.

### Error: FAISS index missing
Either:
- commit `vector_store/index.faiss` and `vector_store/index.pkl`, or
- allow first-run auto-build (requires valid Google API key + enough quota).

### Error: model not found
Ensure the configured chat model is available to your API key. By default, the app uses `gemini-2.5-flash`.

## 7) Production hardening recommendations

- Use the provided `healthcheck.py` to monitor service uptime.
- Add rate limiting for public deployments.
- Add optional auth if exposing externally (e.g., Streamlit auth).
