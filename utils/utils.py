import json
from datetime import datetime, timedelta


def generate_dates(start_date_str):
    # String conversion to a date object
    start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
    end_date = datetime.now().date() #today

    # Date generation
    date_list = [] # List of resulting dates
    current_date = start_date
    while current_date <= end_date:
        date_list.append((current_date.year, current_date.month, current_date.day))
        current_date += timedelta(days=1)
    
    return date_list