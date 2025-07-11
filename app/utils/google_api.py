from app.models import GoogleAccount
from datetime import datetime, timezone
from .google_auth import refresh_access_token
import requests

def fetch_google_event_data(event_id, calendar_id, access_token, user_id):
    account = GoogleAccount.query.filter_by(user_id=user_id).first()
    if not account:
        return None

    if account.token_expiry is None or account.token_expiry.replace(tzinfo=timezone.utc) <= datetime.now(timezone.utc):
        success, msg = refresh_access_token(account)
        if not success:
            return None
        access_token = account.access_token

    url = f"https://www.googleapis.com/calendar/v3/calendars/{calendar_id}/events/{event_id}"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        return None

    data = response.json()
    return {
        "summary": data.get("summary"),
        "start": parse_google_datetime(data["start"]),
        "end": parse_google_datetime(data["end"]),
        "location": data.get("location"),
        "description": data.get("description")
    }

def parse_google_datetime(obj):
    dt = obj.get("dateTime") or obj.get("date")
    return datetime.fromisoformat(dt)