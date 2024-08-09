import streamlit as st
import openai
import yaml
import os
import json
from newsapi import NewsApiClient
from textblob import TextBlob
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import LatentDirichletAllocation
import nltk
import re

# Ensure necessary NLTK resources are available
nltk.download('punkt')

def load_config(config_path):
    """Load configuration from a YAML file."""
    if not os.path.isfile(config_path):
        st.error(f"File not found: {config_path}")
        return {}
    try:
        with open(config_path, 'r') as file:
            return yaml.safe_load(file)
    except Exception as e:
        st.error(f"Error loading configuration: {e}")
        return {}

def setup_api_keys(config):
    """Set up API keys from the configuration."""
    if 'api_keys' not in config:
        st.error("Missing 'api_keys' section in config.")
        return None, None
    openai_key = config['api_keys'].get('openai', {}).get('api_key')
    newsapi_key = config['api_keys'].get('newsapi', {}).get('api_key')
    if not openai_key or not newsapi_key:
        st.error("Missing API keys in config.")
        return None, None
    openai.api_key = openai_key
    return newsapi_key, openai_key

def initialize_newsapi(newsapi_key):
    """Initialize the NewsAPI client."""
    try:
        return NewsApiClient(api_key=newsapi_key)
    except Exception as e:
        st.error(f"Error initializing NewsAPI client: {e}")
        return None

def authenticate_user(username, password, users):
    """Authenticate the user based on the provided credentials."""
    for user in users:
        if user['username'] == username and user['password'] == password:
            return True
    return False

def preprocess_text(text):
    """Preprocess text by removing URLs, mentions, hashtags, and punctuations."""
    text = re.sub(r'http\S+|www\S+|https\S+', '', text)
    text = re.sub(r'\@\w+|\#', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    tokens = nltk.word_tokenize(text)
    tokens = [word.lower() for word in tokens if word.isalpha()]
    return ' '.join(tokens)

def summarize_article(article_text):
    """Generate a summary for the given article using OpenAI."""
    try:
        response = openai.Completion.create(
            engine="gpt-3.5-turbo",
            prompt=f"Summarize the following news article:\n\n{article_text}",
            max_tokens=150
        )
        return response.choices[0].text.strip()
    except openai.error.RateLimitError:
        return "Summary could not be generated. API quota exceeded."
    except Exception as e:
        return "Summary could not be generated due to an error."

def analyze_sentiment(text):
    """Analyze the sentiment of the text using TextBlob."""
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
        st.error(f"Error analyzing sentiment: {e}")
        return 'unknown'

def check_non_empty_documents(documents):
    """Ensure documents are not empty after preprocessing."""
    non_empty_docs = [doc for doc in documents if doc.strip()]
    if not non_empty_docs:
        raise ValueError("All documents are empty after preprocessing.")
    return non_empty_docs

def perform_topic_clustering(documents, num_topics=5):
    """Perform topic clustering using LDA."""
    preprocessed_docs = check_non_empty_documents([preprocess_text(doc) for doc in documents])
    vectorizer = TfidfVectorizer()
    doc_term_matrix = vectorizer.fit_transform(preprocessed_docs)

    if doc_term_matrix.shape[1] == 0:
        raise ValueError("Empty vocabulary after vectorization. Check preprocessing.")

    lda_model = LatentDirichletAllocation(n_components=num_topics, random_state=0)
    lda_topics = lda_model.fit_transform(doc_term_matrix)

    feature_names = vectorizer.get_feature_names_out()
    topics = []
    for topic_idx, topic in enumerate(lda_model.components_):
        top_words = [feature_names[i] for i in topic.argsort()[-10:]]
        topics.append((f"Topic {topic_idx}", top_words))
    return topics

def fetch_news(newsapi, query, language='en', page_size=100):
    """Fetch news articles based on a query."""
    try:
        response = newsapi.get_everything(q=query, language=language, page_size=page_size)
        if 'articles' in response:
            return response['articles']
        else:
            st.error(f"Unexpected response format: {response}")
            return []
    except Exception as e:
        st.error(f"Error fetching news: {e}")
        return []

def load_sample_articles(file_path):
    """Load sample articles from a JSON file."""
    if not os.path.isfile(file_path):
        st.error(f"File not found: {file_path}")
        return []
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except Exception as e:
        st.error(f"Error loading sample articles: {e}")
        return []

def log_feedback(feedback, feedback_log_path="feedback_log.txt"):
    """Log user feedback to a file."""
    if feedback:
        try:
            with open(feedback_log_path, 'a') as file:
                file.write(f"{feedback}\n")
        except Exception as e:
            st.error(f"Error logging feedback: {e}")

def main():
    """Main function for Streamlit app."""
    st.title("Equity Research News Tool")

    # Load configuration
    config_path = "C:\\Users\\admin\\OneDrive\\Desktop\\llm project\\config\\config.yaml"
    config = load_config(config_path)
    if not config:
        st.stop()

    # Authentication
    users = config.get('users', [])
    st.sidebar.title("Login")
    username = st.sidebar.text_input("Username")
    password = st.sidebar.text_input("Password", type="password")

    if st.sidebar.button("Login"):
        if authenticate_user(username, password, users):
            st.session_state.logged_in = True
            st.sidebar.success("Login successful!")
        else:
            st.sidebar.error("Invalid username or password.")
            st.session_state.logged_in = False
            st.stop()

    # Check if user is logged in
    if not st.session_state.get('logged_in', False):
        st.stop()

    # Setup API keys and initialize NewsAPI
    newsapi_key, openai_key = setup_api_keys(config)
    if not newsapi_key or not openai_key:
        st.stop()

    newsapi = initialize_newsapi(newsapi_key)
    if newsapi is None:
        st.stop()

    # Load and display sample articles
    sample_articles_path = "C:\\Users\\admin\\OneDrive\\Desktop\\llm project\\config\\sample_articles.json"
    sample_articles = load_sample_articles(sample_articles_path)

    if sample_articles:
        st.sidebar.title("Sample Articles")
        sample_article_titles = [article.get('title', 'No title available') for article in sample_articles]
        selected_title = st.sidebar.selectbox("Select a sample article", sample_article_titles)

        selected_article = next((article for article in sample_articles if article.get('title') == selected_title), None)
        if selected_article:
            st.subheader(selected_article.get('title', 'No title available'))
            st.write(selected_article.get('description', 'No description available'))
            st.write(f"[Read more]({selected_article.get('url', 'No URL available')})")

            # Summarize and analyze sentiment
            summary = summarize_article(selected_article.get('description', ''))
            sentiment = analyze_sentiment(selected_article.get('description', ''))
            st.write("Summary:", summary)
            st.write("Sentiment:", sentiment)

            st.write("\n")

    query = st.text_input("Enter search query")

    # Option to select the number of articles to view
    num_articles = st.sidebar.slider("Number of articles to view", min_value=1, max_value=100, value=10)

    if st.button("Fetch News"):
        if not query:
            st.error("Please enter a query.")
            st.stop()

        articles = fetch_news(newsapi, query, page_size=num_articles)
        if articles:
            st.write(f"Found {len(articles)} articles.")
            for article in articles:
                st.subheader(article.get('title', 'No title available'))
                st.write(article.get('description', 'No description available'))
                st.write(f"[Read more]({article.get('url', 'No URL available')})")

                # Summarize and analyze sentiment
                summary = summarize_article(article.get('description', ''))
                sentiment = analyze_sentiment(article.get('description', ''))
                st.write("Summary:", summary)
                st.write("Sentiment:", sentiment)

                st.write("\n")
        else:
            st.write("No articles found.")

    # Feedback area
    st.subheader("Feedback")
    feedback = st.text_area("Share your feedback about the tool")
    if st.button("Submit Feedback"):
        log_feedback(feedback)
        st.success("Thank you for your feedback!")

if __name__ == "__main__":
    main()
