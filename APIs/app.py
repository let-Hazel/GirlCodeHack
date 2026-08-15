from flask import Flask, jsonify, request
import sqlite3

app = Flask(__name__)

DB_PATH = "skillPay.db"


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


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
                users.email,
                users.bio,
                users.location,
                users.avg_rating,
                users.completed_jobs_count,
                skills.id AS skill_id,
                skills.skill_name,
                skills.category,
                skills.price_min,
                skills.price_max,
                skills.description AS skill_description
            FROM users
            JOIN skills ON users.id = skills.provider_id
            WHERE skills.active = 1
            AND skills.skill_name LIKE ?
        """, (f"%{skill}%",)).fetchall()
    else:
        rows = conn.execute("""
            SELECT
                users.id,
                users.name,
                users.surname,
                users.email,
                users.bio,
                users.location,
                users.avg_rating,
                users.completed_jobs_count,
                skills.id AS skill_id,
                skills.skill_name,
                skills.category,
                skills.price_min,
                skills.price_max,
                skills.description AS skill_description
            FROM users
            JOIN skills ON users.id = skills.provider_id
            WHERE skills.active = 1
        """).fetchall()

    conn.close()

    return jsonify([dict(row) for row in rows])


if __name__ == "__main__":
    app.run(debug=True)