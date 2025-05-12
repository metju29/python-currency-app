import json
import logging
from datetime import datetime, timedelta

# Configure logger
logger = logging.getLogger(__name__)

def generate_dates(start_date_str):
    logger.info(f"Generating dates from {start_date_str} to today")
    # String conversion to a date object
    start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
    end_date = datetime.now().date() #today
    logger.debug(f"Date range: {start_date} to {end_date}")

    # Date generation
    date_list = [] # List of resulting dates
    current_date = start_date
    while current_date <= end_date:
        date_list.append((current_date.year, current_date.month, current_date.day))
        current_date += timedelta(days=1)
    
    logger.info(f"Generated {len(date_list)} dates")
    return date_list