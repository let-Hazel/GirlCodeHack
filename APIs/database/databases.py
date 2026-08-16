import sqlite3
from datetime import date, datetime, timezone
import uuid

DB_PATH = "skillLink.db"

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    conn = get_connection()

    # USERS
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            surname TEXT NOT NULL,
            phone TEXT,
            email TEXT NOT NULL UNIQUE,
            password TEXT,
            location TEXT,
            created_at TEXT NOT NULL,
            avg_rating REAL NOT NULL DEFAULT 0,
            completed_jobs_count INTEGER NOT NULL DEFAULT 0
        )
    """)

    # SKILLS
    conn.execute("""
        CREATE TABLE IF NOT EXISTS skills (
            id TEXT PRIMARY KEY,
            provider_id INTEGER NOT NULL,
            skill_name TEXT NOT NULL,
            category TEXT,
            price_min REAL NOT NULL,
            price_max REAL NOT NULL,
            description TEXT,
            active INTEGER NOT NULL DEFAULT 1,
            created_at TEXT NOT NULL,

            CHECK (price_min <= price_max),

            FOREIGN KEY (provider_id)
                REFERENCES users(id)
        )
    """)

    # REQUESTS
    conn.execute("""
        CREATE TABLE IF NOT EXISTS requests (
            id TEXT PRIMARY KEY,
            skill_id TEXT NOT NULL,
            skill_name_snapshot TEXT NOT NULL,
            provider_id INTEGER NOT NULL,
            requester_id INTEGER NOT NULL,
            budget REAL,
            status TEXT NOT NULL DEFAULT 'open',
            created_at TEXT NOT NULL,
            accepted_at TEXT,
            completed_at TEXT,

            CHECK (
                status IN ('open', 'accepted', 'completed')
            ),

            FOREIGN KEY (skill_id)
                REFERENCES skills(id),

            FOREIGN KEY (provider_id)
                REFERENCES users(id),

            FOREIGN KEY (requester_id)
                REFERENCES users(id)
        )
    """)

    # RATINGS
    conn.execute("""
        CREATE TABLE IF NOT EXISTS ratings (
            id TEXT PRIMARY KEY,
            request_id TEXT NOT NULL UNIQUE,
            provider_id INTEGER NOT NULL,
            requester_id INTEGER NOT NULL,
            stars INTEGER NOT NULL,
            comment TEXT,
            created_at TEXT NOT NULL,

            CHECK (stars >= 1 AND stars <= 5),

            FOREIGN KEY (request_id)
                REFERENCES requests(id),

            FOREIGN KEY (provider_id)
                REFERENCES users(id),

            FOREIGN KEY (requester_id)
                REFERENCES users(id)
        )
    """)

    conn.commit()
    conn.close()

    print("Database tables created successfully!")


def _now():
    return date.today().isoformat()


def create_user(name, surname, email, password="", phone="", location=""):
    user_id = str(uuid.uuid4())
    conn = get_connection()
    now = _now()

    try:
        with conn:
            conn.execute("""
                INSERT INTO users
                (id, name, surname, email, password, phone, location, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                user_id, name, surname, email, password, phone, location, now
            ))
    except sqlite3.IntegrityError:
        raise ValueError("Email already exists")
    finally:
        conn.close()

    return user_id


def log_in(email, password):

    conn = get_connection()

    row = conn.execute("""
        SELECT id, name, surname, email
        FROM users
        WHERE email = ?
        AND password = ?
    """, (email, password)).fetchone()

    conn.close()

    return dict(row) if row else None


def get_user(user_id):

    conn = get_connection()

    row = conn.execute("""
        SELECT *
        FROM users
        WHERE id = ?
    """, (user_id,)).fetchone()

    conn.close()

    if row:
        return dict(row)

    return None


def create_skill(
    provider_id,
    skill_name,
    category,
    price_min,
    price_max,
    description
):

    if price_min > price_max:
        raise ValueError(
            "Minimum price cannot be greater than maximum price"
        )

    skill_id = str(uuid.uuid4())

    conn = get_connection()

    with conn:

        conn.execute("""
            INSERT INTO skills
            (
                id,
                provider_id,
                skill_name,
                category,
                price_min,
                price_max,
                description,
                active,
                created_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, 1, ?)
        """, (
            skill_id,
            provider_id,
            skill_name,
            category,
            price_min,
            price_max,
            description,
            _now()
        ))

    conn.close()

    return skill_id


def deactivate_skill(skill_id):

    conn = get_connection()

    with conn:
        conn.execute("""
            UPDATE skills
            SET active = 0
            WHERE id = ?
        """, (skill_id,))

    conn.close()


def get_skill(skill_id):
    conn = get_connection()

    row = conn.execute("""
        SELECT *
        FROM skills
        WHERE id = ?
    """, (skill_id,)).fetchone()

    conn.close()

    if row:
        return dict(row)

    return None


def browse_skills(category=None):
    conn = get_connection()

    if category:

        rows = conn.execute("""
            SELECT *
            FROM skills
            WHERE active = 1
            AND category = ?
        """, (category,)).fetchall()

    else:

        rows = conn.execute("""
            SELECT *
            FROM skills
            WHERE active = 1
        """).fetchall()

    conn.close()

    return [dict(row) for row in rows]


def create_request(skill_id, requester_id, budget):
    skill = get_skill(skill_id)

    if skill is None:
        raise ValueError("Skill not found")

    request_id = str(uuid.uuid4())

    conn = get_connection()

    with conn:

        conn.execute("""
            INSERT INTO requests
            (
                id,
                skill_id,
                skill_name_snapshot,
                provider_id,
                requester_id,
                budget,
                status,
                created_at
            )
            VALUES (?, ?, ?, ?, ?, ?, 'open', ?)
        """, (
            request_id,
            skill_id,
            skill["skill_name"],
            skill["provider_id"],
            requester_id,
            budget,
            _now()
        ))

    conn.close()

    return request_id


def get_request(request_id):
    conn = get_connection()

    row = conn.execute("""
        SELECT *
        FROM requests
        WHERE id = ?
    """, (request_id,)).fetchone()

    conn.close()

    if row:
        return dict(row)

    return None


def get_requests_for_provider(provider_id):
    conn = get_connection()

    rows = conn.execute("""
        SELECT *
        FROM requests
        WHERE provider_id = ?
    """, (provider_id,)).fetchall()

    conn.close()

    return [dict(row) for row in rows]


def get_requests_for_requester(requester_id):
    conn = get_connection()

    rows = conn.execute("""
        SELECT *
        FROM requests
        WHERE requester_id = ?
    """, (requester_id,)).fetchall()

    conn.close()

    return [dict(row) for row in rows]


def accept_request(request_id):
    conn = get_connection()

    request = conn.execute("""
        SELECT *
        FROM requests
        WHERE id = ?
    """, (request_id,)).fetchone()

    if request is None:
        conn.close()
        raise ValueError("Request not found")

    if request["status"] != "open":
        conn.close()
        raise ValueError(
            "Only open requests can be accepted"
        )

    with conn:

        conn.execute("""
            UPDATE requests
            SET status = 'accepted',
                accepted_at = ?
            WHERE id = ?
        """, (
            _now(),
            request_id
        ))

    conn.close()


def complete_request(request_id):
    conn = get_connection()

    request = conn.execute("""
        SELECT *
        FROM requests
        WHERE id = ?
    """, (request_id,)).fetchone()

    if request is None:
        conn.close()
        raise ValueError("Request not found")

    if request["status"] != "accepted":
        conn.close()
        raise ValueError(
            "Request must be accepted before it can be completed"
        )

    with conn:

        conn.execute("""
            UPDATE requests
            SET status = 'completed',
                completed_at = ?
            WHERE id = ?
        """, (
            _now(),
            request_id
        ))

    conn.close()


def add_rating(request_id, stars, comment=""):
    if stars < 1 or stars > 5:
        raise ValueError(
            "Rating must be between 1 and 5"
        )

    conn = get_connection()

    request = conn.execute("""
        SELECT *
        FROM requests
        WHERE id = ?
    """, (request_id,)).fetchone()

    if request is None:
        conn.close()
        raise ValueError("Request not found")

    if request["status"] != "completed":
        conn.close()
        raise ValueError(
            "Request must be completed before it can be rated"
        )

    existing_rating = conn.execute("""
        SELECT id
        FROM ratings
        WHERE request_id = ?
    """, (request_id,)).fetchone()

    if existing_rating:
        conn.close()
        raise ValueError(
            "This request has already been rated"
        )

    provider_id = request["provider_id"]
    requester_id = request["requester_id"]

    provider = conn.execute("""
        SELECT avg_rating, completed_jobs_count
        FROM users
        WHERE id = ?
    """, (provider_id,)).fetchone()

    if provider is None:
        conn.close()
        raise ValueError("Provider not found")

    old_rating = provider["avg_rating"]
    old_count = provider["completed_jobs_count"]

    new_count = old_count + 1

    new_average = (
        (old_rating * old_count) + stars
    ) / new_count

    rating_id = str(uuid.uuid4())

    with conn:

        conn.execute("""
            INSERT INTO ratings
            (
                id,
                request_id,
                provider_id,
                requester_id,
                stars,
                comment,
                created_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            rating_id,
            request_id,
            provider_id,
            requester_id,
            stars,
            comment,
            _now()
        ))

        conn.execute("""
            UPDATE users
            SET avg_rating = ?,
                completed_jobs_count = ?
            WHERE id = ?
        """, (
            round(new_average, 2),
            new_count,
            provider_id
        ))

    conn.close()

    return rating_id


def get_ratings_for_provider(provider_id):
    conn = get_connection()

    rows = conn.execute("""
        SELECT *
        FROM ratings
        WHERE provider_id = ?
    """, (provider_id,)).fetchall()

    conn.close()

    return [dict(row) for row in rows]



if __name__ == "__main__":
    init_db()