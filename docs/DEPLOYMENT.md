# Deployment Guide - Smart Student Assistant

This guide gives you a reliable path to deploy the app from this repository.

## 1) Pre-deploy checklist

- Google Gemini API key is available.
- `.env` exists locally with:

```env
GOOGLE_API_KEY=your_actual_api_key
```

- Dependencies installed:

```bash
pip install -r requirements.txt
```

- FAISS index can be generated:

```bash
python scripts/build_index.py
```

- Retrieval tests pass:

```bash
pytest scripts/test_retrieval.py -v
```

## 2) Local deployment (recommended first)

Run the app locally in the project root:

```bash
streamlit run app.py
```

Open the URL shown in terminal (usually `http://localhost:8501`).

## 3) Deploy on Streamlit Community Cloud

1. Push this project to GitHub.
2. Go to Streamlit Community Cloud and create a new app.
3. Set:
   - Repository: your GitHub repo
   - Branch: `main` (or your deployment branch)
   - Main file path: `app.py`
4. In app settings, add secret:

```toml
GOOGLE_API_KEY="your_actual_api_key"
```

5. Deploy.

### Notes

- Keep `vector_store/` in the repo if you want faster cold start.
- If `vector_store/` is not committed, first launch may take longer because the app will build index automatically.
- `runtime.txt` pins Python for better compatibility.

## 4) Deploy on Render (Procfile-based)

This repo includes a `Procfile`:

```text
web: streamlit run app.py --server.address 0.0.0.0 --server.port $PORT
```

Render setup:

1. Create a new Web Service from your GitHub repo.
2. Environment:
   - Runtime: Python
   - Build Command: `pip install -r requirements.txt`
   - Start Command: auto-detected from `Procfile` or set same command manually
3. Add environment variable:
   - `GOOGLE_API_KEY=your_actual_api_key`
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

### Error: `GOOGLE_API_KEY` not set

Set it in platform secrets/environment settings and redeploy.

### Error: FAISS index missing

Either:
- commit `vector_store/index.faiss` and `vector_store/index.pkl`, or
- allow first-run auto-build (requires valid API key + enough quota).

### Error: embedding API quota exceeded (429)

The index builder already includes retry logic. If quota remains exhausted, wait and retry.

### Error: model not found

Current code uses `gemini-embedding-001`, which is compatible with the installed SDK setup.

## 7) Production hardening recommendations

- Add request logging and observability (LangSmith or app logs).
- Add rate limiting for public deployments.
- Add optional auth if exposing externally.
- Add health check endpoint or startup check script.
