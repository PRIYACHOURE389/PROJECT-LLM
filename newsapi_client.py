from newsapi import NewsApiClient
import yaml

def load_config(config_path):
    with open(config_path, 'r') as file:
        return yaml.safe_load(file)

def setup_api_keys(config_path):
    config = load_config(config_path)
    openai_api_key = config['openai']['api_key']
    newsapi_key = config['newsapi']['api_key']
    return openai_api_key, newsapi_key

def initialize_newsapi(newsapi_key):
    return NewsApiClient(api_key=newsapi_key)

def fetch_news(newsapi, query, language='en', page_size=100):
    try:
        response = newsapi.get_everything(q=query, language=language, page_size=page_size)
        return response['articles']
    except Exception as e:
        print(f"Error fetching news: {e}")
        return []

def save_articles_to_file(articles, file_path):
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            for article in articles:
                file.write(f"Title: {article['title']}\n")
                file.write(f"Description: {article.get('description', 'No description available')}\n")
                file.write(f"URL: {article['url']}\n")
                file.write("\n")
        print(f"Articles saved to {file_path}")
    except Exception as e:
        print(f"Error saving articles to file: {e}")

if __name__ == "__main__":
    config_path = 'C:\\Users\\admin\\OneDrive\\Desktop\\PROJECT-LLM\\config\\config.yaml'
    openai_api_key, newsapi_key = setup_api_keys(config_path)
    newsapi = initialize_newsapi(newsapi_key)
    articles = fetch_news(newsapi, 'equity research', page_size=100)
    
    for article in articles:
        print(article['title'])
    
    save_articles_to_file(articles, 'C:\\Users\\admin\\OneDrive\\Desktop\\PROJECT-LLM\\equity_research_articles.txt')
