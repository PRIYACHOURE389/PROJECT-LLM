from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import LatentDirichletAllocation
from text_processing import preprocess_text

def perform_topic_clustering(documents, num_topics=5):
    preprocessed_docs = [preprocess_text(doc) for doc in documents]
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
