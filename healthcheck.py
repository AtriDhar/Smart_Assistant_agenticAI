"""
Health check endpoint for Docker / Render / Railway.

Usage:
    python healthcheck.py          # exits 0 if app is reachable, 1 if not
    curl http://localhost:8501/_stcore/health   # Streamlit built-in health
"""
import sys
import os
import urllib.request


def check() -> bool:
    ports = []
    env_port = os.getenv("PORT", "").strip()
    if env_port:
        ports.append(env_port)
    if "8501" not in ports:
        ports.append("8501")

    for port in ports:
        try:
            url = f"http://localhost:{port}/_stcore/health"
            req = urllib.request.Request(url, method="GET")
            with urllib.request.urlopen(req, timeout=5) as resp:
                if resp.status == 200:
                    return True
        except Exception:
            continue
    return False


if __name__ == "__main__":
    if check():
        print("✅ Healthy")
        sys.exit(0)
    else:
        print("❌ Unhealthy")
        sys.exit(1)
