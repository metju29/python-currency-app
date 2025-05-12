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