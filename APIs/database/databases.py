import sqlite3
from datetime import date
import uuid
from pathlib import Path

DB_PATH = Path(__file__).resolve().parents[1] / "skillLink.db"


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def _now():
    return date.today().isoformat()


def init_db():
    conn = get_connection()
    conn.executescript("""
    CREATE TABLE IF NOT EXISTS users (
        id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        surname TEXT NOT NULL,
        phone TEXT DEFAULT '',
        email TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL,
        location TEXT DEFAULT '',
        role TEXT NOT NULL DEFAULT 'user',
        created_at TEXT NOT NULL,
        avg_rating REAL NOT NULL DEFAULT 0,
        completed_jobs_count INTEGER NOT NULL DEFAULT 0
    );

    CREATE TABLE IF NOT EXISTS skills (
        id TEXT PRIMARY KEY,
        provider_id TEXT NOT NULL,
        skill_name TEXT NOT NULL,
        category TEXT DEFAULT '',
        price_min REAL NOT NULL,
        price_max REAL NOT NULL,
        description TEXT DEFAULT '',
        active INTEGER NOT NULL DEFAULT 1,
        created_at TEXT NOT NULL,
        CHECK (price_min <= price_max),
        FOREIGN KEY (provider_id) REFERENCES users(id) ON DELETE CASCADE
    );

    CREATE TABLE IF NOT EXISTS requests (
        id TEXT PRIMARY KEY,
        skill_id TEXT NOT NULL,
        skill_name_snapshot TEXT NOT NULL,
        provider_id TEXT NOT NULL,
        requester_id TEXT NOT NULL,
        budget REAL,
        status TEXT NOT NULL DEFAULT 'open',
        created_at TEXT NOT NULL,
        accepted_at TEXT,
        completed_at TEXT,
        CHECK (status IN ('open','accepted','completed')),
        FOREIGN KEY (skill_id) REFERENCES skills(id),
        FOREIGN KEY (provider_id) REFERENCES users(id),
        FOREIGN KEY (requester_id) REFERENCES users(id)
    );

    CREATE TABLE IF NOT EXISTS ratings (
        id TEXT PRIMARY KEY,
        request_id TEXT NOT NULL UNIQUE,
        provider_id TEXT NOT NULL,
        requester_id TEXT NOT NULL,
        stars INTEGER NOT NULL,
        comment TEXT DEFAULT '',
        created_at TEXT NOT NULL,
        CHECK (stars BETWEEN 1 AND 5),
        FOREIGN KEY (request_id) REFERENCES requests(id),
        FOREIGN KEY (provider_id) REFERENCES users(id),
        FOREIGN KEY (requester_id) REFERENCES users(id)
    );
    """)
    conn.commit()
    conn.close()


def create_user(name, surname, email, password, phone='', location='', role='user'):
    if role not in ('user', 'provider'):
        raise ValueError('Invalid account type')
    user_id = str(uuid.uuid4())
    conn = get_connection()
    try:
        with conn:
            conn.execute("""
                INSERT INTO users
                (id,name,surname,email,password,phone,location,role,created_at)
                VALUES (?,?,?,?,?,?,?,?,?)
            """, (user_id,name,surname,email,password,phone,location,role,_now()))
    except sqlite3.IntegrityError:
        raise ValueError('Email already exists')
    finally:
        conn.close()
    return user_id


def log_in(email, password, role=None):
    conn = get_connection()
    query = """
        SELECT id,name,surname,email,phone,location,role,avg_rating,completed_jobs_count
        FROM users WHERE email=? AND password=?
    """
    params = [email, password]
    if role:
        query += " AND role=?"
        params.append(role)
    row = conn.execute(query, params).fetchone()
    conn.close()
    return dict(row) if row else None


def get_user(user_id):
    conn = get_connection()
    row = conn.execute("SELECT * FROM users WHERE id=?", (user_id,)).fetchone()
    conn.close()
    return dict(row) if row else None


def create_skill(provider_id, skill_name, category, price_min, price_max, description):
    if not skill_name:
        raise ValueError('Skill name is required')
    try:
        price_min, price_max = float(price_min), float(price_max)
    except (TypeError, ValueError):
        raise ValueError('Prices must be numbers')
    if price_min > price_max:
        raise ValueError('Minimum price cannot be greater than maximum price')
    conn = get_connection()
    provider = conn.execute("SELECT id,role FROM users WHERE id=?", (provider_id,)).fetchone()
    if not provider or provider['role'] != 'provider':
        conn.close()
        raise ValueError('Provider account not found')
    skill_id = str(uuid.uuid4())
    with conn:
        conn.execute("""
            INSERT INTO skills
            (id,provider_id,skill_name,category,price_min,price_max,description,created_at)
            VALUES (?,?,?,?,?,?,?,?)
        """, (skill_id,provider_id,skill_name,category or '',price_min,price_max,description or '',_now()))
    conn.close()
    return skill_id


def get_skill(skill_id):
    conn = get_connection()
    row = conn.execute("SELECT * FROM skills WHERE id=?", (skill_id,)).fetchone()
    conn.close()
    return dict(row) if row else None


def browse_skills(category=None, provider_id=None):
    conn = get_connection()
    query = """
        SELECT skills.*, users.name, users.surname, users.location,
               users.phone, users.avg_rating
        FROM skills JOIN users ON users.id=skills.provider_id
        WHERE skills.active=1
    """
    params = []
    if category:
        query += " AND skills.category=?"
        params.append(category)
    if provider_id:
        query += " AND skills.provider_id=?"
        params.append(provider_id)
    query += " ORDER BY skills.created_at DESC"
    rows = conn.execute(query, params).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def deactivate_skill(skill_id):
    conn = get_connection()
    with conn:
        conn.execute("UPDATE skills SET active=0 WHERE id=?", (skill_id,))
    conn.close()


def create_request(skill_id, requester_id, budget):
    skill = get_skill(skill_id)
    requester = get_user(requester_id)
    if not skill or not skill['active']:
        raise ValueError('Skill not found')
    if not requester:
        raise ValueError('Requester not found')
    if skill['provider_id'] == requester_id:
        raise ValueError('You cannot request your own service')
    try:
        budget = float(budget) if budget not in (None, '') else None
    except (TypeError, ValueError):
        raise ValueError('Budget must be a number')
    request_id = str(uuid.uuid4())
    conn = get_connection()
    with conn:
        conn.execute("""
            INSERT INTO requests
            (id,skill_id,skill_name_snapshot,provider_id,requester_id,budget,created_at)
            VALUES (?,?,?,?,?,?,?)
        """, (request_id,skill_id,skill['skill_name'],skill['provider_id'],requester_id,budget,_now()))
    conn.close()
    return request_id


def get_request(request_id):
    conn = get_connection()
    row = conn.execute("""
        SELECT r.*, p.name provider_name, p.surname provider_surname,
               u.name requester_name, u.surname requester_surname
        FROM requests r
        JOIN users p ON p.id=r.provider_id
        JOIN users u ON u.id=r.requester_id
        WHERE r.id=?
    """, (request_id,)).fetchone()
    conn.close()
    return dict(row) if row else None


def get_requests_for_provider(provider_id):
    conn = get_connection()
    rows = conn.execute("""
        SELECT r.*, u.name requester_name, u.surname requester_surname
        FROM requests r JOIN users u ON u.id=r.requester_id
        WHERE r.provider_id=? ORDER BY r.created_at DESC
    """, (provider_id,)).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_requests_for_requester(requester_id):
    conn = get_connection()
    rows = conn.execute("""
        SELECT r.*, u.name provider_name, u.surname provider_surname
        FROM requests r JOIN users u ON u.id=r.provider_id
        WHERE r.requester_id=? ORDER BY r.created_at DESC
    """, (requester_id,)).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def accept_request(request_id):
    conn = get_connection()
    row = conn.execute("SELECT status FROM requests WHERE id=?", (request_id,)).fetchone()
    if not row:
        conn.close(); raise ValueError('Request not found')
    if row['status'] != 'open':
        conn.close(); raise ValueError('Only open requests can be accepted')
    with conn:
        conn.execute("UPDATE requests SET status='accepted',accepted_at=? WHERE id=?", (_now(),request_id))
    conn.close()


def complete_request(request_id):
    conn = get_connection()
    row = conn.execute("SELECT status FROM requests WHERE id=?", (request_id,)).fetchone()
    if not row:
        conn.close(); raise ValueError('Request not found')
    if row['status'] != 'accepted':
        conn.close(); raise ValueError('Request must be accepted first')
    with conn:
        conn.execute("UPDATE requests SET status='completed',completed_at=? WHERE id=?", (_now(),request_id))
    conn.close()


def add_rating(request_id, stars, comment=''):
    try:
        stars = int(stars)
    except (TypeError, ValueError):
        raise ValueError('Rating must be between 1 and 5')
    if not 1 <= stars <= 5:
        raise ValueError('Rating must be between 1 and 5')
    conn = get_connection()
    request = conn.execute("SELECT * FROM requests WHERE id=?", (request_id,)).fetchone()
    if not request:
        conn.close(); raise ValueError('Request not found')
    if request['status'] != 'completed':
        conn.close(); raise ValueError('Request must be completed before rating')
    if conn.execute("SELECT id FROM ratings WHERE request_id=?", (request_id,)).fetchone():
        conn.close(); raise ValueError('This request has already been rated')
    provider = conn.execute("SELECT avg_rating,completed_jobs_count FROM users WHERE id=?", (request['provider_id'],)).fetchone()
    count = provider['completed_jobs_count']
    new_count = count + 1
    new_average = ((provider['avg_rating'] * count) + stars) / new_count
    rating_id = str(uuid.uuid4())
    with conn:
        conn.execute("""
            INSERT INTO ratings
            (id,request_id,provider_id,requester_id,stars,comment,created_at)
            VALUES (?,?,?,?,?,?,?)
        """, (rating_id,request_id,request['provider_id'],request['requester_id'],stars,comment or '',_now()))
        conn.execute("UPDATE users SET avg_rating=?,completed_jobs_count=? WHERE id=?", (round(new_average,2),new_count,request['provider_id']))
    conn.close()
    return rating_id


def get_ratings_for_provider(provider_id):
    conn = get_connection()
    rows = conn.execute("""
        SELECT r.*, u.name requester_name, u.surname requester_surname
        FROM ratings r JOIN users u ON u.id=r.requester_id
        WHERE r.provider_id=? ORDER BY r.created_at DESC
    """, (provider_id,)).fetchall()
    conn.close()
    return [dict(r) for r in rows]