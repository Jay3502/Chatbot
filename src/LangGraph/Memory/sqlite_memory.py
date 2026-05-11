import os
import sqlite3

from langgraph.checkpoint.sqlite import SqliteSaver

_DB_PATH = os.path.normpath(os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "..", "..", "..",
    "chatbot_memory.db"
))

_conn = None

def get_db_path():
    return _DB_PATH

def get_memory():
    global _conn
    if _conn is None:
        _conn = sqlite3.connect(_DB_PATH, check_same_thread=False)

        # Create chat_sessions table if it doesn't exist
        _conn.execute("""
            CREATE TABLE IF NOT EXISTS chat_sessions (
                chat_name  TEXT NOT NULL,
                usecase    TEXT NOT NULL,
                thread_id  TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY (chat_name, usecase)
            )
        """)

        # Migrate old schema: add usecase column if missing
        cols = [r[1] for r in _conn.execute("PRAGMA table_info(chat_sessions)").fetchall()]
        if "usecase" not in cols:
            _conn.execute(
                "ALTER TABLE chat_sessions ADD COLUMN usecase TEXT NOT NULL DEFAULT 'Basic Chatbot'"
            )

        _conn.commit()
    return SqliteSaver(_conn)


def load_chats(usecase):
    """Return {chat_name: thread_id} for the given usecase, ordered by creation time."""
    get_memory()
    rows = _conn.execute(
        "SELECT chat_name, thread_id FROM chat_sessions WHERE usecase = ? ORDER BY created_at",
        (usecase,)
    ).fetchall()
    return {name: tid for name, tid in rows} if rows else {}


def save_chat(chat_name, thread_id, usecase):
    """Persist a new chat. Ignores duplicate inserts so created_at is never overwritten."""
    get_memory()
    _conn.execute(
        "INSERT OR IGNORE INTO chat_sessions (chat_name, usecase, thread_id) VALUES (?, ?, ?)",
        (chat_name, usecase, thread_id)
    )
    _conn.commit()