import sqlite3
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent.parent
DB_PATH = PROJECT_DIR / "poliklinika.db"

def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def initialize_database() -> None:
    with get_connection() as conn:
        conn.executescript((PROJECT_DIR / "schema.sql").read_text(encoding="utf-8"))
        conn.executescript((PROJECT_DIR / "seed.sql").read_text(encoding="utf-8"))
