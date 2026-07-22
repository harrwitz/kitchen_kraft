import sys
import os

# Add backend directory to sys.path for Vercel Serverless Function runtime
backend_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend"))
if backend_path not in sys.path:
    sys.path.insert(0, backend_path)

try:
    from main import app, ensure_state_loaded
    ensure_state_loaded()
except Exception as e:
    print(f"Initialization error in Vercel serverless environment: {e}")
    from main import app
