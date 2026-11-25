"""
All the database work lives here .

Keeping the database code in its own file.
streamlit_app.py just imports these functions and uses them.
"""

import sqlite3
from pathlib import Path
from typing import Iterable, Mapping

# Keep the database in the project root, regardless of the process working directory.
DB_FILE = Path(__file__).resolve().parents[2] / "Improvement.db"


def init_db():
    """Create the improvement table the first time we run."""
    with sqlite3.connect(DB_FILE) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS improvement (
                id INTEGER PRIMARY KEY,
                input TEXT NOT NULL,
                output TEXT NOT NULL
            )
        """)


def save_results(results: Mapping[str, object]) -> int:
    """Write all improvements into the database."""
    if isinstance(results, Mapping):
        results = (results,)

    rows = [
        (r["input"], r["output"])
        for r in results
        if r.get("output") != "error"
    ]
    if not rows:
        return 0

    with sqlite3.connect(DB_FILE) as conn:
        conn.executemany(
            "INSERT INTO improvement (input, output) VALUES (?, ?)",
            rows,
        )
    return len(rows)


def load_history():
    """Read every improvement we have saved so far."""
    with sqlite3.connect(DB_FILE) as conn:
        return conn.execute(
            "SELECT input, output FROM improvement ORDER BY id DESC"
        ).fetchall()
