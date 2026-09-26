import sqlite3
import json
from datetime import datetime

DB_PATH = "chat_history.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS sessions (
            id TEXT PRIMARY KEY,
            title TEXT,
            created_at TEXT,
            messages TEXT
        )
    """)
    conn.commit()
    conn.close()

def save_session(session_id, title, messages):
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        "INSERT OR REPLACE INTO sessions (id, title, created_at, messages) VALUES (?, ?, ?, ?)",
        (session_id, title, datetime.now().isoformat(), json.dumps(messages))
    )
    conn.commit()
    conn.close()

def load_all_sessions():
    conn = sqlite3.connect(DB_PATH)
    rows = conn.execute("SELECT id, title, created_at FROM sessions ORDER BY created_at DESC").fetchall()
    conn.close()
    return rows

def load_session(session_id):
    conn = sqlite3.connect(DB_PATH)
    row = conn.execute("SELECT messages FROM sessions WHERE id = ?", (session_id,)).fetchone()
    conn.close()
    return json.loads(row[0]) if row else []

def delete_session(session_id):
    conn = sqlite3.connect(DB_PATH)
    conn.execute("DELETE FROM sessions WHERE id = ?", (session_id,))
    conn.commit()
    conn.close()