import sys
import os

# Add backend directory to sys.path for Vercel Serverless Function runtime
backend_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend"))
if backend_path not in sys.path:
    sys.path.insert(0, backend_path)

from main import app, ensure_state_loaded

# Warm up dataset state on cold start
try:
    ensure_state_loaded()
except Exception as e:
    print(f"Dataset load warning in Vercel serverless environment: {e}")
