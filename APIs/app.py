from flask import Flask, jsonify, request
import sqlite3
import main

app = Flask(__name__)

import os


DB_PATH = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "database",
    "skillLink.db"
)

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn
@app.post("/users")
def create_user():

    data = request.get_json()

    name = data.get("name")
    surname = data.get("surname")
    email = data.get("email")
    password = data.get("password")
    location = data.get("location", "")

    if not name or not surname or not email or not password:
        return jsonify({
            "error": "Name, surname, email and password are required"
        }), 400

    conn = get_connection()

    existing_user = conn.execute(
        "SELECT id FROM users WHERE email = ?",
        (email,)
    ).fetchone()

    if existing_user:
        conn.close()
        return jsonify({
            "error": "Email already exists"
        }), 409

    cursor = conn.execute("""
        INSERT INTO users
        (name, surname, email, password, location, created_at)
        VALUES (?, ?, ?, ?, ?, datetime('now'))
    """, (
        name,
        surname,
        email,
        password,
        location
    ))

    conn.commit()

    user_id = cursor.lastrowid

    conn.close()

    return jsonify({
        "message": "User created successfully",
        "user_id": user_id
    }), 201

@app.get("/providers")
def get_providers():

    skill = request.args.get("skill")

    conn = get_connection()

    if skill:
        rows = conn.execute("""
            SELECT
                users.id,
                users.name,
                users.surname,
                users.location,
                users.avg_rating,
                users.completed_jobs_count,
                skills.id AS skill_id,
                skills.skill_name,
                skills.category,
                skills.price_min,
                skills.price_max,
                skills.description
            FROM users
            JOIN skills
                ON users.id = skills.provider_id
            WHERE skills.active = 1
            AND skills.skill_name LIKE ?
        """, (f"%{skill}%",)).fetchall()

    else:
        rows = conn.execute("""
            SELECT
                users.id,
                users.name,
                users.surname,
                users.location,
                users.avg_rating,
                users.completed_jobs_count,
                skills.id AS skill_id,
                skills.skill_name,
                skills.category,
                skills.price_min,
                skills.price_max,
                skills.description
            FROM users
            JOIN skills
                ON users.id = skills.provider_id
            WHERE skills.active = 1
        """).fetchall()

    conn.close()

    return jsonify([dict(row) for row in rows])
@app.get("/")
def home():
    return jsonify({
        "message": "SkillPay API is running"
    })

if __name__ == "__main__":
    app.run(debug=True)