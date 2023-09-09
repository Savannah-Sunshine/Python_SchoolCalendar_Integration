from util import convert_to_datetime, file_exists, save_overwrite_to_file, Event
from datetime import datetime, timedelta

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ['https://www.googleapis.com/auth/calendar']
TOKEN_FILE = 'files/token.json'
CREDENTIAL_FILE = 'files/credentials.json'


def get_credentials():
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if file_exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CREDENTIAL_FILE, SCOPES)
            creds = flow.run_local_server(port=0)

        # Save the credentials for the next run
        with open(TOKEN_FILE, 'w') as token:
            token.write(creds.to_json())
    return creds




def get_calendars(creds):
    my_calendar_list = []
    try:
        service = build('calendar', 'v3', credentials=creds)
        # Call the Calendar API
        page_token = None
        while True:
            calendar_list = service.calendarList().list(pageToken=page_token).execute()
            for calendar_list_entry in calendar_list['items']:
                my_calendar_list.append({'calendar_name': calendar_list_entry['summary'], 'calendar_id': calendar_list_entry['id'], 'offical_class_name': None})
            page_token = calendar_list.get('nextPageToken')
            if not page_token:
                break

    except HttpError as error:
        print('An error occurred: %s' % error)
    return my_calendar_list

def insert_new_event(creds, event: Event):
    # Call API

    start_datetime = convert_to_datetime(event.event_due_date)
    event_request = {
        'summary': event.event_name,
        'start': {
            'dateTime': start_datetime.strftime('%Y-%m-%dT%H:%M:%S-06:00'),
            'timeZone': 'America/Denver',
        },
        'end': {
            'dateTime': (start_datetime + timedelta(minutes=30)).strftime('%Y-%m-%dT%H:%M:%S-06:00'),
            'timeZone': 'America/Denver',
        },
    }

    # print(event_request)
    
    service = build('calendar', 'v3', credentials=creds)
    # TODO go to event.event_calendar_id, right now is Primary
    new_event = service.events().insert(calendarId=event.event_calendar_id, body=event_request).execute()

    # print('Event created: \n%s\n\n' % (new_event.get('htmlLink')))

    event.event_id = new_event['id']
    return event

def delete_event(event_id, event_calendar_id, creds):
    service = build('calendar', 'v3', credentials=creds)
    service.events().delete(calendarId=event_calendar_id, eventId=event_id).execute()