import datetime
import os
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID", "")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET", "")
GOOGLE_API_SCOPES = ["https://www.googleapis.com/auth/calendar.events"]


def add_event_to_calendar(refresh_token: str, summary: str, description: str, start_time: datetime.datetime, end_time: datetime.datetime) -> Optional[str]:
    creds = Credentials(
        None,
        refresh_token=refresh_token,
        token_uri="https://oauth2.googleapis.com/token",
        client_id=GOOGLE_CLIENT_ID,
        client_secret=GOOGLE_CLIENT_SECRET,
        scopes=GOOGLE_API_SCOPES,
    )
    service = build("calendar", "v3", credentials=creds)
    event = {
        "summary": summary,
        "description": description,
        "start": {"dateTime": start_time.isoformat(), "timeZone": "UTC"},
        "end": {"dateTime": end_time.isoformat(), "timeZone": "UTC"},
    }
    created_event = service.events().insert(calendarId="primary", body=event).execute()
    return created_event.get("id") 