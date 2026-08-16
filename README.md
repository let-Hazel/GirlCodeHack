# SkillLink — Integrated Frontend + Backend Prototype

This version connects the existing SkillLink frontend to a Flask REST API and SQLite database.

## Features connected

- Registration for service users and service providers
- Login with account type
- SQLite persistence
- Provider service/skill creation
- Live provider listing from the database
- Provider search through the API
- Service requests
- Provider accept/complete workflow
- Provider ratings API
- WhatsApp contact button
- AI-style natural language matching against live provider data
- CORS configured for local frontend development

## Project structure

```text
GirlCodeHack/
├── APIs/
│   ├── app.py
│   ├── main.py
│   └── database/
│       ├── __init__.py
│       └── databases.py
├── AI/
│   └── model.py
├── frontend/
│   ├── index.html
│   ├── login.html
│   ├── signup.html
│   ├── service-user.html
│   ├── service-provider.html
│   ├── css/
│   └── js/
│       ├── api.js
│       ├── auth.js
│       ├── user-dashboard.js
│       ├── provider-dashboard.js
│       └── ai-search.js
├── requirements.txt
└── run.py
```

## Run locally

From the `GirlCodeHack` directory:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python run.py
```

The API runs at:

```text
http://127.0.0.1:5000
```

Check it with:

```text
http://127.0.0.1:5000/health
```

In a second terminal, from the same project directory:

```bash
python3 -m http.server 5500 --directory frontend
```

Then open:

```text
http://127.0.0.1:5500/signup.html
```

## Demo flow

1. Register a Service Provider account.
2. Log in as the provider.
3. Click **+ Add Service** and add a skill.
4. Log out.
5. Register a Service User account.
6. Log in as the service user.
7. The provider should appear from the SQLite database.
8. Use the AI search box or provider search.
9. Click **Request Service**.
10. Log back in as the provider.
11. Accept the request.
12. Complete the request.

## Important prototype note

Passwords are currently stored as plain text because this is a local prototype. Before production deployment, replace this with password hashing and proper session/token authentication.