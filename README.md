# Reminda, no more no-shows.

## Target User & Problem

Locally owned cleaning businesses often struggle with frequent no-shows and resulting opportunity costs due to non-standardized schedule management that heavily relies on the business owner.

## Solution

Reminda provides an automated workflow that sends reminders to customers with scheduled cleaning appointments in Google Calendar.

## Features

- 🔔 Automatic email reminders (same-day or day-before)
- 📅 Google Calendar Add-on with customer assignment
- 🧑‍💻 Web dashboard for managing reminders and settings
- 🔐 Google OAuth-based secure login
- 💌 Gmail API for email delivery
- 🛠️ Compatible with Render and GitHub Actions

## Tech Stack

### Frontend (Google Calendar Add-on UI)
- Apps Script
- CardService

### Frontend (Web UI)
- Jinja2**
- Bootstrap 5
- Vanilla JS

### Backend
- Flask
- SQLAlchemy
- Celery
- Redis

### Database
- PostgreSQL

### Authentication
- Flask-Login

### Google Integration
- OAuth 2.0 (Google)
- Google Calendar API
- Gmail API

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/<your-username>/reminda.git
cd reminda
```

### 2. Install dependencies

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Create `.env` file

```bash
# Flask App Settings
SECRET_KEY=your-secret-key

# PostgreSQL Database Settings
POSTGRES_USER=your-username
POSTGRES_PASSWORD=your-password
POSTGRES_HOST=localhost
POSTGRES_DB=reminda

# Google OAuth Settings (use your own credentials)
GOOGLE_CLIENT_ID=your-google-client-id.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=your-google-client-secret
GOOGLE_REDIRECT_URI=http://127.0.0.1:5000/auth/google_callback
```

### 4. Create MySQL database and initialize schema

```bash
# Create PostgreSQL database
createdb reminda

# Set Flask app if needed
export FLASK_APP=run.py

# Initialize migrations folder (only once)
flask db init

# Generate migration scripts from models
flask db migrate -m "Initial migration"

# Apply migrations to create tables
flask db upgrade
```

### 5. Run the server

```bash
flask run
```

### 6. Start background scheduler

```bash
celery -A celeryconfig.celery worker --loglevel=info
```

## Directory Structure

```bash
reminda/
├── .vscode/               # VS Code settings (optional)
├── app/
│   ├── forms/             # WTForms classes
│   ├── jobs/              # Scheduled/background tasks
│   ├── models/            # SQLAlchemy models
│   ├── routes/            # Flask routes (blueprints)
│   ├── scripts/           # Utility scripts
│   ├── static/            # CSS, JS, image assets
│   ├── templates/         # HTML templates (Jinja2)
│   ├── utils/             # Helper functions
│   ├── __init__.py        # App factory
│   └── extensions.py      # Flask extensions (DB, LoginManager, etc.)
├── migrations/            # DB migration history (Flask-Migrate)
├── .env                   # Environment variables (not committed)
├── .flaskenv              # Flask CLI settings
├── .gitignore
├── celery_workers.py      # Celery worker launcher
├── celeryconfig.py        # Celery config
├── config.py              # App configuration
├── LICENSE
├── README.md
├── requirements.txt
└── run.py                 # App entry point
```