# text_preprocessor.py

import re
import json
import nltk
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import LatentDirichletAllocation

# Ensure you have the necessary NLTK resources
nltk.download('punkt')

def preprocess_text(text):
    """Clean and preprocess text."""
    text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
    text = re.sub(r'\@\w+|\#', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    tokens = word_tokenize(text)
    tokens = [word.lower() for word in tokens if word.isalpha()]
    return ' '.join(tokens)

def check_non_empty_documents(documents):
    """Ensure documents are not empty after preprocessing."""
    non_empty_docs = [doc for doc in documents if doc.strip()]
    if not non_empty_docs:
        raise ValueError("All documents are empty after preprocessing.")
    return non_empty_docs

def load_json_file(file_path):
    """Load JSON file containing documents."""
    with open(file_path, 'r') as file:
        return json.load(file)

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

if __name__ == "__main__":
    # Path to JSON file containing sample documents
    file_path = r"C:\Users\admin\OneDrive\Desktop\llm project\sample_articles.json"

    try:
        raw_docs = load_json_file(file_path)
        documents = [doc['content'] for doc in raw_docs if 'content' in doc]

        if isinstance(documents, list):
            preprocessed_docs = [preprocess_text(doc) for doc in documents]
            non_empty_docs = check_non_empty_documents(preprocessed_docs)

            topics = perform_topic_clustering(non_empty_docs)
            for topic in topics:
                print(topic)
        else:
            print("Error: The loaded data is not in the expected format (list of documents).")
    except (FileNotFoundError, ValueError) as e:
        print(f"Error: {e}")
