from pydantic import ValidationError
from src.models import PaperInput, PaperMetadata
import arxiv

class PaperScraper:
    def __init__(self):
        self.client = arxiv.Client()

    def scrape_papers(self, input_data: PaperInput):
        try:
            search = arxiv.Search(
                query=input_data.query,
                max_results=input_data.max_results,
                sort_by=arxiv.SortCriterion.Relevance
            )
            papers = []
            for result in self.client.results(search):
                try:
                    metadata = PaperMetadata(
                        title=result.title,
                        abstract=result.summary
                    )
                    papers.append({
                        "title": metadata.title,
                        "abstract": metadata.abstract
                    })
                except ValidationError as e:
                    print(f"Skipping invalid paper: {e}")
                    continue
            return papers
        except Exception as e:
            print(f"Error fetching papers: {e}")
            return []

def test_scraper():
    input_data = PaperInput(query="machine learning", max_results=2)
    scraper = PaperScraper()
    papers = scraper.scrape_papers(input_data)
    print(f"Scraped {len(papers)} papers:")
    for paper in papers:
        print(f"Title: {paper['title']}")
        print(f"Abstract: {paper['abstract'][:100]}...")
        print("-" * 50)

if __name__ == "__main__":
    test_scraper()