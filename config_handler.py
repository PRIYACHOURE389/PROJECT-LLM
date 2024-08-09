import yaml

def load_config(file_path):
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

config_path = r"C:\Users\admin\OneDrive\Desktop\llm project\config\config.yaml"  # Use raw string or forward slashes
try:
    config = load_config(config_path)
    openai_api_key = config['api_keys']['openai']['api_key']
    newsapi_key = config['api_keys']['newsapi']['api_key']
    print("API keys loaded successfully.")
    print(f"OpenAI API Key: {openai_api_key}")
    print(f"NewsAPI Key: {newsapi_key}")
except FileNotFoundError:
    print(f"Error: Configuration file {config_path} not found.")
except KeyError as e:
    print(f"Error: Missing key {e} in the configuration file.")
except yaml.YAMLError as exc:
    print(f"Error parsing YAML file: {exc}")
