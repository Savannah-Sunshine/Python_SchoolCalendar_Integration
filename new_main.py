
import sys
from busy import print_busiest
from util import Event, Class, read_json_Classes, file_exists, save_event_append_to_file,  read_json_Events, read_ls_txt_file, read_other_json_file, read_canvas_txt_file
from GoogleAPI import get_credentials, get_google_calendars, insert_new_canvas_event
from CanvasAPI import get_Canvas_Classes, get_Canvas_Assignments_as_Events
from events import add_due_dates_events, compare_saved_events
from datetime import datetime


# If modifying scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar']
CALENDAR_FILE = 'files/new_calendars.json'
OOPS_FILE = 'OOPS.json'

LS_TRGT_EVENT_FILE = 'files/LS_events.json'
CANVAS_TRGT_EVENT_FILE = 'files/canvas_events.json'
OTHER_TRGT_EVENT_FILE = 'files/other_events.json'

LS_SRC_FILE = 'files/LS_sept6.txt'
CANVAS_SRC_FILE = 'files/c_cs312_grades_sept8.json'
# OTHER_SRC_FILE = 'files/o_404_readings_sept8.json'

OTHER_SRC_FILE = 'files/o_324_readings_sept19.json'
# OTHER_SRC_FILE = 'files/o_312_readings_sept8.json'



def main():
    creds = get_credentials()

    my_class_list : [Class] = []
    if file_exists(CALENDAR_FILE):
        # TODO check if calendars are correct?
        # TODO check if calendars are old?
        my_class_list = read_json_Classes(CALENDAR_FILE)
    else:
        print("No Calendar File")
        # my_calendar_list = get_google_calendars(creds)
        # save_overwrite_to_file(my_calendar_list, CALENDAR_FILE)
        

    # TODO: ASK USER WHICH CLASSES?

    # runs through all classes
    for cal_class in my_class_list:
        if cal_class.class_name is None or cal_class.class_name != "C S 324 - Systems Programming": #TODO TEMPOARY
            continue


        if cal_class.class_source == 'LS': #TODO can they have multiple sources?
            pass
        elif cal_class.class_source == 'Canvas':
            # canvas_do_events(cal_class.class_id)
            pass
        elif cal_class.class_source == 'Other':
            # other_get_old_events()
            # TODO set OTHER_SRC_FILE
            pass
            # Get new events
            # new_events = other_get_new_events(OTHER_SRC_FILE, cal_class.class_google_calendar_id)
            # # update/add events
            # other_add_events(creds, new_events)
            # # save added events
            # save_event_append_to_file(new_events, OTHER_TRGT_EVENT_FILE)
        else:
            continue





def other_get_new_events(file_name, class_cal_id):
    # Get new events
    new_events = read_other_json_file(file_name, class_cal_id)
    # print(saved_events[0].to_json())
    # compare_saved_events(saved_events, new_events)
    return new_events

def other_add_events(creds, events_to_update : [Event]):
    for event in events_to_update:
        # Only insert those we haven't done yet
        if event.event_due_date >= datetime.now(): 
            insert_new_canvas_event(creds, event)



def canvas_do_events(class_id):
    # Get old events
    EVENT_FILE = CANVAS_TRGT_EVENT_FILE #TODO
    if file_exists(EVENT_FILE):
        saved_events = read_json_Events(EVENT_FILE)
        if saved_events is None:
            pass #TODO do the else
            
        # Get new events
        new_events = get_Canvas_Assignments_as_Events(class_id)
        # print(new_events[0].to_json())
        # print(saved_events[0].to_json())
        compare_saved_events(saved_events, new_events)
        return #TODO remove this, only 1 class be fixed for now
    else:
        pass
        #add all events
        # Get new events



# This Allows You to Execute Code When the File Runs as a Script,
# but Not When It's Imported as a Module
if __name__ == '__main__':
    main()