import datetime

def get_previous_sunday():
    today = datetime.date.today()
    weekday = today.weekday()

    if weekday == 6:  # If today is Sunday
        return today
    else:
        days_to_subtract = weekday + 1
        return today - datetime.timedelta(days=days_to_subtract)

previous_sunday = get_previous_sunday()
next_saturday = get_previous_sunday() + datetime.timedelta(days=6)