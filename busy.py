import datetime
import sys







def print_busiest(assignments):
    #sort assignments by date
    assignments.sort(key=lambda x: x.event_datetime)

    # get number of assignments per weekday and week of year
    weekday_num_assignments = [0,0,0,0,0,0,0]
    week_num_assignments = {}
    for assignment in assignments:
        # Gets weekday number (0-6 ~ Mon-Sun)
        weekday_num_assignments[assignment.event_datetime.weekday()] += 1

        # Gets week number of the year
        week_num = assignment.event_datetime.isocalendar()[1]
        if week_num in week_num_assignments:
            week_num_assignments[week_num] += 1
        else:
            week_num_assignments[week_num] = 1

    # find which weekday has the most assignments
    day = find_largest_in_list(weekday_num_assignments)
    print(' ' + get_day_from_day_num(day[0]) + ' is busiest with ' + str(day[1]) + ' assignments')


    # find which week has the most assignments
    week_num_assignments = sorted(week_num_assignments.items(), key=lambda x: x[1], reverse=True)
    print("Most assignments are due the week of:")
    print_date_from_weeknum(assignments[0], week_num_assignments[0])
    print("Least amount assignments are due the week of:")
    print_date_from_weeknum(assignments[0], week_num_assignments[len(week_num_assignments)-1])




def find_largest_in_list(list):
    max = 0
    id = 0
    for i in range(0, len(list)):
        if list[i] > max:
            max = list[i]
            id = i
    return [id, max]


def print_date_from_weeknum(first_week, assignment_weeknum_num):
    year = 0
    first_week_num = first_week.event_datetime.isocalendar()[1]
    if(assignment_weeknum_num[0] < first_week_num):
        year = first_week.event_datetime.year + 1
    else:
        year = first_week.event_datetime.year

    week_num = assignment_weeknum_num[0]
    date = datetime.datetime.strptime(f'{year} {week_num} {1}', "%Y %W %w")
    # print date like monday, septemeber 1st
    print(date.strftime("%A, %B %d"))

def get_day_from_day_num(day_num: int):
    if day_num == 0:
        return "Monday"
    elif day_num == 1:
        return "Tuesday"
    elif day_num == 2:
        return "Wednesday"
    elif day_num == 3:
        return "Thursday"
    elif day_num == 4:
        return "Friday"
    elif day_num == 5:
        return "Saturday"
    elif day_num == 6:
        return "Sunday"
    else:
        return "Invalid day number"