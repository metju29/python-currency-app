import logging
from sqlalchemy import create_engine, text

# Get logger
logger = logging.getLogger(__name__)

def make_connection_string(config):
    logger.info("Creating database connection string")
    if config["db_type"] == "sqlite":
        logger.debug(f"Using SQLite database: {config['sqlite_database_file']}")
        con_str = f"sqlite:///{config['sqlite_database_file']}"

    elif config["db_type"] == "postgresql":
        logger.debug(f"Using PostgreSQL database: {config['db_name']} on {config['db_host']}")
        con_str = f"postgresql+psycopg2://{config['db_user']}:{config['db_pass']}@{config['db_host']}:{config['db_port']}/{config['db_name']}"

    else:
        logger.warning(f"Unsupported database type: {config['db_type']}")
        con_str = ""

    return con_str


def open_db(config):
    logger.info("Opening database connection")
    connection_str = make_connection_string(config)
    try:
        db_engine = create_engine(connection_str)
        db_con = db_engine.connect()
        logger.info("Database connection established successfully")
        return db_con
    except Exception as e:
        logger.error(f"Failed to connect to database: {str(e)}")
        raise


def close_db(db):
    logger.info("Closing database connection")
    try:
        db.close()
        logger.info("Database connection closed successfully")
    except Exception as e:
        logger.error(f"Error while closing database connection: {str(e)}")
        raise


def make_db_table(db_con):
    logger.info("Creating database table 'rates' if not exists")
    query = '''
        CREATE TABLE IF NOT EXISTS rates (
            data DATE NOT NULL,
            currency_code VARCHAR NOT NULL,
            exchange_rate FLOAT NOT NULL,
            PRIMARY KEY (data, currency_code)
        );
        '''
    
    try:
        db_con.execute(text(query))
        logger.info("Table 'rates' created or already exists")
    except Exception as e:
        logger.error(f"Failed to create table 'rates': {str(e)}")
        raise

def save_data_to_db(currency, db_con):
    logger.info(f"Saving currency data to database: {currency.get('code')} for date {currency.get('data')}")
    
    # Validate required fields
    required_fields = ['data', 'code', 'mid']
    missing_fields = [field for field in required_fields if field not in currency]
    if missing_fields:
        error_msg = f"Missing required fields in currency data: {', '.join(missing_fields)}"
        logger.error(error_msg)
        raise ValueError(error_msg)

    insert_query = """
    INSERT INTO rates (data, currency_code, exchange_rate)
    VALUES (:data, :code, :mid)
    """

    try:
        logger.debug(f"Executing insert query for currency: {currency['code']}")
        db_con.execute(text(insert_query), currency)
        db_con.commit()
        logger.info(f"Successfully saved currency data: {currency['code']} for date {currency['data']}")
    except Exception as e:
        logger.error(f"Error while saving currency data to database: {str(e)}")
        raise

def load_data_from_db(db_con, currency, start_date, end_date):
    params = {
        "currency": currency.upper(),
        "start_date": start_date,
        "end_date": end_date,
    }

    query = f"""
    SELECT
        data, exchange_rate
    FROM 
        rates
    WHERE
        currency_code = :currency
        AND data >= :start_date
        AND data <= :end_date
    ORDER BY
        data ASC;
    """
    
    # Try to fetch data from the database
    try:
        db_results = db_con.execute(text(query), params)
    except Exception as e:
        # If failed, log the error and return an empty list
        logger.error(f"Failed to fetch exchange rates: {str(e)}")
        return []
    
    results = []
    for r in db_results:
        # Element [0] = date, [1] = rate
        results.append({"date": r[0], "rate": r[1]})
    
    return results

def currency_list_from_db(db_con):
    query = """
        SELECT DISTINCT
            currency_code
        FROM
            rates
        ORDER BY
            currency_code ASC;
    """

    # Try to fetch currency codes from the database
    try:
        db_results = db_con.execute(text(query))
    except Exception as e:
        # If failed, log the error and return an empty list
        logger.error(f"Failed to fetch currency list: {str(e)}")
        return []
    
    # Convert database results to a list
    results = [r[0] for r in db_results]

    return results

def date_range_from_db(db_con, currency_code):
    query = """
        SELECT 
            MIN(data) AS min_date,
            MAX(data) AS max_date
        FROM 
            rates
        WHERE 
            currency_code = :currency_code;
    """
    try:
        # Execute the query and fetch the result
        result = db_con.execute(text(query), {"currency_code": currency_code}).fetchone()
        # Check if the result is not empty and contains valid dates
        if result and result[0] and result[1]:
            return result[0], result[1]
        else:
            return None, None

    except Exception as e:
        # Log the error and return None for both dates
        logger.error(f"Failed to fetch date range for {currency_code}: {str(e)}")
        return None, None