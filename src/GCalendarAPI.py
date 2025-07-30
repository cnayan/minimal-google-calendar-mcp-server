import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]

class GCalendarAPI:
  """Google Calendar API client to fetch upcoming events."""

  def __init__(self):
    self.creds = None
    self.service = None
    self.flow = None

  def get(self, num: int) -> list[dict[str, object]]:
    """Google Calendar API method to fetch upcoming events."""

    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token.json"):
        self.creds = Credentials.from_authorized_user_file("token.json", SCOPES)

    # If there are no (valid) credentials available, let the user log in.
    if not self.creds or not self.creds.valid:
        if self.creds and self.creds.expired and self.creds.refresh_token:
            self.creds.refresh(Request())
        else:
            self.flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )

            self.creds = self.flow.run_local_server(port=0)

            # Save the credentials for the next run
            with open("token.json", "w") as token:
                token.write(self.creds.to_json())

    if self.service is None:
        try:
            self.service = build("calendar", "v3", credentials=self.creds)
        except HttpError as error:
            print(f"An error occurred while connecting to Google Calendar API: {error}")
            return []

    try:
        # Call the Calendar API
        now = datetime.datetime.now(tz=datetime.timezone.utc).isoformat()
        print(f"Getting the upcoming {num} events")
        events_result = (
            self.service.events().list(
                calendarId="primary",
                timeMin=now,
                maxResults=num,
                singleEvents=True,
                orderBy="startTime",
            )
            .execute()
        )

        events = events_result.get("items", [])

        if not events:
            print("No upcoming events found.")
            return []

        return [
            {
                "name": event["summary"],
                "start": event["start"].get("dateTime", event["start"].get("date")),
            }
            for event in events[:num]
        ]

    except HttpError as error:
        print(f"An error occurred: {error}")
        return []
