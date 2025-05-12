import logging
import requests
from datetime import datetime

# Configure logger
logger = logging.getLogger(__name__)

def make_query_url(year, month, day, table="A"):
    logger.debug(f"Creating query URL for date: {year}-{month}-{day}, table: {table}")
    return f"https://api.nbp.pl/api/exchangerates/tables/{table}/{year:04}-{month:02}-{day:02}?format=json"


def get_rates(
        year, month, day, 
        table="A",
        expected_currencies=["eur", "usd", "gbp", "chf"]):
    logger.info(f"Fetching exchange rates for date: {year}-{month}-{day}")
    expected_currencies_lower = [
        element.lower()
        for element in expected_currencies
        ]
    logger.debug(f"Expected currencies: {expected_currencies_lower}")

    query_url = make_query_url(year, month, day, table)
    try:
        logger.debug(f"Making request to: {query_url}")
        result = requests.get(query_url)

        if result.status_code != 200:
            logger.error(f"API request failed with status code: {result.status_code}")
            return []
        
        table = result.json()[0]
        rates = table.get("rates", [])
        rates_filtered = [
            rate for rate in rates
            if rate["code"].lower() in expected_currencies_lower
        ]
        
        logger.info(f"Successfully retrieved {len(rates_filtered)} rates")
        data = datetime(year, month, day).date().strftime("%Y-%m-%d")
        for rate in rates_filtered:
            rate.update({"data": data})

        return rates_filtered
        
    except Exception as e:
        logger.error(f"Error while fetching rates: {str(e)}")
        return []
