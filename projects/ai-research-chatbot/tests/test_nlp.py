from src.bot import ResearchBot
from src.models import PaperInput
import pytest

def test_bot_valid_query():
    bot = ResearchBot()
    response = bot.answer_query("machine learning", max_results=2)
    assert isinstance(response, dict)
    assert response["status"] in ["success", "partial", "error"]
    assert isinstance(response["results"], list)
    if response["status"] == "success":
        assert all("similarity" in result for result in response["results"])

def test_bot_invalid_query():
    bot = ResearchBot()
    response = bot.answer_query("ml", max_results=200)
    assert response["status"] == "error"
    assert "Invalid query" in response["message"]

def test_bot_no_results():
    bot = ResearchBot()
    response = bot.answer_query("obscure topic with no papers", max_results=1)
    assert response["status"] in ["error", "partial"]
    assert "No relevant" in response["message"] or "No papers" in response["message"]