
import json
from canvasapi import Canvas
from util import Class, Event
# curl -H "Authorization: Bearer 7407~NVNI6mAihNpFxdS2YrQr3xNe1sd6oXNvuTtTkx8ZSq88NUl0A0rrYy8rxfUzDRtM" "https://canvas.instructure.com/api/v1/courses"        

# Canvas API URL
API_URL = "https://canvas.instructure.com"
saved_canvas: Canvas = None

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
    
def get_Canvas_Assignments_Events(class_id):
    canvas = get_Canvas_Obj()
    course = canvas.get_course(class_id)
    assignments = course.get_assignments()
    
    events = []
    for assignment in assignments:
        events.append(Event(class_id, assignment.name, assignment.due_at, assignment.id, assignment.name))

    print(events[0].to_json())
    return events

get_Canvas_Assignments_Events('74070000000022233')