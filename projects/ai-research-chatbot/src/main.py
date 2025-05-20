from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from src.bot import ResearchBot

app = FastAPI(title="AI Research Assistant Chatbot")

class QueryInput(BaseModel):
    query: str
    max_results: int = 5

@app.post("/query")
async def answer_query(input_data: QueryInput):
    bot = ResearchBot()
    response = bot.answer_query(input_data.query, input_data.max_results)
    if response["status"] == "error":
        raise HTTPException(status_code=400, detail=response["message"])
    return response

@app.get("/")
async def root():
    return {"message": "Welcome to the AI Research Assistant Chatbot API. Use POST /query to search papers."}