import sqlite3
from datetime import datetime, timezone
import uuid

DB_PATH = "skillLink.db"


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    return conn


def init_db():
    conn = get_connection()
    conn.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id  TEXT,
        name TEXT NOT NULL,
        surname TEXT NOT NULL,
        email TEXT NOT NULL,
        password TEXT,
        location TEXT,
        created_at TEXT NOT NULL,
        avg_rating REAL NOT NULL DEFAULT 0,
        completed_jobs_count INTEGER NOT NULL DEFAULT 0
    );
    """)
    conn.commit()

    conn.execute("""
    CREATE TABLE IF NOT EXISTS skills (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        provider_id TEXT NOT NULL,
        skill_name TEXT NOT NULL,
        category TEXT,
        price_min REAL,
        price_max REAL,
        description TEXT,
        active INTEGER NOT NULL DEFAULT 1,
        created_at TEXT NOT NULL,
        FOREIGN KEY (provider_id) REFERENCES users(id)
    );
    """)
    conn.commit()

    conn.execute("""
    CREATE TABLE IF NOT EXISTS requests (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        skill_id TEXT NOT NULL,
        skill_name_snapshot TEXT NOT NULL,
        provider_id TEXT NOT NULL,
        requester_id TEXT NOT NULL,
        budget REAL,
        status TEXT NOT NULL DEFAULT 'open',
        created_at TEXT NOT NULL,
        accepted_at TEXT,
        completed_at TEXT,
        FOREIGN KEY (skill_id) REFERENCES skills(id),
        FOREIGN KEY (provider_id) REFERENCES users(id),
        FOREIGN KEY (requester_id) REFERENCES users(id)
    );
    """)
    conn.commit()

    conn.execute("""
    CREATE TABLE IF NOT EXISTS ratings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        request_id TEXT NOT NULL UNIQUE,
        provider_id TEXT NOT NULL,
        requester_id TEXT NOT NULL,
        stars INTEGER NOT NULL,
        comment TEXT,
        created_at TEXT NOT NULL,
        FOREIGN KEY (request_id) REFERENCES requests(id),
        FOREIGN KEY (provider_id) REFERENCES users(id),
        FOREIGN KEY (requester_id) REFERENCES users(id)
    );
    """)
    conn.commit()
    conn.close()


def _now():
    return datetime.now(timezone.utc).isoformat()


def create_user(id, name, surname, email, password, location=""):
    conn = get_connection()
    with conn:
        conn.execute(
            "INSERT INTO users (id, name, surname, email, password, location, created_at) "
            "VALUES (?, ?, ?, ?, ?)",
            (id, name, surname, email, password, location, _now()),
        )
        user_id = conn.execute(
                    "SELECT id FROM users WHERE id = ? "
                    "VALUES (?)",
                    (id),
                )
    conn.close()
    return user_id

def log_in(email, password):
    conn = get_connection()
    conn.execute("SELECT * FROM users WHERE email = ? AND password = ?"
                        "VALUES (?, ?)",
                        (email, password))

def get_user(user_id):
    conn = get_connection()
    row = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
    conn.close()
    return dict(row) if row else None


def create_skill(provider_id, skill_name, category, price_min, price_max, description):
    skill_id = str(uuid.uuid4())
    conn = get_connection()
    with conn:
        conn.execute(
            "INSERT INTO skills (id, provider_id, skill_name, category, price_min, "
            "price_max, description, active, created_at) VALUES (?, ?, ?, ?, ?, ?, ?, 1, ?)",
            (skill_id, provider_id, skill_name, category, price_min, price_max, description, _now()),
        )
    conn.close()
    return skill_id


def deactivate_skill(skill_id):
    conn = get_connection()
    with conn:
        conn.execute("UPDATE skills SET active = 0 WHERE id = ?", (skill_id,))
    conn.close()


def get_skill(skill_id):
    conn = get_connection()
    row = conn.execute("SELECT * FROM skills WHERE id = ?", (skill_id,)).fetchone()
    conn.close()
    return dict(row) if row else None


def browse_skills(category=None):
    conn = get_connection()
    if category:
        rows = conn.execute(
            "SELECT * FROM skills WHERE active = 1 AND category = ?", (category,)
        ).fetchall()
    else:
        rows = conn.execute("SELECT * FROM skills WHERE active = 1").fetchall()
    conn.close()
    return [dict(row) for row in rows]


def create_request(skill_id, requester_id, budget):
    skill = get_skill(skill_id)
    if skill is None:
        raise ValueError("skill not found")
    request_id = str(uuid.uuid4())
    conn = get_connection()
    with conn:
        conn.execute(
            "INSERT INTO requests (id, skill_id, skill_name_snapshot, provider_id, "
            "requester_id, budget, status, created_at, accepted_at, completed_at) "
            "VALUES (?, ?, ?, ?, ?, ?, 'open', ?, NULL, NULL)",
            (request_id, skill_id, skill["skill_name"], skill["provider_id"], requester_id, budget, _now()),
        )
    conn.close()
    return request_id


def get_request(request_id):
    conn = get_connection()
    row = conn.execute("SELECT * FROM requests WHERE id = ?", (request_id,)).fetchone()
    conn.close()
    return dict(row) if row else None


def get_requests_for_provider(provider_id, status=None):
    conn = get_connection()
    if status:
        rows = conn.execute(
            "SELECT * FROM requests WHERE provider_id = ? AND status = ?",
            (provider_id, status),
        ).fetchall()
    else:
        rows = conn.execute(
            "SELECT * FROM requests WHERE provider_id = ?", (provider_id,)
        ).fetchall()
    conn.close()
    return [dict(row) for row in rows]


def get_requests_for_requester(requester_id, status=None):
    conn = get_connection()
    if status:
        rows = conn.execute(
            "SELECT * FROM requests WHERE requester_id = ? AND status = ?",
            (requester_id, status),
        ).fetchall()
    else:
        rows = conn.execute(
            "SELECT * FROM requests WHERE requester_id = ?", (requester_id,)
        ).fetchall()
    conn.close()
    return [dict(row) for row in rows]


def accept_request(request_id):
    conn = get_connection()
    with conn:
        conn.execute(
            "UPDATE requests SET status = 'accepted', accepted_at = ? WHERE id = ?",
            (_now(), request_id),
        )
    conn.close()


def cancel_request(request_id):
    conn = get_connection()
    with conn:
        conn.execute("UPDATE requests SET status = 'cancelled' WHERE id = ?", (request_id,))
    conn.close()


def complete_request_and_rate(request_id, stars, comment=""):
    conn = get_connection()
    try:
        with conn:
            request_row = conn.execute(
                "SELECT * FROM requests WHERE id = ?", (request_id,)
            ).fetchone()
            if request_row is None:
                raise ValueError("request not found")
            if request_row["status"] != "accepted":
                raise ValueError("request must be accepted before it can be completed")

            provider_row = conn.execute(
                "SELECT * FROM users WHERE id = ?", (request_row["provider_id"],)
            ).fetchone()
            if provider_row is None:
                raise ValueError("provider not found")

            old_count = provider_row["completed_jobs_count"]
            old_avg = provider_row["avg_rating"]
            new_count = old_count + 1
            new_avg = ((old_avg * old_count) + stars) / new_count
            now = _now()
            rating_id = str(uuid.uuid4())

            conn.execute(
                "UPDATE requests SET status = 'completed', completed_at = ? WHERE id = ?",
                (now, request_id),
            )
            conn.execute(
                "INSERT INTO ratings (id, request_id, provider_id, requester_id, stars, "
                "comment, created_at) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (rating_id, request_id, request_row["provider_id"], request_row["requester_id"],
                 stars, comment, now),
            )
            conn.execute(
                "UPDATE users SET completed_jobs_count = ?, avg_rating = ?, "
                "total_earned = total_earned + ? WHERE id = ?",
                (new_count, new_avg, request_row["budget"] or 0, request_row["provider_id"]),
            )
    finally:
        conn.close()
    return rating_id


def get_ratings_for_provider(provider_id):
    conn = get_connection()
    rows = conn.execute(
        "SELECT * FROM ratings WHERE provider_id = ?", (provider_id,)
    ).fetchall()
    conn.close()
    return [dict(row) for row in rows]