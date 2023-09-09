
from GoogleAPI import insert_new_event
from util import Event, read_json_file, save_event_append_to_file, file_exists, save_event_overwrite_to_file
EVENT_FILE = None
LS_SRC_FILE = None

def find_matching_event_by_name(look_for_event_name, all_events):
    for i_event in all_events:
        if i_event['event_name'] == look_for_event_name:
            return i_event
    return None

def check_event_needs_adding(event: Event, all_events):
    old_matching_event = find_matching_event_by_name(event.event_name, all_events)
    # If new event, add it
    if old_matching_event is None:
        return True
    
    return False

def assign_calendar_id(event_class_name, my_calendar_list):
    for calendar in my_calendar_list:
        if calendar.get('offical_class_name') == event_class_name:
            return calendar.get('calendar_id')
    return 'primary'


def add_due_dates_events(new_event_file, assignments: [Event], creds, my_calendars):
    EVENT_FILE = new_event_file

    if(assignments is None):
        print('No assignments found')
        return 'DONE'
    #TODO get dictionary from file & make sure it's not saved

    saved_events = []
    if file_exists(EVENT_FILE):
        saved_events = read_json_file(EVENT_FILE)

    all_new_events = []
    for hw in assignments:
        if saved_events is None or check_event_needs_adding(hw, saved_events):
            print(hw.event_name + ' will be added')
            hw.event_calendar_id = assign_calendar_id(hw.event_class,my_calendars)
            hw_event = insert_new_event(creds, hw)
            all_new_events.append(hw_event)

    #This file is just in case something bad happens. It will save everything that was run. 
    save_event_overwrite_to_file(all_new_events, 'OOPS.json')
    save_event_append_to_file(all_new_events, EVENT_FILE)
