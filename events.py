
from GoogleAPI import insert_new_canvas_event
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
            hw_event = insert_new_canvas_event(creds, hw)
            all_new_events.append(hw_event)

    #This file is just in case something bad happens. It will save everything that was run. 
    save_event_overwrite_to_file(all_new_events, 'OOPS.json')
    save_event_append_to_file(all_new_events, EVENT_FILE)


# Must both come from same source (LS, Canvas, or other)
def compare_saved_events(saved_events, new_events):
    # since they are in the same order, shouldn't take too long
    # Compare
    i_new = 0
    i_save = 0
    while i_save < len(saved_events) and i_new < len(new_events):
        # checks for same event
        if saved_events[i_save].event_name == new_events[i_new].event_name:
            # checks if due date changed
            if saved_events[i_save].event_due_date != new_events[i_new].event_due_date:
                print('Due date changed for ' + saved_events[i_save].event_name)
                # TODO: call update

            # looks for next event
            i_new += 1
            i_save += 1
            continue
        else:
            # TODO: needs logic for deleting, only goes through i_save
            # finds matching event
            i_temp = i_save
            found = False
            while i_temp < len(saved_events):
                # if events match, check if due date changed
                if saved_events[i_temp].event_name == new_events[i_new].event_name:
                    # checks if due date changed
                    if saved_events[i_save].event_due_date != new_events[i_new].event_due_date:
                        print('Due date changed for ' + saved_events[i_save].event_name)
                        found = True
                        # TODO: call update
                    # exits while loop
                    i_new += 1
                    break
                i_temp += 1
            # needs to look through
            # insert if not found
            if not found:
                pass 
                #TODO: call add
                # add_due_dates_events(new_events[i_new].event_class, [new_events[i_new]], creds, my_calendars)
    
