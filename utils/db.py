from sqlalchemy import create_engine, text


def make_connection_string(config):
    if config["db_type"] == "sqlite":
        con_str = f"sqlite:///{config['sqlite_database_file']}"

    elif config["db_type"] == "postgresql":
        con_str = f"postgresql+psycopg2://{config['db_user']}:{config['db_pass']}@{config['db_host']}:{config['db_port']}/{config['db_name']}"

    else:
        con_str = ""

    return con_str


def open_db(config):
    connection_str = make_connection_string(config)
    db_engine = create_engine(connection_str)
    db_con = db_engine.connect()
    return db_con


def close_db(db):
    db.close()


def make_db_table(db_con):
    query = '''
        CREATE TABLE IF NOT EXISTS rates (
            data DATE NOT NULL,
            currency_code VARCHAR NOT NULL,
            exchange_rate FLOAT NOT NULL,
            PRIMARY KEY (data, currency_code)
        );
        '''
    
    db_con.execute(text(query))