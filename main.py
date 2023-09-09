import sys
from util import read_json_file, file_exists, save_overwrite_to_file, read_ls_txt_file, read_other_json_file, read_canvas_txt_file
from GoogleAPI import get_credentials, get_calendars
from events import add_due_dates_events

# If modifying scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar']
CALENDAR_FILE = 'files/calendars.json'
OOPS_FILE = 'OOPS.json'

LS_TRGT_EVENT_FILE = 'files/LS_events.json'
CANVAS_TRGT_EVENT_FILE = 'files/canvas_events.json'
OTHER_TRGT_EVENT_FILE = 'files/other_events.json'

LS_SRC_FILE = 'files/LS_sept6.txt'
CANVAS_SRC_FILE = 'files/canvas_sept.txt'
OTHER_SRC_FILE = 'files/other_sept8.json'


def main():
    creds = get_credentials()

    my_calendar_list = None
    if file_exists(CALENDAR_FILE):
        # TODO check if calendars are correct?
        # TODO check if calendars are old?
        my_calendar_list = read_json_file(CALENDAR_FILE)
    else:
        print("No Calendar File")
        my_calendar_list = get_calendars(creds)
        save_overwrite_to_file(my_calendar_list, CALENDAR_FILE)



    assignments = []

    if len(sys.argv) != 2:
        print('Add some arguments (all, ls, canvas, other)')
        return
    
    elif sys.argv[1].lower() == 'ls':
        # Get events to add - LS
        assignments = read_ls_txt_file(LS_SRC_FILE)
        EVENT_FILE = LS_TRGT_EVENT_FILE

    elif sys.argv[1].lower() == 'canvas':
        # Get events to add - Canvas TODO
        assignments = read_canvas_txt_file(CANVAS_SRC_FILE)
        EVENT_FILE = CANVAS_TRGT_EVENT_FILE

    elif sys.argv[1].lower() == 'other':
        # Get events to add - Other
        assignments = read_other_json_file(OTHER_SRC_FILE)
        EVENT_FILE = OTHER_TRGT_EVENT_FILE

    # print(assignments)

    # update & add due dates to events
    add_due_dates_events(EVENT_FILE, assignments, creds)

    # TODO: Get events from Canvas
    # TODO eventually: Asks what calendars are assigned to what classes
    #                  Ask what time to save due date






# This Allows You to Execute Code When the File Runs as a Script,
# but Not When It's Imported as a Module
if __name__ == '__main__':
    main()