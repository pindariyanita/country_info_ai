from fastapi import FastAPI
from agent import build_graph

app = FastAPI()
graph = build_graph()

@app.get("/")
def home():
    return {"message": "Country Info AI Agent is running"}

@app.get("/ask")
def ask(query: str):
    result = graph.invoke({
        "query": query,
        "country": None,
        "fields": None,
        "api_response": None,
        "final_answer": None,
        "error": None
    })

    return {
        "query": query,
        "answer": result.get("final_answer")
    }