import openai
import yaml
import json
import re
import chardet
import nltk
from newsapi import NewsApiClient
from textblob import TextBlob
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import LatentDirichletAllocation
import os

# Ensure you have the necessary NLTK resources
nltk.download('punkt')

def load_config(config_path):
    """Load configuration from a YAML file."""
    if not os.path.isfile(config_path):
        print(f"File not found: {config_path}")
        raise FileNotFoundError(f"The file {config_path} was not found.")
    
    try:
        with open(config_path, 'r') as file:
            return yaml.safe_load(file)
    except Exception as e:
        print(f"Error loading configuration: {e}")
        return {}

def setup_api_keys(config_path):
    """Set up API keys from the configuration file."""
    config = load_config(config_path)
    
    if 'api_keys' not in config:
        raise KeyError("Missing 'api_keys' section in config.")
    
    openai_section = config['api_keys'].get('openai')
    newsapi_section = config['api_keys'].get('newsapi')
    
    if openai_section is None or 'api_key' not in openai_section:
        raise KeyError("Missing 'openai' section or 'api_key' in config.")
    if newsapi_section is None or 'api_key' not in newsapi_section:
        raise KeyError("Missing 'newsapi' section or 'api_key' in config.")
    
    openai_api_key = openai_section['api_key']
    newsapi_key = newsapi_section['api_key']
    openai.api_key = openai_api_key
    return newsapi_key

def initialize_newsapi(newsapi_key):
    """Initialize the NewsAPI client."""
    try:
        return NewsApiClient(api_key=newsapi_key)
    except Exception as e:
        print(f"Error initializing NewsAPI client: {e}")
        return None

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

def preprocess_text(text):
    """Preprocess the input text."""
    text = re.sub(r'http\S+|www\S+|https\S+', '', text)  # Remove URLs
    text = re.sub(r'\@\w+|\#', '', text)  # Remove mentions and hashtags
    text = re.sub(r'\s+', ' ', text).strip()  # Remove extra spaces
    tokens = nltk.word_tokenize(text)
    tokens = [word.lower() for word in tokens if word.isalpha()]  # Remove non-alphabetic tokens
    return ' '.join(tokens)

def summarize_article(article_text):
    try:
        response = openai.Completion.create(
            engine="gpt-3.5-turbo",
            prompt=f"Summarize the following news article:\n\n{article_text}",
            max_tokens=150
        )
        return response.choices[0].text.strip()
    except Exception as e:
        print(f"Error summarizing article: {e}")
        return "Summary could not be generated."

def analyze_sentiment(text):
    """Analyze sentiment of the provided text using TextBlob."""
    try:
        blob = TextBlob(text)
        sentiment_polarity = blob.sentiment.polarity
        if sentiment_polarity > 0:
            return 'positive'
        elif sentiment_polarity < 0:
            return 'negative'
        else:
            return 'neutral'
    except Exception as e:
        print(f"Error analyzing sentiment: {e}")
        return 'unknown'

def check_non_empty_documents(documents):
    """Ensure there are non-empty documents for processing."""
    non_empty_docs = [doc for doc in documents if doc.strip()]
    if not non_empty_docs:
        raise ValueError("All documents are empty after preprocessing.")
    return non_empty_docs

def perform_topic_clustering(documents, num_topics=5):
    """Perform topic clustering on the provided documents using LDA."""
    preprocessed_docs = [preprocess_text(doc) for doc in documents]
    non_empty_docs = check_non_empty_documents(preprocessed_docs)

    vectorizer = TfidfVectorizer()
    doc_term_matrix = vectorizer.fit_transform(non_empty_docs)
    lda_model = LatentDirichletAllocation(n_components=num_topics, random_state=0)
    lda_topics = lda_model.fit_transform(doc_term_matrix)
    
    feature_names = vectorizer.get_feature_names_out()
    topics = []
    for topic_idx, topic in enumerate(lda_model.components_):
        top_words = [feature_names[i] for i in topic.argsort()[-10:]]
        topics.append((f"Topic {topic_idx}", top_words))
    
    return topics

def load_sample_articles(file_path):
    """Load sample articles from a JSON file."""
    if not os.path.isfile(file_path):
        st.error(f"File not found: {file_path}") # type: ignore
        return []
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except Exception as e:
        st.error(f"Error loading sample articles: {e}") # type: ignore
        return []

def save_to_file(filename, data):
    """Save data to a JSON file."""
    try:
        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4)
        return True
    except Exception as e:
        print(f"Error saving data to file: {e}")
        return False

def user_authentication(username, password, config_file):
    """Authenticate a user based on provided username and password."""
    try:
        with open(config_file, 'r') as file:
            users = yaml.safe_load(file).get('users', [])
            for user in users:
                if user['username'] == username and user['password'] == password:
                    return True
        return False
    except Exception as e:
        print(f"Error loading user configuration: {e}")
        return False

def detect_encoding(file_path):
    """Detect the encoding of a file."""
    with open(file_path, 'rb') as file:
        result = chardet.detect(file.read())
    return result['encoding']

def load_articles(file_path):
    """Load articles from a JSON file."""
    encoding = detect_encoding(file_path)
    try:
        with open(file_path, 'r', encoding=encoding) as f:
            articles = json.load(f)
        return articles
    except json.JSONDecodeError:
        print("Error: The JSON file is not properly formatted.")
        return []
    except FileNotFoundError:
        print("Error: The file was not found.")
        return []
    except UnicodeDecodeError:
        print("Error: The file encoding is not compatible.")
        return []
