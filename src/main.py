import sys
from pathlib import Path

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.database import initialize_database
from src.ui.cli import run

if __name__ == "__main__":
    initialize_database()
    run()
