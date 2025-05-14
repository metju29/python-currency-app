from utils.config import load_config, logger
from utils.db import close_db, make_db_table, open_db, save_data_to_db
from utils.files import make_filename, save_data_to_file
from utils.utils import generate_dates
from utils.web import get_rates

CONFIG_FILE = "config.yaml"

def main():
    # Load configuration from YAML file
    logger.info("Loading configuration from YAML file...")
    config = load_config(CONFIG_FILE)

    # Generate a list of dates for which rates should be fetched
    logger.info(f"Generating date list starting from {config['start_date']}...")
    rate_dates = generate_dates(config["start_date"])

    # Open database connection if saving to database is enabled
    if config["save_to_db"]:
        logger.info("Opening database connection...")
        db = open_db(config)
        make_db_table(db)

    # Iterate over each date to fetch and process rates
    for date in rate_dates:
        req_year, req_month, req_day = date  # Unpack tuple into three variables
        logger.debug(f"Fetching rates for {req_year}-{req_month:02}-{req_day:02}")
        nbp_rates = get_rates(
            req_year, req_month, req_day, expected_currencies=config["currencies"]
        )

        # Process each currency rate
        for currency in nbp_rates:
            currency_code = currency["code"]
            if config["save_to_file"]:
                filename = make_filename(
                    req_year,
                    req_month,
                    req_day,
                    currency_code,
                    rates_dir_name=config["output_folder"],
            )

            # Save data to file if enabled in config
            if config["save_to_file"]:
                logger.debug(f"Saving data to file: {filename}")
                save_data_to_file(currency, filename)

            # Save data to database if enabled in config
            if config["save_to_db"]:
                logger.debug(f"Saving data to database for currency: {currency_code}")
                save_data_to_db(currency, db)

    # Close database connection
    if config["save_to_db"]:
        logger.info("Closing database connection...")
        close_db(db)

if __name__ == "__main__":
    main()