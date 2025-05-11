import yaml


def load_config(file_path="config.yaml"):
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
            
        # Update default configuration with values from file
        default_config.update(user_config)
        
        # Check if all required parameters are present
        missing_params = [param for param in REQUIRED_PARAMS if param not in default_config]
        if missing_params:
            raise ValueError(f"Missing required configuration parameters: {', '.join(missing_params)}")
            
        return default_config
    except FileNotFoundError:
        print(f"Configuration file {file_path} not found. Using default configuration.")
        return default_config
    except Exception as e:
        print(f"Error occurred while loading configuration: {str(e)}")
        return default_config