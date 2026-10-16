
from fastapi import FastAPI

app = FastAPI(title="RAG Learning API")


@app.get("/")
def home():
    return {"message": "Welcome to the RAG Learning API"}


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "message": "API is running successfully"
    }
