from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class Indexer:
    def __init__(self):
        self.vectorizer = None
        self.tfidf_matrix = None
        self.documents = []

    def add_document(self, content):
        self.documents.append(content)

    def build_index(self):
        if not self.documents:
            raise ValueError("No documents to build index from.")
        self.vectorizer = TfidfVectorizer(stop_words='english')
        self.tfidf_matrix = self.vectorizer.fit_transform(self.documents)

    def search(self, query):
        print("Vectorizer:", self.vectorizer)
        print("TFIDF Matrix:", self.tfidf_matrix)
        if not self.vectorizer:
            raise ValueError("Indexer has not been built. Call build_index before searching.")
        query_vector = self.vectorizer.transform([query])
        similarities = cosine_similarity(query_vector, self.tfidf_matrix)
        sorted_indices = similarities.argsort().flatten()[::-1]
        results = [(self.documents[i], similarities[0, i]) for i in sorted_indices]
        return results
