from app.extensions import db
from datetime import datetime, timezone, timedelta
from dotenv import load_dotenv
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from urllib.parse import urlencode

import requests, os

load_dotenv()

CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
REDIRECT_URI = os.getenv("GOOGLE_REDIRECT_URI")

def get_google_auth_url():
    params = {
        "client_id": CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "response_type": "code",
        "scope": "openid email profile https://www.googleapis.com/auth/calendar.readonly https://www.googleapis.com/auth/gmail.send",
        "access_type": "offline",
        "prompt": "consent",
    }
    return f"https://accounts.google.com/o/oauth2/v2/auth?{urlencode(params)}"

def exchange_code_for_tokens(code):
    url = "https://oauth2.googleapis.com/token"
    data = {
        "code": code,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "redirect_uri": REDIRECT_URI,
        "grant_type": "authorization_code",
    }
    response = requests.post(url, data=data)
    return response.json()

def refresh_access_token(account):
    creds = Credentials(
        token=None,
        refresh_token=account.refresh_token,
        token_uri="https://oauth2.googleapis.com/token",
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET
    )

    try:
        creds.refresh(Request())
        account.access_token = creds.token
        account.token_expiry = datetime.now(timezone.utc) + timedelta(seconds=creds.expiry.timestamp() - datetime.now(timezone.utc).timestamp())
        db.session.commit()
        return True, "Token refreshed"
    except Exception as e:
        return False, f"Failed to refresh token: {str(e)}"