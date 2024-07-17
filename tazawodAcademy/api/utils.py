from datetime import datetime

def get_weekday(specific: int = 0):
    if specific > 6 or specific < -6:
        raise ValueError("specific must be between -6 and 6")

    # Get the current date
    today = datetime.today()
    # Get the weekday (0=Monday, 6=Sunday)
    weekday = today.weekday() + specific
    if weekday > 6:
        weekday = weekday - 7
    elif weekday < 0:
      weekday = weekday + 7
    
    # Convert the weekday number to the corresponding weekday name
    weekdays = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    weekday_name = weekdays[weekday]

    return weekday_name
