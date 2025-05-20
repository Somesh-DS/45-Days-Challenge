from src.models import PaperInput, PaperMetadata
import pytest

def test_paper_input_valid():
    input_data = PaperInput(query="machine learning", max_results=20)
    assert input_data.query == "machine learning"
    assert input_data.max_results == 20

def test_paper_input_invalid():
    with pytest.raises(ValueError):
        PaperInput(query="ml", max_results=200)

def test_paper_metadata_valid():
    metadata = PaperMetadata(
        title="A Survey of Machine Learning",
        abstract="This paper reviews recent advances in machine learning."
    )
    assert metadata.title == "A Survey of Machine Learning"
    assert len(metadata.abstract) >= 10

def test_paper_metadata_invalid():
    with pytest.raises(ValueError):
        PaperMetadata(title="", abstract="Short")