import os
import sys

# Ensure project root '/app' is on sys.path when running inside the container
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

