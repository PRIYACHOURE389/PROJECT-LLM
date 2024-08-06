import streamlit as st
import json
import pandas as pd
from utils import (
    load_config, setup_api_keys, initialize_newsapi, fetch_news,
    preprocess_text, summarize_article, analyze_sentiment,
    perform_topic_clustering, save_to_file, user_authentication
)

def detect_encoding(file_path):
    import chardet
    with open(file_path, 'rb') as file:
        result = chardet.detect(file.read())
    return result['encoding']

def load_articles(file_path):
    import json
    encoding = detect_encoding(file_path)
    try:
        with open(file_path, 'r', encoding=encoding) as f:
            articles = json.load(f)
        return articles
    except json.JSONDecodeError:
        st.error("Error: The JSON file is not properly formatted.")
        return []
    except FileNotFoundError:
        st.error("Error: The file was not found.")
        return []
    except UnicodeDecodeError:
        st.error("Error: The file encoding is not compatible.")
        return []

def main():
    config_path = 'config/config.yaml'
    config = load_config(config_path)

    st.set_page_config(page_title=config.get('streamlit', {}).get('title', 'Equity Research News Tool'), layout="wide")

    st.title(config.get('streamlit', {}).get('title', 'Equity Research News Tool'))
    st.sidebar.title(config.get('streamlit', {}).get('sidebar_title', 'Article Summaries'))

    # User authentication
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False

    if not st.session_state.authenticated:
        st.sidebar.subheader("Login")
        username = st.sidebar.text_input("Username")
        password = st.sidebar.text_input("Password", type="password")

        if st.sidebar.button("Login"):
            if user_authentication(username, password, 'config/users.yaml'):
                st.session_state.authenticated = True
                st.sidebar.success("Login successful!")
            else:
                st.sidebar.error("Invalid username or password")

    if st.session_state.authenticated:
        query = st.sidebar.text_input("Enter query for news articles", value="equity research")

        if st.sidebar.button("Fetch News"):
            newsapi_key = setup_api_keys(config_path)
            newsapi = initialize_newsapi(newsapi_key)

            articles = fetch_news(newsapi, query)

            documents = [article.get('content', '') for article in articles]

            topics = perform_topic_clustering(documents)

            processed_articles = []
            for article in articles:
                title = article.get('title', 'No title')
                description = article.get('description', 'No description')
                content = article.get('content', '')

                preprocessed_content = preprocess_text(content)

                summary = "No content available for summary."
                if preprocessed_content:
                    summary = summarize_article(preprocessed_content)

                sentiment = analyze_sentiment(content)

                processed_articles.append({
                    'title': title,
                    'description': description,
                    'preprocessed_content': preprocessed_content,
                    'summary': summary,
                    'sentiment': sentiment
                })

            output_file = 'news_summaries.json'
            if save_to_file(output_file, {'articles': processed_articles, 'topics': topics}):
                st.success(f"Data saved to {output_file}")
            else:
                st.error("Error saving data.")

            st.subheader("Processed Articles")
            for article in processed_articles:
                st.markdown(f"### {article['title']}")
                st.write(f"**Description:** {article['description']}")
                st.write(f"**Preprocessed Content:** {article['preprocessed_content']}")
                st.write(f"**Summary:** {article['summary']}")
                st.write(f"**Sentiment:** {article['sentiment']}")
                st.write("---")

            st.subheader("Topics")
            topics_df = pd.DataFrame(topics, columns=["Topic", "Top Words"])
            st.write(topics_df)

            # Plotting topics with Seaborn
            st.subheader("Topic Distribution")
            import matplotlib.pyplot as plt
            import seaborn as sns
            fig, ax = plt.subplots()
            sns.barplot(x='Topic', y='Count', data=topics_df, ax=ax)
            st.pyplot(fig)

if __name__ == "__main__":
    main()
