import json
from datetime import datetime, timedelta


class Event:
    def __init__(self, event_calendar_id, event_class, event_due_date, event_id, event_name):
        self.event_calendar_id = event_calendar_id
        self.event_class = event_class
        self.event_id = event_id
        self.event_name = event_name
        if event_due_date is not None and type(event_due_date) is str:
            self.event_due_date = convert_to_datetime(event_due_date)
        elif event_due_date is not None:
            self.event_due_date = event_due_date
        else:
            self.event_due_date = None

    def to_json(self):
        return {
            "event_calendar_id": self.event_calendar_id,
            "event_class": self.event_class,
            "event_due_date": self.event_due_date.strftime('%Y-%m-%dT%H:%M:%S-06:00'),
            "event_id": self.event_id,
            "event_name": self.event_name
        }

class EventEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Event):
            return obj.to_json()
        return super().default(obj)

class Class:
    def __init__(self, class_id, class_name, class_google_calendar_id, class_google_calendar_name, class_source):
        self.class_id = class_id
        self.class_name = class_name
        self.class_google_calendar_id = class_google_calendar_id
        self.class_google_calendar_name = class_google_calendar_name
        self.class_source = class_source

    def to_json(self):
        return {
            "class_id": self.class_id,
            "class_name": self.class_name,
            "class_google_calendar_id": self.class_google_calendar_id,
            "class_google_calendar_name": self.class_google_calendar_name,
            "class_source": self.class_source
        }

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