from flask import Flask, jsonify, request
from flask_cors import CORS

from APIs.database.databases import *

app = Flask(__name__)

# Allow the frontend to communicate with Flask
CORS(app)

# Initialise database
init_db()


# =========================================================
# DATABASE CONNECTION
# =========================================================

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


# =========================================================
# HEALTH CHECK
# =========================================================

@app.get("/health")
def health():

    return jsonify({
        "status": "ok",
        "message": "SkillLink API is running"
    }), 200


# =========================================================
# CREATE USER
# =========================================================

@app.post("/users")
def create_user_route():

    data = request.get_json() or {}

    name = data.get("name")
    surname = data.get("surname")
    email = data.get("email")
    password = data.get("password")

    phone = data.get("phone", "")
    location = data.get("location", "")
    role = data.get("role", "user")


    if not name or not surname or not email or not password:

        return jsonify({
            "error":
            "Name, surname, email and password are required"
        }), 400


    if role not in ["user", "provider"]:

        return jsonify({
            "error": "Invalid role"
        }), 400


    try:

        user_id = create_user(
            name,
            surname,
            email,
            password,
            phone,
            location,
            role
        )

    except ValueError as e:

        return jsonify({
            "error": str(e)
        }), 409


    return jsonify({

        "message":
        "User created successfully",

        "user_id":
        user_id

    }), 201


# =========================================================
# LOGIN
# =========================================================

@app.post("/login")
def login():

    data = request.get_json() or {}

    email = data.get("email")
    password = data.get("password")
    role = data.get("role")


    if not email or not password:

        return jsonify({
            "error":
            "Email and password are required"
        }), 400


    user = log_in(
        email,
        password,
        role
    )


    if not user:

        return jsonify({
            "error":
            "Invalid email, password, or account type"
        }), 401


    return jsonify(user), 200


# =========================================================
# GET USER
# =========================================================

@app.get("/users/<user_id>")
def get_user_route(user_id):

    user = get_user(user_id)


    if not user:

        return jsonify({
            "error":
            "User not found"
        }), 404


    return jsonify(user), 200


# =========================================================
# PROVIDERS
# =========================================================

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
                users.phone,
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

            WHERE users.role = 'provider'

            AND skills.active = 1

            AND skills.skill_name LIKE ?

        """, (f"%{skill}%",)).fetchall()


    else:

        rows = conn.execute("""
            SELECT
                users.id,
                users.name,
                users.surname,
                users.phone,
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

            WHERE users.role = 'provider'

            AND skills.active = 1

        """).fetchall()


    conn.close()


    return jsonify([
        dict(row)
        for row in rows
    ])


# =========================================================
# CREATE SKILL
# =========================================================

@app.post("/skills")
def create_skill_route():

    data = request.get_json() or {}


    try:

        skill_id = create_skill(

            provider_id =
            data.get("provider_id"),

            skill_name =
            data.get("skill_name"),

            category =
            data.get("category"),

            price_min =
            data.get("price_min"),

            price_max =
            data.get("price_max"),

            description =
            data.get("description")

        )

    except ValueError as e:

        return jsonify({
            "error": str(e)
        }), 400


    return jsonify({

        "message":
        "Skill created",

        "skill_id":
        skill_id

    }), 201


# =========================================================
# GET SKILL
# =========================================================

@app.get("/skills/<skill_id>")
def get_skill_route(skill_id):

    skill = get_skill(skill_id)


    if not skill:

        return jsonify({
            "error":
            "Skill not found"
        }), 404


    return jsonify(skill), 200


# =========================================================
# BROWSE SKILLS
# =========================================================

@app.get("/skills")
def browse_skills_route():

    category = request.args.get("category")


    skills = browse_skills(category)


    return jsonify(skills), 200


# =========================================================
# DEACTIVATE SKILL
# =========================================================

@app.post("/skills/<skill_id>/deactivate")
def deactivate_skill_route(skill_id):

    deactivate_skill(skill_id)


    return jsonify({
        "message":
        "Skill deactivated"
    }), 200


# =========================================================
# CREATE SERVICE REQUEST
# =========================================================

@app.post("/requests")
def create_request_route():

    data = request.get_json() or {}


    try:

        request_id = create_request(

            skill_id =
            data.get("skill_id"),

            requester_id =
            data.get("requester_id"),

            budget =
            data.get("budget")

        )

    except ValueError as e:

        return jsonify({
            "error": str(e)
        }), 400


    return jsonify({

        "message":
        "Request created",

        "request_id":
        request_id

    }), 201


# =========================================================
# GET REQUEST
# =========================================================

@app.get("/requests/<request_id>")
def get_request_route(request_id):

    req = get_request(request_id)


    if not req:

        return jsonify({
            "error":
            "Request not found"
        }), 404


    return jsonify(req), 200


# =========================================================
# PROVIDER REQUESTS
# =========================================================

@app.get("/requests/provider/<provider_id>")
def requests_for_provider_route(
    provider_id
):

    return jsonify(
        get_requests_for_provider(
            provider_id
        )
    ), 200


# =========================================================
# REQUESTER REQUESTS
# =========================================================

@app.get("/requests/requester/<requester_id>")
def requests_for_requester_route(
    requester_id
):

    return jsonify(
        get_requests_for_requester(
            requester_id
        )
    ), 200


# =========================================================
# ACCEPT REQUEST
# =========================================================

@app.post("/requests/<request_id>/accept")
def accept_request_route(
    request_id
):

    try:

        accept_request(
            request_id
        )

    except ValueError as e:

        return jsonify({
            "error": str(e)
        }), 400


    return jsonify({
        "message":
        "Request accepted"
    }), 200


# =========================================================
# COMPLETE REQUEST
# =========================================================

@app.post("/requests/<request_id>/complete")
def complete_request_route(
    request_id
):

    try:

        complete_request(
            request_id
        )

    except ValueError as e:

        return jsonify({
            "error": str(e)
        }), 400


    return jsonify({
        "message":
        "Request completed"
    }), 200


# =========================================================
# RATINGS
# =========================================================

@app.post("/ratings")
def add_rating_route():

    data = request.get_json() or {}


    try:

        rating_id = add_rating(

            request_id =
            data.get("request_id"),

            stars =
            data.get("stars"),

            comment =
            data.get("comment", "")

        )

    except ValueError as e:

        return jsonify({
            "error": str(e)
        }), 400


    return jsonify({

        "message":
        "Rating added",

        "rating_id":
        rating_id

    }), 201


# =========================================================
# PROVIDER RATINGS
# =========================================================

@app.get("/ratings/provider/<provider_id>")
def ratings_for_provider_route(
    provider_id
):

    return jsonify(
        get_ratings_for_provider(
            provider_id
        )
    ), 200


# =========================================================
# START SERVER
# =========================================================

if __name__ == "__main__":

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )