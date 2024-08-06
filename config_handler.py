import yaml

def load_config(config_path):
    """Load the YAML configuration file."""
    try:
        with open(config_path, 'r') as file:
            return yaml.safe_load(file)
    except Exception as e:
        raise RuntimeError(f"Error loading configuration file: {e}")

def setup_api_keys(config_path):
    """Set up API keys from the configuration file."""
    config = load_config(config_path)
    try:
        openai_api_key = config['openai']['api_key']
        newsapi_key = config['newsapi']['api_key']
        if not openai_api_key or not newsapi_key:
            raise ValueError("API keys are missing in the configuration.")
        return openai_api_key, newsapi_key
    except KeyError as e:
        raise KeyError(f"Missing key in configuration file: {e}")
    except Exception as e:
        raise RuntimeError(f"Error setting up API keys: {e}")
