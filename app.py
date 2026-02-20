import os
import logging
import uuid
from fastapi import FastAPI
import chromadb
import ollama

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)

MODEL_NAME = os.getenv("MODEL_NAME", "tinyllama")
USE_MOCK_LLM = os.getenv("USE_MOCK_LLM", "0") == "1"

logging.info(f"Using model: {MODEL_NAME}")
logging.info(f"Mock mode: {USE_MOCK_LLM}")

chroma = chromadb.PersistentClient(path="./db")
collection = chroma.get_or_create_collection("docs")

app = FastAPI()


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/query")
def query(q: str):
    results = collection.query(query_texts=[q], n_results=1)
    context = results["documents"][0][0] if results["documents"] else ""

    if USE_MOCK_LLM:
        answer = context
    else:
        response = ollama.generate(
            model=MODEL_NAME,
            prompt=f"Context:\n{context}\n\nQuestion: {q}\n\nAnswer clearly and concisely:"
        )
        answer = response["response"]

    logging.info(f"/query asked: {q}")
    
    return {"answer": answer}


@app.post("/add")
def add_knowledge(text: str):
    """Add new content to the knowledge base dynamically."""
    try:
        doc_id = str(uuid.uuid4())
        collection.add(documents=[text], ids=[doc_id])
        
        logging.info(f"/add received new text (id: {doc_id})")
        
        return {
            "status": "success",
            "message": "Content added to knowledge base",
            "id": doc_id
        }
    except Exception as e:
        logging.error(f"/add failed: {str(e)}")
        return {
            "status": "error",
            "message": str(e)
        }