
import json
from canvasapi import Canvas
from util import Class, Event
from datetime import datetime
# curl -H "Authorization: Bearer 7407~NVNI6mAihNpFxdS2YrQr3xNe1sd6oXNvuTtTkx8ZSq88NUl0A0rrYy8rxfUzDRtM" "https://canvas.instructure.com/api/v1/courses"        

# Canvas API URL
API_URL = "https://canvas.instructure.com"
saved_canvas: Canvas = None
DATE_FORMAT = "%Y-%m-%dT%H:%M:%SZ"


def get_Canvas_Obj():
    global saved_canvas
    if saved_canvas is None:
        # Canvas API key
        API_KEY =  json.load(open('files/canvas_auth.json'))['token']

        # Initialize a new Canvas object
        saved_canvas = Canvas(API_URL, API_KEY)
    return saved_canvas


def get_Canvas_Classes():
    canvas = get_Canvas_Obj()
    user = canvas.get_user('self')
    active_courses = user.get_courses(enrollment_type='student', enrollment_state='active')
    
    # total = 0
    classes = []
    for course in active_courses:
        # total += 1
        # print(course.name + " " + str(course.id) + " " + str(course.end_at))
        classes.append(Class(course.id, course.name, None, None))
    
    return classes
    
def get_Canvas_Assignments_as_Events(class_id):
    canvas = get_Canvas_Obj()
    course = canvas.get_course(class_id)
    assignments = course.get_assignments()
    
    #Todo, assign the ones with no due_date to last due obj
    temp_due_date = datetime.strptime("2020-12-21T23:59:59Z", DATE_FORMAT)
    events = []
    for assignment in assignments:
        print(assignment.due_at)
        if(assignment.due_at is None):
            events.append(Event(class_id, assignment.name, temp_due_date, assignment.id, assignment.name))
        else:
            due_date = datetime.strptime(assignment.due_at, DATE_FORMAT)
            events.append(Event(class_id, assignment.name, due_date, assignment.id, assignment.name))
    return events