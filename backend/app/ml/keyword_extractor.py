from sklearn.feature_extraction.text import TfidfVectorizer
import re

class KeywordExtractor:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(stop_words='english', max_features=20) # Sesuaikan max_features

    def extract_keywords(self, text: str) -> list:
        # Pra-pemrosesan teks (opsional, tergantung kualitas data)
        text = text.lower()
        text = re.sub(r'[^a-z\s]', '', text) # Hapus karakter non-alfabet

        # Fit dan transform teks
        self.vectorizer.fit([text])
        tfidf_matrix = self.vectorizer.transform([text])

        # Dapatkan feature names (kata-kata) dan skor TF-IDF
        feature_names = self.vectorizer.get_feature_names_out()
        tfidf_scores = tfidf_matrix.toarray()[0]

        # Gabungkan kata kunci dengan skornya dan urutkan
        keywords_with_scores = sorted(zip(feature_names, tfidf_scores), key=lambda x: x[1], reverse=True)

        formatted_keywords = []
        for keyword, score in keywords_with_scores:
            formatted_keywords.append({
                "keyword_text": keyword,
                "score": int(score * 100) # Konversi ke int untuk simplicity
            })
        return formatted_keywords