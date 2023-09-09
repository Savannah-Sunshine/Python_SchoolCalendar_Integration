import os.path
import json
import re
from datetime import datetime, timedelta


class Event:
    def __init__(self, event_calendar_id, event_class, event_due_date, event_id, event_name):
        self.event_calendar_id = event_calendar_id
        self.event_class = event_class
        self.event_due_date = event_due_date
        self.event_id = event_id
        self.event_name = event_name

    def to_json(self):
        return {
            "event_calendar_id": self.event_calendar_id,
            "event_class": self.event_class,
            "event_due_date": self.event_due_date,
            "event_id": self.event_id,
            "event_name": self.event_name
        }

class EventEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Event):
            return obj.to_json()
        return super().default(obj)

def json_to_Event(values):
    return Event(values['event_calendar_id'], values['event_class'],
                 values['event_due_date'], values['event_id'], values['event_name'])



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

# Thanks GPT
def convert_to_datetime(date_string, time_string_military=None):
    # Define a mapping of month abbreviations to month numbers
    month_mapping = {
        'jan': 1, 'feb': 2, 'mar': 3, 'apr': 4,
        'may': 5, 'jun': 6, 'jul': 7, 'aug': 8,
        'sep': 9, 'oct': 10, 'nov': 11, 'dec': 12
    }
    
    try:
        # Split the input date string
        parts = date_string.lower().split()
        
        #Make sure string is 3 characters
        parts[0] = parts[0][0:3]

        # Extract the month and day
        month = month_mapping[parts[0]]
        day = int(parts[1])
        
        # Get the current year
        current_year = datetime.now().year
        
        # Create a datetime object with the year, month, and day
        rfc_date = datetime(current_year, month, day)

        
        if time_string_military is not None:
            # If a time string is provided, add the time to the datetime object
            time_parts = time_string_military.split(':')
            hour = int(time_parts[0])
            minute = int(time_parts[1])
            rfc_date = rfc_date.replace(hour=hour, minute=minute)
        else:
            #default date time is 7am
            rfc_date = rfc_date.replace(hour=7, minute=0)
        
        # Format the datetime object in RFC 3339 format
        # rfc3339_date = date_obj.strftime('%Y-%m-%dT%H:%M:%S-06:00')
        
        return rfc_date
    except (ValueError, KeyError, IndexError):
        return None

def read_ls_txt_file(file_name):
    
    if not file_exists(file_name):
        return None
    
    with open(file_name, 'r') as LS_HW:
        lines = [word for line in LS_HW for word in re.split(r'[\n\t]+', line) if word]

    assignments = []
    for i in range(0, len(lines), 3):
        assignments.append(Event(None, lines[i+1], lines[i+2], None, lines[i])) #todo, might need to assign cal ID again

    return assignments


def read_other_json_file(file_name): 
    lines = read_json_file(file_name)
    assignments = []
    for reading in lines:
        assignments.append(Event(None, reading['event_class_name'], reading['event_due_date'], None, reading['event_name'])) #todo, might need to assign cal ID again
    return assignments

def read_canvas_txt_file(file_name):
    return 
