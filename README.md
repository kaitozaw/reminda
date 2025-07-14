# Reminda, no more no-shows.

## Target User & Problem

Locally owned cleaning businesses often struggle with frequent no-shows and resulting opportunity costs due to non-standardized schedule management that heavily relies on the business owner.

## Solution

Reminda provides an automated workflow that sends reminders to customers with scheduled cleaning appointments in Google Calendar.

## Features

- 🔔 Automatic email reminders (same-day or day-before)
- 💌 Gmail API for email delivery
- 📅 Google Calendar Add-on with customer assignment
- 🔐 Google OAuth 2.0 integration for accessing Gmail and Calendar APIs
- 🧑‍💻 Web dashboard for viewing reminder delivery logs and managing reminder settings
- 🛠️ Deployable to Render with GitHub Actions automation

## Data Model

![Data Model](./docs/data_model.png)

## Tech Stack

### Frontend (Google Calendar Add-on UI)
- Apps Script
- CardService

### Frontend (Web UI)
- Jinja2
- Bootstrap 5
- Vanilla JS

### Backend
- Flask
- SQLAlchemy
- WTForm

### Database
- PostgreSQL

### Authentication
- Flask-Login

### Google Integration
- OAuth 2.0
- Google Calendar API
- Gmail API

### Scheduled Tasks
- GitHub Actions

### DevOps / Hosting
- GitHub
- Render

## Getting Started

Follow these steps to set up Reminda locally for development.

### 1. Clone the repository

```bash
git clone https://github.com/kaitoozawa/reminda.git
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
FLASK_APP=run.py
FLASK_ENV=development
SECRET_KEY=your-secret-key

# PostgreSQL settings
DATABASE_URL=postgresql://your-username:your-password@localhost/reminda

# Google OAuth Settings
GOOGLE_CLIENT_ID=your-google-client-id.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=your-google-client-secret
GOOGLE_REDIRECT_URI=http://127.0.0.1:5000/auth/google_callback
```

### 4. Create PostgreSQL database and initialize schema

```bash
# Create PostgreSQL database
createdb reminda

# Set Flask app if needed
export FLASK_APP=run.py

# Apply migrations to create tables
flask db upgrade
```

### 5. Run the server

```bash
flask run
```

## Google Calendar Add-on Integration

Follow these steps to set up the Google Calendar sidebar add-on using Google Apps Script.

### 1. Create a Google Cloud Project

- Go to [Google Cloud Console](https://console.cloud.google.com)
- Create a new project (e.g., `reminda-dev`)

### 2. Enable Gmail and Calendar APIs

- Navigate to **API & Services > Library**
- Enable the following APIs:
  - Gmail API
  - Google Calendar API

### 3. Configure OAuth Consent Screen

- Go to **APIs & Services > OAuth consent screen**
- Fill in the required fields:
  - App name (e.g., `reminda-dev`)
  - User support email
- Choose `External` as the user type
- Set developer contact email
- Under **Test users**, add your own Google account to test during development

### 4. Create OAuth 2.0 Credentials

- Go to **APIs & Services > Credentials**
- Click **Create Credentials > OAuth client ID**
- Fill in the required fields:
  - Application type: `Web application`
  - Name (e.g., `reminda-dev`)
  - Authorized redirect URI: `http://127.0.0.1:5000/auth/google_callback`
- Copy `client_id` and `client_secret` into your `.env` file as:
  ```bash
  GOOGLE_CLIENT_ID=your-client-id.apps.googleusercontent.com
  GOOGLE_CLIENT_SECRET=your-client-secret
  ```

### 5. Create an Apps Script Project

- Visit [Google Apps Script](https://script.google.com/)
- Click **New Project**
- Name the project (e.g., `reminda-dev`)
- Go to **Project Settings**
- Enable: **Show "appsscript.json" manifest file in editor**
- Under **Google Cloud Platform (GCP) Project**, paste the **project number** from the Google Cloud project created in Step 1

### 6. Add application.json and Code.gs
- You can copy and paste the contents from the `gas/` directory in the cloned GitHub repository:
  - `gas/appsscript.json` → paste into `appsscript.json`
  - `gas/Code.gs` → paste into `Code.gs`

### 7. Test the Add-on Using Cloudflare Tunnel

You can expose your local Flask app to the internet temporarily using [Cloudflare Tunnel](https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/), which is useful for testing the Add-on sidebar with a live backend.

```bash
# Install Cloudflare Tunnel CLI
brew install cloudflared

# Start your Flask server locally
# Make sure your .env and database are configured correctly
flask run --host=127.0.0.1 --port=5000

# In a new terminal, start the Cloudflare Tunnel
cloudflared tunnel --url http://localhost:5000

# After running, you'll see a public URL like:
# https://your-tunnel-name.trycloudflare.com
# Keep this terminal open while testing
```

### 8. Insert the Tunnel URL in `Code.gs` and Deploy the Add-on

- Open the Apps Script editor for your Add-on project
- In `Code.gs`, update the first line with your Cloudflare Tunnel URL
- Go to **Deploy > Test deployments**
- Click **Install**

## Directory Structure

```bash
reminda/
├── .github/               # GitHub Actions workflows
├── app/
│   ├── forms/             # WTForms classes
│   ├── jobs/              # Scheduled/background tasks
│   ├── models/            # SQLAlchemy models
│   ├── routes/            # Flask routes
│   ├── static/            # CSS, JS
│   ├── templates/         # HTML templates
│   ├── utils/             # Helper functions
│   ├── __init__.py        # App factory
│   └── extensions.py      # Flask extensions
├── docs/                  # Data model diagram
├── gas/                   # Contains Google Apps Script code and UI components for the Calendar Add-on
├── migrations/            # DB migration history
├── scripts/               # Runs the scheduled reminder dispatch process
├── .env                   # Environment variables (not committed)
├── .gitignore
├── config.py              # App configuration
├── LICENSE
├── README.md
├── requirements.txt
└── run.py                 # App entry point
```