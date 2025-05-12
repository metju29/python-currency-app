import logging
import yaml
from pathlib import Path

# Configure logger
log_file = Path(__file__).parent.parent / 'currency_app.log'
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

def load_config(file_path="config.yaml"):
    logger.info(f"Loading configuration from {file_path}")
    # Required configuration parameters
    REQUIRED_PARAMS = ("start_date", "currencies")
    
    # Default configuration
    default_config = {
        "start_date": "2024-01-01",
        "currencies": ["eur", "usd", "chf"],
        "output_folder": "rates",
        "save_to_file": True,
        "save_to_db": False,
        "db_type": "sqlite",
        "sqlite_database_file": "data.sqlite"
    }
    
    try:
        with open(file_path, "r") as file:
            user_config = yaml.safe_load(file)
            logger.debug("Configuration file loaded successfully")
            
        # Update default configuration with values from file
        default_config.update(user_config)
        logger.debug("Default configuration updated with user values")
        
        # Check if all required parameters are present
        missing_params = [param for param in REQUIRED_PARAMS if param not in default_config]
        if missing_params:
            logger.error(f"Missing required configuration parameters: {', '.join(missing_params)}")
            raise ValueError(f"Missing required configuration parameters: {', '.join(missing_params)}")
            
        logger.info("Configuration loaded successfully")
        return default_config
    except FileNotFoundError:
        logger.warning(f"Configuration file {file_path} not found. Using default configuration.")
        return default_config
    except Exception as e:
        logger.error(f"Error occurred while loading configuration: {str(e)}")
        return default_config