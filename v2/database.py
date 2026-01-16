import sqlite3
from datetime import datetime

DB_NAME = "learning_v2.db"


def get_connection():
    """
    Returns a SQLite connection.
    check_same_thread=False is required for Streamlit.
    """
    return sqlite3.connect(DB_NAME, check_same_thread=False)


def init_db():
    """
    Creates required tables if they don't exist.
    Safe to call multiple times.
    """
    conn = get_connection()
    cur = conn.cursor()

    # -------------------------
    # USERS TABLE
    # -------------------------
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        created_at TEXT
    )
    """)

    # -------------------------
    # AUTH TABLE
    # -------------------------
    cur.execute("""
    CREATE TABLE IF NOT EXISTS auth (
        user_id INTEGER PRIMARY KEY,
        password_hash BLOB,
        FOREIGN KEY(user_id) REFERENCES users(id)
    )
    """)


    # -------------------------
    # PROGRESS TABLE
    # -------------------------
    cur.execute("""
    CREATE TABLE IF NOT EXISTS progress (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        topic TEXT,
        accuracy REAL,
        response_time REAL,
        timestamp TEXT,
        FOREIGN KEY(user_id) REFERENCES users(id)
    )
    """)

    # -------------------------
    # PREFERENCES TABLE
    # -------------------------
    cur.execute("""
    CREATE TABLE IF NOT EXISTS preferences (
        user_id INTEGER PRIMARY KEY,
        learning_style TEXT,
        difficulty TEXT,
        FOREIGN KEY(user_id) REFERENCES users(id)
    )
    """)

    conn.commit()
    conn.close()


# Utility function (optional, helpful later)
def now():
    return datetime.now().isoformat()

