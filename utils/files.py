import logging
import json
from pathlib import Path

# Configure logger
logger = logging.getLogger(__name__)

def make_filename(year, month, day, currency, rates_dir_name="rates"):
    logger.debug(f"Creating filename for {currency} on {year}-{month}-{day}")
    # Catalog
    current_dir = Path()
    rates_dir = current_dir / rates_dir_name.lower()
    rates_dir.mkdir(exist_ok=True)
    currency_dir = rates_dir / currency.lower()
    currency_dir.mkdir(exist_ok=True)
    
    filename = currency_dir / f"{year:04}_{month:02}_{day:02}.json"
    logger.debug(f"Created filename: {filename}")
    return filename

def save_data_to_file(data, file_name):
    logger.info(f"Saving data to file: {file_name}")
    try:
        with open(f"{file_name}", "w", encoding="utf-8") as fp:
            json.dump(data, fp)
        logger.info("Data saved successfully")
    except Exception as e:
        logger.error(f"Error while saving data to file: {str(e)}")
        raise