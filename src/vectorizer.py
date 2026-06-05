import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class LocalVectorizer:
    def __init__(self, corpus_sentences: list):
        """
        corpus_sentences: lista de strings (user_inputs já pré-processadas)
        Usa unigramas + bigramas para melhor captura de contexto.
        """
        self.vectorizer = CountVectorizer(
            analyzer='word',
            ngram_range=(1, 2),
            min_df=1
        )
        self.corpus_vectors = self.vectorizer.fit_transform(corpus_sentences)

    def get_most_similar(self, query: str, threshold: float = 0.2):
        """
        Vetoriza a query e compara com todos os exemplos do corpus.

        Retorna:
            (best_idx, best_score) se score >= threshold
            (-1, best_score) caso nenhum supere o limiar
        """
        query_vec = self.vectorizer.transform([query])
        similarities = cosine_similarity(query_vec, self.corpus_vectors).flatten()
        best_idx = int(np.argmax(similarities))
        best_score = float(similarities[best_idx])

        if best_score >= threshold:
            return best_idx, best_score
        return -1, best_score
