import datetime
import os.path
import requests
import calsnap_duckling
import calsnap_textextract

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/calendar"]
text = calsnap_textextract.text_extract('screenshot2.png')

def main():
  """
    Creates an event in Google Calendar.
    This function takes the specified title, start time, and end time,
    constructs an event object, and inserts it into the user's primary calendar.
  """
  creds = None

  if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
  
  if not creds or not creds.valid:
    
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())

    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          "credentials.json", SCOPES
      )
      creds = flow.run_local_server(port=0)

    with open("token.json", "w") as token:
      token.write(creds.to_json())

  try:
    service = build("calendar", "v3", credentials=creds)


    timezone = "Asia/Hong_Kong"
    start_time, end_time = calsnap_duckling.duckling(text)
    event_title = input("Please name the event: ")
    body = {"summary": event_title,
            "start": {
                "dateTime": start_time,
                "timeZone": timezone
            },
            "end": {
                "dateTime": end_time,
                "timeZone": timezone
            },
            "description": "Details about the event...",
            "location": "Event location..."
            }
    event = service.events().insert(calendarId='primary', body=body).execute()
    print('Event created: %s' % (event.get('htmlLink')))  
  
  except HttpError as error:
    print(f"An error occurred: {error}")


if __name__ == "__main__":
  main()