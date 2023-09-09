from util import read_json_file, save_overwrite_to_file
from GoogleAPI import get_credentials, delete_event
from main import LS_TRGT_EVENT_FILE, LS_SRC_FILE

# If modifying scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar']

OOPS_FILE = 'OOPS.json'

def main():
    creds = get_credentials()

    # get everything from event file
    events_to_delete = read_json_file(OOPS_FILE)
    # clear event file
    # save_overwrite_to_file([], OOPS_FILE)

    # delete events
    if events_to_delete is not None:
        for event in events_to_delete:
            print('Deleting ' + event['event_name'])
            delete_event(event['event_id'], event['event_calendar_id'], creds)





# This Allows You to Execute Code When the File Runs as a Script,
# but Not When It's Imported as a Module
if __name__ == '__main__':
    main()