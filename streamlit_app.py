import streamlit as st
import yaml
import json
import pandas as pd
from datetime import datetime
from utils import (
    load_config,
    setup_api_keys,
    initialize_newsapi,
    fetch_news,
    preprocess_text,
    summarize_article,
    analyze_sentiment,
    perform_topic_clustering,
    save_to_file,
    user_authentication,
    load_articles
)
import logging
import os

# Create a logging directory if it doesn't exist
log_dir = "C:/Users/admin/OneDrive/Desktop/PROJECT-LLM/logs"
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

# Configure logging
log_file = os.path.join(log_dir, 'app.log')

logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Load configuration
try:
    config_path = "C:/Users/admin/OneDrive/Desktop/PROJECT-LLM/config/config.yaml"
    config = load_config(config_path)
    logging.info('Configuration loaded successfully.')
except Exception as e:
    logging.error(f'Error loading configuration: {e}')
    st.error(f"Error loading configuration: {e}")

# Setup API keys
try:
    newsapi_key = setup_api_keys(config_path)
    newsapi = initialize_newsapi(newsapi_key)
    logging.info('API keys set up successfully.')
except Exception as e:
    logging.error(f'Error setting up API keys: {e}')
    st.error(f"Error setting up API keys: {e}")

# Apply custom CSS
st.markdown("""
    <style>
        @import url('/style.css');
    </style>
""", unsafe_allow_html=True)

# Streamlit App
st.title(config.get('streamlit', {}).get('title', 'Default Title'))
st.sidebar.title(config.get('streamlit', {}).get('sidebar_title', 'Login'))
st.sidebar.subheader('Login')

# User Authentication
username = st.sidebar.text_input('Username')
password = st.sidebar.text_input('Password', type='password')

if st.sidebar.button('Login'):
    if user_authentication(username, password, config_path):
        st.sidebar.success("Logged in successfully")
        logging.info(f'User {username} logged in successfully.')
    else:
        st.sidebar.error("Invalid username or password")
        logging.warning(f'Failed login attempt for user {username}.')

# Initialize a list to keep track of query and summary history
if 'history' not in st.session_state:
    st.session_state.history = []

# News fetching and display
st.header("Fetch and Analyze News Articles")

query = st.text_input("Enter search query:")
num_results = st.slider("Number of articles to display", min_value=1, max_value=100, value=10)

if st.button('Fetch News'):
    if query:
        try:
            articles = fetch_news(newsapi, query)
            if articles:
                # Limit the number of articles to display based on user input
                articles_to_display = articles[:num_results]
                st.write(f"Displaying {len(articles_to_display)} articles out of {len(articles)} found.")
                logging.info(f'Fetched {len(articles_to_display)} articles for query: {query}')
                
                summaries = []
                for article in articles_to_display:
                    title = article['title']
                    description = article['description']
                    url = article['url']
                    content = article['content'] or ""
                    
                    # Display the article with custom styling
                    with st.container():
                        st.markdown(f"""
                            <div class="article">
                                <h2>{title}</h2>
                                <p><strong>Description:</strong> {description}</p>
                                <p><a href="{url}" target="_blank">Read more</a></p>
                                <p><strong>Summary:</strong> {summarize_article(content)}</p>
                                <p><strong>Sentiment:</strong> {analyze_sentiment(content)}</p>
                                <p><strong>Accuracy:</strong> <input type="range" min="1" max="5" value="3" disabled> 3</p>
                                <p><strong>Relevance:</strong> <input type="range" min="1" max="5" value="3" disabled> 3</p>
                            </div>
                            <hr />
                        """, unsafe_allow_html=True)
                    
                    # Save to history
                    summaries.append({
                        'title': title,
                        'description': description,
                        'url': url,
                        'summary': summarize_article(content),
                        'accuracy': st.slider(f"Rate summary accuracy for '{title}' (1: Poor, 5: Excellent)", 1, 5, 3, key=f"accuracy_{title}"),
                        'relevance': st.slider(f"Rate summary relevance for '{title}' (1: Poor, 5: Excellent)", 1, 5, 3, key=f"relevance_{title}"),
                        'sentiment': analyze_sentiment(content),
                        'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    })
                
                # Add to session state history
                st.session_state.history.append({
                    'query': query,
                    'summaries': summaries
                })
            else:
                st.error("No articles found.")
                logging.info(f'No articles found for query: {query}')
        except Exception as e:
            logging.error(f'Error fetching or displaying news: {e}')
            st.error(f"Error fetching or displaying news: {e}")

# Save query and summaries to a file
if st.button('Export Summaries'):
    if st.session_state.history:
        file_type = st.radio('Select file type to export', ['CSV', 'JSON'])
        export_data = []
        for entry in st.session_state.history:
            for summary in entry['summaries']:
                export_data.append({
                    'query': entry['query'],
                    **summary
                })
        
        try:
            if file_type == 'CSV':
                df = pd.DataFrame(export_data)
                csv_file = "exported_summaries.csv"
                df.to_csv(csv_file, index=False)
                st.download_button('Download CSV', csv_file)
                logging.info('Exported summaries to CSV.')
            elif file_type == 'JSON':
                json_file = "exported_summaries.json"
                with open(json_file, 'w') as f:
                    json.dump(export_data, f, indent=4)
                st.download_button('Download JSON', json_file)
                logging.info('Exported summaries to JSON.')
        except Exception as e:
            logging.error(f'Error exporting summaries: {e}')
            st.error(f"Error exporting summaries: {e}")
    else:
        st.error("No data available to export.")
        logging.warning("Attempted to export summaries but no data was available.")

# Historical Data Analysis
st.header("Historical Data Analysis")

if st.session_state.history:
    st.write("Historical Queries and Summaries:")
    for entry in st.session_state.history:
        st.write(f"Query: {entry['query']}")
        for summary in entry['summaries']:
            st.subheader(summary['title'])
            st.write(f"Summary: {summary['summary']}")
            st.write(f"Accuracy: {summary['accuracy']}")
            st.write(f"Relevance: {summary['relevance']}")
            st.write(f"Sentiment: {summary['sentiment']}")
            st.write("---")
else:
    st.write("No historical data available.")

# Load and display sample articles for selection
st.header("Select Sample Article for Topic Clustering")

sample_articles_path = "C:/Users/admin/OneDrive/Desktop/PROJECT-LLM/config/sample_articles.json"

def load_sample_articles(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except Exception as e:
        logging.error(f"Error loading sample articles: {e}")
        st.error(f"Error loading sample articles: {e}")
        return []

sample_articles = load_sample_articles(sample_articles_path)

if sample_articles:
    titles = [article['title'] for article in sample_articles]
    selected_title = st.selectbox("Select an article title", titles)

    if selected_title:
        selected_article = next(article for article in sample_articles if article['title'] == selected_title)
        st.subheader(selected_article['title'])
        st.write(f"Description: {selected_article['description']}")
        st.write(f"Content: {selected_article['content']}")

        # Perform topic clustering on the selected article
        st.write("Topic Clustering Results:")
        num_topics = st.slider("Select number of topics", min_value=2, max_value=10, value=5)

        if st.button("Perform Topic Clustering"):
            try:
                clustered_topics = perform_topic_clustering([selected_article['content']], num_topics)
                st.write(f"Topic Clustering Results for {selected_article['title']}:")
                for i, topic in enumerate(clustered_topics):
                    st.write(f"Topic {i + 1}: {topic}")
                logging.info(f"Performed topic clustering on article: {selected_title}")
            except Exception as e:
                logging.error(f"Error performing topic clustering: {e}")
                st.error(f"Error performing topic clustering: {e}")
else:
    st.write("No sample articles available.")
