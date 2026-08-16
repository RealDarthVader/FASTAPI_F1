# api/index.py
import sys
import os

# Add the Backend folder to Python's module search path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "Backend")))

from app.main import app  # type: ignore