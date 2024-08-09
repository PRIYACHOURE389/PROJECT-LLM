from newsapi import NewsApiClient
import yaml
import os

def load_config(config_path):
    """Load configuration from a YAML file."""
    if not os.path.isfile(config_path):
        raise FileNotFoundError(f"The file {config_path} was not found.")
    
    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)
        return config

def setup_api_keys(config_path):
    """Set up API keys from the configuration file."""
    config = load_config(config_path)
    
    # Ensure the 'api_keys' section is present
    if 'api_keys' not in config:
        raise KeyError("Missing 'api_keys' section in config.")
    
    openai_section = config['api_keys'].get('openai')
    newsapi_section = config['api_keys'].get('newsapi')
    
    # Ensure both API keys are present
    if openai_section is None or 'api_key' not in openai_section:
        raise KeyError("Missing 'openai' section or 'api_key' in config.")
    if newsapi_section is None or 'api_key' not in newsapi_section:
        raise KeyError("Missing 'newsapi' section or 'api_key' in config.")
    
    openai_api_key = openai_section['api_key']
    newsapi_key = newsapi_section['api_key']
    return openai_api_key, newsapi_key

def initialize_newsapi(newsapi_key):
    """Initialize the NewsAPI client."""
    return NewsApiClient(api_key=newsapi_key)

def fetch_news(newsapi, query, language='en', page_size=100):
    """Fetch news articles based on a query."""
    try:
        response = newsapi.get_everything(q=query, language=language, page_size=page_size)
        if 'articles' in response:
            return response['articles']
        else:
            print(f"Unexpected response format: {response}")
            return []
    except Exception as e:
        print(f"Error fetching news: {e}")
        return []

def save_articles_to_file(articles, file_path):
    """Save fetched articles to a file."""
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            for article in articles:
                file.write(f"Title: {article.get('title', 'No title available')}\n")
                file.write(f"Description: {article.get('description', 'No description available')}\n")
                file.write(f"URL: {article.get('url', 'No URL available')}\n")
                file.write("\n")
        print(f"Articles saved to {file_path}")
    except Exception as e:
        print(f"Error saving articles to file: {e}")

if __name__ == "__main__":
    # Corrected config path
    config_path = r"C:\Users\admin\OneDrive\Desktop\llm project\config\config.yaml"
    print(f"Config path: {config_path}")

    try:
        openai_api_key, newsapi_key = setup_api_keys(config_path)
        newsapi = initialize_newsapi(newsapi_key)
        articles = fetch_news(newsapi, 'equity research', page_size=100)
        
        if articles:
            for article in articles:
                print(article.get('title', 'No title available'))
            save_articles_to_file(articles, r'C:\Users\admin\OneDrive\Desktop\llm project\equity_research_articles.txt')
        else:
            print("No articles found.")
    except (FileNotFoundError, KeyError) as e:
        print(f"Error: {e}")
