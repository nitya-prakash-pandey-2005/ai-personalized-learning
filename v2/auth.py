import bcrypt
from v2.database import get_connection
from datetime import datetime


# -----------------------------
# PASSWORD HELPERS
# -----------------------------

def hash_password(password: str) -> bytes:
    """Hash a password using bcrypt"""
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


def verify_password(password: str, hashed_password: bytes) -> bool:
    """Verify password against hash"""
    return bcrypt.checkpw(password.encode(), hashed_password)


# -----------------------------
# USER MANAGEMENT
# -----------------------------

def create_user(email: str, password: str) -> bool:
    """
    Create a new user with hashed password.
    Returns False if user already exists.
    """
    conn = get_connection()
    cur = conn.cursor()

    # Check if user exists
    cur.execute("SELECT id FROM users WHERE username = ?", (email,))
    if cur.fetchone():
        conn.close()
        return False

    hashed = hash_password(password)

    cur.execute("""
        INSERT INTO users (username, created_at)
        VALUES (?, ?)
    """, (email, datetime.now().isoformat()))

    user_id = cur.lastrowid

    cur.execute("""
        INSERT INTO auth (user_id, password_hash)
        VALUES (?, ?)
    """, (user_id, hashed))

    conn.commit()
    conn.close()
    return True


def authenticate_user(email: str, password: str) -> bool:
    """
    Authenticate user by checking hashed password.
    """
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT u.id, a.password_hash
        FROM users u
        JOIN auth a ON u.id = a.user_id
        WHERE u.username = ?
    """, (email,))

    row = cur.fetchone()
    conn.close()

    if not row:
        return None

    user_id, stored_hash = row
    if verify_password(password, stored_hash):
        return user_id
    return None