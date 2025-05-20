from src.scraper import PaperScraper
from src.models import PaperInput
import pytest

def test_scraper_valid():
    input_data = PaperInput(query="machine learning", max_results=2)
    scraper = PaperScraper()
    papers = scraper.scrape_papers(input_data)
    assert isinstance(papers, list)
    assert len(papers) <= 2
    if papers:
        assert "title" in papers[0]
        assert "abstract" in papers[0]

def test_scraper_invalid_query():
    input_data = PaperInput(query="a", max_results=2)  # Invalid query length
    scraper = PaperScraper()
    with pytest.raises(ValueError):
        scraper.scrape_papers(input_data)