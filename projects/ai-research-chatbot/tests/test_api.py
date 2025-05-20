from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {
        "message": "Welcome to the AI Research Assistant Chatbot API. Use POST /query to search papers."
    }

def test_query_valid():
    response = client.post("/query", json={"query": "machine learning", "max_results": 2})
    assert response.status_code == 200
    json_response = response.json()
    assert json_response["status"] in ["success", "partial", "error"]
    assert isinstance(json_response["results"], list)

def test_query_invalid():
    response = client.post("/query", json={"query": "ml", "max_results": 200})
    assert response.status_code == 400
    assert "Invalid query" in response.json()["detail"]