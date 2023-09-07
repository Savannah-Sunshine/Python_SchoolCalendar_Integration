from __future__ import print_function

import datetime
import re
import json
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar']

def get_credentials():
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
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
                my_calendar_list.append([{'calendar_name': calendar_list_entry['summary']}, {'calendar_id': calendar_list_entry['id']}])
            page_token = calendar_list.get('nextPageToken')
            if not page_token:
                break

    except HttpError as error:
        print('An error occurred: %s' % error)
    return my_calendar_list

def save_calendars(calendar_list):
    # Save the calendars in JSON for the next run
    with open('calendars.json', 'w') as calendars:
        calendars.write(json.dumps(calendar_list))

def update_needed_calendars():
    return not os.path.exists('calendars.json')
    # todo check if calendars are correct?
    # todo check if calendars are old?

def read_ls_txt_file():
    lines = None
    if os.path.exists('LS_sept6.txt'): #todo hardcoded name
        with open('LS_sept6.txt', 'r') as LS_HW:
            lines = [word for line in LS_HW for word in re.split(r'[\n\t]+', line) if word]
    else:
        print("No LS file found")
    return lines

def update_events():
    #todo
    print()
    # if(event not found)
    #     create_new_event():

def create_new_event():
    #todo
    # Call API
    save_event()

def save_event():
    #todo
    print()

def main():
    # creds = get_credentials()
    # if update_needed_calendars():
    #     my_calendar_list = get_calendars(creds)
    #     save_calendars(my_calendar_list)

    # LS read from file
    # check_saved_events_file()
    read_ls_txt_file() #todo make these 3 a method
    update_events()

    # todo: Get events from LS & Canvas
    #       Add events to calendar
    #       Store added & old events
    #       Store class name, source, calendar name, event ID....

    # todo eventually: Asks what calendars are assigned to what classes
    #       Ask....

# This Allows You to Execute Code When the File Runs as a Script,
# but Not When It's Imported as a Module
if __name__ == '__main__':
    main()