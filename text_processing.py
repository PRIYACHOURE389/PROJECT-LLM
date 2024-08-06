import re
import nltk
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import LatentDirichletAllocation

# Ensure you have the necessary NLTK resources
nltk.download('punkt')

def preprocess_text(text):
    text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
    text = re.sub(r'\@\w+|\#', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    tokens = word_tokenize(text)
    tokens = [word.lower() for word in tokens if word.isalpha()]
    return ' '.join(tokens)

def check_non_empty_documents(documents):
    non_empty_docs = [doc for doc in documents if doc.strip()]
    if not non_empty_docs:
        raise ValueError("All documents are empty after preprocessing.")
    return non_empty_docs

# Sample documents
raw_docs = [
    "Check out this link: http://example.com! #example @user",
    "   Here is a sample text with mixed Case and extra spaces.  ",
    ""
]

# Preprocess documents
preprocessed_docs = [preprocess_text(doc) for doc in raw_docs]
non_empty_docs = check_non_empty_documents(preprocessed_docs)

# Vectorize
vectorizer = TfidfVectorizer()
try:
    doc_term_matrix = vectorizer.fit_transform(non_empty_docs)
    if doc_term_matrix.shape[1] == 0:
        raise ValueError("Empty vocabulary after vectorization. Check preprocessing.")
except ValueError as e:
    print(f"Vectorization Error: {e}")

# Topic Clustering
def perform_topic_clustering(documents, num_topics=5):
    preprocessed_docs = check_non_empty_documents([preprocess_text(doc) for doc in documents])
    vectorizer = TfidfVectorizer()
    doc_term_matrix = vectorizer.fit_transform(preprocessed_docs)
    lda_model = LatentDirichletAllocation(n_components=num_topics, random_state=0)
    lda_topics = lda_model.fit_transform(doc_term_matrix)
    feature_names = vectorizer.get_feature_names_out()
    topics = []
    for topic_idx, topic in enumerate(lda_model.components_):
        top_words = [feature_names[i] for i in topic.argsort()[-10:]]
        topics.append((f"Topic {topic_idx}", top_words))
    return topics
