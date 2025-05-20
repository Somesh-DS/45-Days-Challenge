from src.models import PaperInput
from src.scraper import PaperScraper
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


class ResearchBot:
    def __init__(self):
        self.scraper = PaperScraper()
        self.vectorizer = TfidfVectorizer(stop_words='english')

    def answer_query(self, query: str, max_results: int = 5):
        try:
            input_data = PaperInput(query=query, max_results=max_results)
            papers = self.scraper.scrape_papers(input_data)
            if not papers:
                return {"status": "error", "message": "No relevant papers found.", "results": []}

            # TF-IDF ranking
            abstracts = [paper['abstract'] for paper in papers]
            tfidf_matrix = self.vectorizer.fit_transform(abstracts + [query])
            similarities = cosine_similarity(tfidf_matrix[-1], tfidf_matrix[:-1]).flatten()

            # Sort papers by similarity
            ranked_indices = np.argsort(similarities)[::-1]
            responses = []
            for idx in ranked_indices[:3]:
                if similarities[idx] > 0.1:
                    responses.append({
                        "title": papers[idx]['title'],
                        "abstract": papers[idx]['abstract'][:200] + "...",
                        "similarity": float(similarities[idx])
                    })

            if responses:
                return {"status": "success", "message": "Found relevant papers.", "results": responses}
            return {
                "status": "partial",
                "message": "No highly relevant papers, but here are some results.",
                "results": [{"title": paper['title'], "abstract": paper['abstract'][:200] + "..."} for paper in
                            papers[:3]]
            }
        except ValueError as e:
            return {"status": "error", "message": f"Invalid query: {e}", "results": []}


def test_bot():
    bot = ResearchBot()
    response = bot.answer_query("machine learning", max_results=2)
    print("Query Response:", response)


if __name__ == "__main__":
    test_bot()