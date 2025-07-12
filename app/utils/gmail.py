from app.models import GoogleAccount
from datetime import datetime, timezone
from dotenv import load_dotenv
from email.mime.text import MIMEText
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from .google_auth import refresh_access_token
import base64
import os

load_dotenv()
CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")


def reminder_email_via_gmail(user_id, to_email, subject, body):
    account = GoogleAccount.query.filter_by(user_id=user_id).first()
    if not account:
        return 400, "Google account not found"

    if account.token_expiry is None or account.token_expiry.replace(tzinfo=timezone.utc) <= datetime.now(timezone.utc):
        success, message = refresh_access_token(account)
        if not success:
            return 401, message

    creds = Credentials(
        token=account.access_token,
        refresh_token=account.refresh_token,
        token_uri="https://oauth2.googleapis.com/token",
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET
    )

    try:
        service = build("gmail", "v1", credentials=creds)
        message = create_message(account.email, to_email, subject, body)
        send_result = service.users().messages().send(userId="me", body=message).execute()
        return 200, f"Message sent, ID: {send_result['id']}"
    except Exception as e:
        return 500, f"Failed to send email: {str(e)}"


def create_message(from_email, to_email, subject, body):
    message = MIMEText(body)
    message["from"] = from_email
    message["to"] = to_email
    message["subject"] = subject
    
    raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
    return {"raw": raw}