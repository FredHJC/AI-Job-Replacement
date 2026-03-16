import sqlite3
import json
import secrets
import string
import time
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "data" / "submissions.db"

# Short ID: 8 chars, URL-safe
_ALPHABET = string.ascii_lowercase + string.digits
def _generate_id(length=8):
    return "".join(secrets.choice(_ALPHABET) for _ in range(length))


def _get_conn() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    return conn


def init_db():
    conn = _get_conn()
    conn.execute("CREATE TABLE IF NOT EXISTS meta (key TEXT PRIMARY KEY, value TEXT)")
    row = conn.execute("SELECT value FROM meta WHERE key = 'schema_version'").fetchone()
    current = row["value"] if row else "0"

    if current != "2":
        conn.execute("DROP TABLE IF EXISTS submissions")
        conn.execute("""
            CREATE TABLE submissions (
                id          TEXT PRIMARY KEY,
                job_id      TEXT NOT NULL,
                answers     TEXT NOT NULL,
                result      TEXT NOT NULL,
                created_at  REAL NOT NULL
            )
        """)
        conn.execute("INSERT OR REPLACE INTO meta (key, value) VALUES ('schema_version', '2')")
        conn.commit()
    conn.close()


def save_submission(job_id: str, answers: dict, result: dict) -> str:
    """Save a submission and return its short ID."""
    conn = _get_conn()
    for _ in range(5):
        sid = _generate_id()
        try:
            conn.execute(
                "INSERT INTO submissions (id, job_id, answers, result, created_at) VALUES (?, ?, ?, ?, ?)",
                (sid, job_id, json.dumps(answers, ensure_ascii=False), json.dumps(result, ensure_ascii=False), time.time()),
            )
            conn.commit()
            conn.close()
            return sid
        except sqlite3.IntegrityError:
            continue
    conn.close()
    raise RuntimeError("Failed to generate unique ID")


def get_submission(sid: str) -> dict | None:
    """Load a submission by ID. Returns None if not found."""
    conn = _get_conn()
    row = conn.execute("SELECT * FROM submissions WHERE id = ?", (sid,)).fetchone()
    conn.close()
    if not row:
        return None
    return {
        "id": row["id"],
        "job_id": row["job_id"],
        "answers": json.loads(row["answers"]),
        "result": json.loads(row["result"]),
        "created_at": row["created_at"],
    }
