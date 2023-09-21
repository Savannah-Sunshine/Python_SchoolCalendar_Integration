import sys
from busy import print_busiest
from util import Event, read_json_file, file_exists, save_overwrite_to_file, read_ls_txt_file, read_other_json_file, read_canvas_txt_file
from GoogleAPI import get_credentials, get_google_calendars
from CanvasAPI import get_Canvas_Classes
from events import add_due_dates_events

# If modifying scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar']
CALENDAR_FILE = 'files/calendars.json'
OOPS_FILE = 'OOPS.json'

LS_TRGT_EVENT_FILE = 'files/LS_events.json'
CANVAS_TRGT_EVENT_FILE = 'files/canvas_events.json'
OTHER_TRGT_EVENT_FILE = 'files/other_events.json'

LS_SRC_FILE = 'files/LS_sept6.txt'
CANVAS_SRC_FILE = 'files/c_cs312_grades_sept8.json'
# CANVAS_SRC_FILE = 'files/c_relc_grades_sept8.json'
OTHER_SRC_FILE = 'files/o_404_readings_sept8.json'
# OTHER_SRC_FILE = 'files/o_312_readings_sept8.json'


def main():
    creds = get_credentials()

    my_calendar_list = None
    if file_exists(CALENDAR_FILE):
        # TODO check if calendars are correct?
        # TODO check if calendars are old?
        my_calendar_list = read_json_file(CALENDAR_FILE)
    else:
        print("No Calendar File")
        my_calendar_list = get_google_calendars(creds)
        save_overwrite_to_file(my_calendar_list, CALENDAR_FILE)
        # TODO: Assign ids to classes using canvas api
        # canvas_classes = get_Canvas_Classes()
        



    assignments : [Event] = []

    if len(sys.argv) != 2:
        print('Add some arguments (all, ls, canvas, other)')
        return
    
    elif sys.argv[1].lower() == 'ls':
        # Get events to add - LS
        assignments = read_ls_txt_file(LS_SRC_FILE)
        EVENT_FILE = LS_TRGT_EVENT_FILE

    elif sys.argv[1].lower() == 'canvas':
        # Get events to add - Canvas TODO
        assignments = read_other_json_file(CANVAS_SRC_FILE)
        EVENT_FILE = CANVAS_TRGT_EVENT_FILE
        
    elif sys.argv[1].lower() == 'other':
        # Get events to add - Other
        assignments = read_other_json_file(OTHER_SRC_FILE)
        EVENT_FILE = OTHER_TRGT_EVENT_FILE
    else:
        print("You typed in " + sys.argv[1])
        return

    # add due dates to events
    # print("DATA PUT INTO " + EVENT_FILE)
    # add_due_dates_events(EVENT_FILE, assignments, creds, my_calendar_list)

    # check for updates


    # prints busiest times of semester
    # print_busiest(assignments)



    # TODO eventually: Asks what calendars are assigned to what classes
    #                  Ask what time to save due date



def update_class():
    # Do per class
    # Get events to add





# This Allows You to Execute Code When the File Runs as a Script,
# but Not When It's Imported as a Module
if __name__ == '__main__':
    main()