from util_objects import Event, EventEncoder, Class
import json
import os.path
import re

def read_json_file(file_name):
    # Load the JSON data from the file
    try: 
        with open(file_name, 'r') as file:
            return json.load(file)
    except Exception as error:
         print('An error occurred: %s' % error)
         print('Probably have to delete something on json file')
    return []

def file_exists(file_name):
    return os.path.exists(file_name)

def save_overwrite_to_file(array, file_name):
    # Save the calendars in JSON for the next run
    with open(file_name, 'w') as calendars:
        calendars.write(json.dumps(array, ))

def save_event_overwrite_to_file(array, file_name):
    # Save the calendars in JSON for the next run
    with open(file_name, 'w') as calendars:
        calendars.write(json.dumps(array, cls=EventEncoder))



# TODO There's a better way
def save_append_to_file(dict_array, file_name, id):
    old_data = []
    if file_exists(file_name):
        old_data = read_json_file(file_name)
        for new_row in dict_array: 
            found_in_old_data = False
            for old_row in old_data:
                if old_row[id] == new_row[id]:
                    old_row = new_row.to_json()
                    found_in_old_data = True
                    break
            if not found_in_old_data:
                old_data.append(new_row.to_json())
    else:
        old_data = dict_array

    with open(file_name, 'w') as file:
        file.write(json.dumps(old_data))


def save_event_append_to_file(event_array: [Event], file_name):
    
    old_data = []
    if file_exists(file_name):
        old_data = read_json_file(file_name)
        for new_row in event_array: 
            # TODO: This stuff below is for if it updates, but it currently doesn't update events
            # for old_row in old_data:
            #     print(old_row['event_name'])
            #     print(new_row.event_name)
                
                #     old_row = new_row.to_json() #todo, fix
                #     found_in_old_data = True
                #     break
            # if not found_in_old_data:
            old_data.append(new_row.to_json())
    else:
        old_data = event_array

    with open(file_name, 'w') as file:
        file.write(json.dumps(old_data))


def read_ls_txt_file(file_name):
    
    if not file_exists(file_name):
        return None
    
    with open(file_name, 'r') as LS_HW:
        lines = [word for line in LS_HW for word in re.split(r'[\n\t]+', line) if word]

    assignments = []
    for i in range(0, len(lines), 3):
        assignments.append(Event(None, lines[i+1], lines[i+2], None, lines[i])) #todo, might need to assign cal ID again

    return assignments


# JSON MUST LOOK LIKE THIS
# {
#     "event_class_name": "C S 324 - Systems Programming",
#     "event_due_date": "Dec 4",
#     "event_name": "9.4 - 9.6"
# }
def read_other_json_file(file_name, cal_id): 
    lines = read_json_file(file_name)
    assignments : [Event] = []
    for reading in lines:
        assignments.append(Event(cal_id, reading['event_class_name'], reading['event_due_date'], None, reading['event_name']))
    return assignments

def read_canvas_txt_file(file_name):
    return 


def read_json_Classes(file_name):
    json_obj = read_json_file(file_name)
    classes = []
    for values in json_obj:
        classes.append(Class(values['class_id'], values['class_name'],
             values['class_google_calendar_id'], values['class_google_calendar_name'],
             values['class_source']))
    return classes

def read_json_Events(file_name):
    json_obj = read_json_file(file_name)
    events = []
    for values in json_obj:
        events.append(Event(values['event_calendar_id'], values['event_class'],
             values['event_due_date'], values['event_id'], values['event_name']))
    return events