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

# Ensure you have the necessary NLTK resources
nltk.download('punkt')

def load_config(config_path):
    """Load configuration from a YAML file."""
    try:
        with open(config_path, 'r') as file:
            return yaml.safe_load(file)
    except Exception as e:
        print(f"Error loading configuration: {e}")
        return {}

def setup_api_keys(config_path):
    """Setup API keys from the configuration file."""
    config = load_config(config_path)
    openai.api_key = config.get('openai', {}).get('api_key', '')
    newsapi_key = config.get('newsapi', {}).get('api_key', '')
    if not openai.api_key or not newsapi_key:
        raise ValueError("API keys are missing in the configuration.")
    return newsapi_key

def initialize_newsapi(newsapi_key):
    """Initialize NewsAPI client with the provided API key."""
    try:
        return NewsApiClient(api_key=newsapi_key)
    except Exception as e:
        print(f"Error initializing NewsAPI client: {e}")
        return None

def fetch_news(newsapi, query, language='en', page_size=100):
    """Fetch news articles using the NewsAPI client."""
    try:
        if newsapi is None:
            raise ValueError("NewsAPI client is not initialized.")
        response = newsapi.get_everything(q=query, language=language, page_size=page_size)
        return response.get('articles', [])
    except Exception as e:
        print(f"Error fetching news: {e}")
        return []

def preprocess_text(text):
    """Preprocess the input text by removing URLs, mentions, hashtags, extra spaces, and non-alphabetic tokens."""
    text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)  # Remove URLs
    text = re.sub(r'\@\w+|\#', '', text)  # Remove mentions and hashtags
    text = re.sub(r'\s+', ' ', text).strip()  # Remove extra spaces
    tokens = nltk.word_tokenize(text)  # Tokenize
    tokens = [word.lower() for word in tokens if word.isalpha()]  # Remove non-alphabetic tokens
    return ' '.join(tokens)

def summarize_article(article_text):
    """Generate a summary of the provided article text using OpenAI."""
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
    non_empty_docs = check_non_empty_documents(preprocessed_docs)  # Ensure no empty documents

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
