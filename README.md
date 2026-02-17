# Build a RAG API with FAST API 
This is how companies build AI-powered API that developers can integerate into their apps, e.g  CHATGPT'S API for conversational AI, Github Copilot's  for code suggestions or translation services that understand context- these all use AI to power their responses.

In this project I would be building my own modern web frameworks like FastAPI, combined with RAG(Retrieval-Augmented Generation) to create intelligent APIs that answer questions based on your own knowledge base.

## Our Goal 
Building and packaging the app so it works anywhere, automating deployments when data changes, monitoring it for mistakes- that is how  intend to succeed at scale.

**What I will build**

You'll create a RAG (Retrieval-Augmented Generation) API using FastAPI + Chroma + Ollama (a local LLM) - and you'll run everything right on your own computer. That means you can complete the whole project without paying any API fees or relying on cloud services!

Your API will answer questions by searching your knowledge base, then using AI to generate accurate answers. You'll also get automatic, interactive API documentation with Swagger UI - the same tools professional developers use to build and test APIs, but all locally and for free.

### STEP 1

**Set Up Your Environment**

Time to set up Python and Ollama - the core tools for building your RAG API.

**In this step, you' re going to**:

1. Verify Python is istalled 
2. Install Ollama 
3. Pull the tinyllama model

Verify Python Installation

Using your terminal check if Python is installed using `python3 --version`

![alt text](<RAG api/Screenshot 2026-02-17 at 1.13.45 PM.png>)

Installation of Ollama 

Check if there is ollama on the computer with `ollama --version`

![alt text](<RAG api/Screenshot 2026-02-16 at 11.05.40 AM.png>)

If Ollama is not found, use `brew install --cask ollama`

![alt text](<RAG api/Screenshot 2026-02-16 at 11.05.58 AM.png>)

Verify Installation with `Ollama --version`

![alt text](<RAG api/Screenshot 2026-02-16 at 11.50.48 AM.png>)

Check if **Ollama** is running curl http://localhost:11434

**Pull tinyllama Model** 

Check if the model is available using `ollama list`

![alt text](<RAG api/Screenshot 2026-02-16 at 11.51.06 AM.png>)

Download the Model with `ollama pull tinyllama` 

![alt text](<RAG api/Screenshot 2026-02-17 at 1.35.40 PM.png>)

Test the model `ollama run tinyllama`

![alt text](<RAG api/Screenshot 2026-02-16 at 11.56.53 AM.png>)

The response might be inaccurate - that's why we need RAG! Exit with /bye or ctrl D


### STEP 2

**Set up your Python Environment**

In this step, you're going to:

1.Create a project folder
2.Create and activate a Python virtual environment
3.Install Python dependencies

![alt text](<RAG api/Screenshot 2026-02-16 at 11.58.30 AM.png>)

Using `python3 -m venv venv` and `ls` you will see `venv`

Activate virtual Environment with `source venv/bin/activate`

![alt text](<RAG api/Screenshot 2026-02-17 at 1.49.18 PM.png>)

Your prompt should show (venv) at the start.

**Install Dependencies**

> Verify pip is using your virtual environment: `pip --version`

![alt text](<RAG api/Screenshot 2026-02-17 at 1.53.05 PM.png>)

Path should include `venv.`
Install packages:
`pip install fastapi uvicorn chromadb ollama`

![alt text](<RAG api/Screenshot 2026-02-16 at 12.11.57 PM.png>)

Verify installation:

`pip list | grep -E "fastapi|uvicorn|chromadb|ollama"`

You should see all four packages with version numbers.

![alt text](<RAG api/Screenshot 2026-02-16 at 12.11.29 PM.png>)


### STEP 3

**Create Your Knowledge Base and Embeddings**

Python environment is set up. Now let's create the  knowledge base and convert it into embeddings that the RAG API can search through.

> Why do we need a knowledge base?
AI models like tinyllama have limited knowledge from their training data. By providing your own knowledge base, you can give the AI accurate, up-to-date information about specific topics. This is the "Retrieval" part of RAG - we retrieve relevant information before generating an answer.

In this step, you're going to:

1. Write content in your knowledge base
2. Create a script that prepares your content for AI search
3. Run the script to make your content searchable

Open your `Practice-rag-api` folder in VS-CODE (or your preferred IDE).

![alt text](<RAG api/Screenshot 2026-02-16 at 12.18.40 PM.png>)

**Create Knowledge Document**

> Create a new file k8s.txt with this content:

Kubernetes is a container orchestration platform used to manage containers at scale.

![alt text](<RAG api/Screenshot 2026-02-17 at 2.04.17 PM.png>)

> What is this file?
Your knowledge base - the source of information your RAG system will use to answer questions. When someone asks "What is Kubernetes?", the system searches this file for context.

**Create Embedding Script**

* Create `embed.py`

``import chromadb

client = chromadb.PersistentClient(path="./db")
collection = client.get_or_create_collection("docs")

with open("k8s.txt", "r") as f:
    text = f.read()

collection.add(documents=[text], ids=["k8s"])

print("Embedding stored in Chroma")``

![alt text](<RAG api/Screenshot 2026-02-17 at 2.11.48 PM.png>)

>What does this script do?
Reads k8s.txt and stores it in Chroma as embeddings (numerical representations) for semantic search. This prepares your knowledge base for the RAG system.

**Run Embedding Script**

Make sure your virtual environment is activated (`(venv)` in prompt):
`python embed.py`

![alt text](<RAG api/Screenshot 2026-02-16 at 12.17.05 PM.png>)

Perfect! Your knowledge base is ready.

Check your file explorer in Vscode. You should now see a new db/ folder inside your project directory.

![alt text](<RAG api/Screenshot 2026-02-17 at 2.15.34 PM.png>)

### STEP 4

knowledge base is now stored as embeddings in Chroma. Now to bring it all together - let's build an API that combines AI with document search to answer questions!

>What is an API?
An API (Application Programming Interface) lets software retrieve and share data with other apps. In this project, you'll build a web API that can answer questions using AI powered by your own knowledge base.

**In this step, you're going to**:

1. Create a FastAPI app
2. Run the API server

**Create FastAPI App**

Create `app.py`:

``from fastapi import FastAPI
import chromadb
import ollama

app = FastAPI()
chroma = chromadb.PersistentClient(path="./db")
collection = chroma.get_or_create_collection("docs")

@app.post("/query")
def query(q: str):
    results = collection.query(query_texts=[q], n_results=1)
    context = results["documents"][0][0] if results["documents"] else ""

    answer = ollama.generate(
        model="tinyllama",
        prompt=f"Context:\n{context}\n\nQuestion: {q}\n\nAnswer clearly and concisely:"
    )

    return {"answer": answer["response"]``

![alt text](<RAG api/Screenshot 2026-02-16 at 12.18.40 PM.png>)

**Run API Server**
Verify uvicorn is installed: `uvicorn --version`

![alt text](<RAG api/Screenshot 2026-02-17 at 2.37.02 PM.png>)

Check if Ollama is running?

![alt text](<RAG api/Screenshot 2026-02-17 at 2.39.41 PM.png>)

Should say "Ollama is running".
Start the server: `uvicorn app:app --reload`

![alt text](<RAG api/Screenshot 2026-02-17 at 2.41.24 PM.png>)


### STEP 5 

**Test Your RAG API**

Perfect! Your API server is running. Now let's test it to make sure everything works correctly!

Let's test your API using the command line first, then try FastAPI's feature called Swagger UI that lets you explore and test your API visually in your browser.

> What is Swagger UI?
Swagger UI is an automatically generated, interactive documentation page for your FastAPI server. It lets you visually explore your API's endpoints, see what parameters they accept, and even try them out right from your browser.

**In this step, you're going to**:
* Test your RAG API endpoint

**Call RAG Endpoint**

* Open a new terminal and test:
You should see:
{"answer":"Kubernetes is a container orchestration platform that helps manage containers at scale..."}

![alt text](<RAG api/Screenshot 2026-02-17 at 2.45.15 PM.png>)

Perfect! Your RAG system is working - it retrieved context from Chroma and used Ollama to generate an accurate answer!

**Explore with Swagger UI**

Open your browser: http://127.0.0.1:8000/docs
Test the /query endpoint with What is Kubernetes?

![alt text](<RAG api/Screenshot 2026-02-16 at 12.58.56 PM.png>)

This is your RAG API with interactive documentation - automatically generated by FastAPI!

## Add Dynamic Content to Your Knowledge Base

Ready for a challenge? Add a `/add ` `endpoint` that lets you dynamically add content to your knowledge base through the API

**To achieve this you're going to**:


You're going to add a new endpoint to your API that lets you dynamically add content to your knowledge base - the same way production APIs allow users to update data in real-time!

* Create a new /add POST endpoint
* Add content to Chroma dynamically
* Test your new endpoint in Swagger UI
* Showcase advanced API design skills in your documentation!

> What is dynamic content?
Dynamic content means information that can be added, updated, or removed while your application is running. Instead of editing `k8s.txt` and re-running `embed.py`, you'll add new information through an API call.

**Create the /add endpoint**
* Open app.py in Cursor
* Add this new endpoint after your existing /query endpoint:

@app.post("/add")
def add_knowledge(text: str):
    """Add new content to the knowledge base dynamically."""
    try:
        # Generate a unique ID for this document
        import uuid
        doc_id = str(uuid.uuid4())

        # Add the text to Chroma collection
        collection.add(documents=[text], ids=[doc_id])

        return {
            "status": "success",
            "message": "Content added to knowledge base",
            "id": doc_id
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }



![alt text](<RAG api/Screenshot 2026-02-17 at 3.00.47 PM.png>)

> What does this code do?
This endpoint accepts text, generates a unique ID using uuid, adds the text to the Chroma collection, and returns a success message with the document ID.

* Save the file

![alt text](<RAG api/Screenshot 2026-02-17 at 3.02.53 PM.png>)

**Add a `/health` endpoint**

DevOps teams use health endpoints for readiness/liveness probes.

Add this endpoint to `app.py`

`@app.get("/health")
def health():
    return {"status": "ok"}`

> Why a health endpoint?
Load balancers and orchestrators (like Kubernetes) ping /health to check if your app is ready to receive traffic.

**Make the model configurable**

Update the top of `app.py`:
`import os
import logging
`

Right after imports:

`
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)

MODEL_NAME = os.getenv("MODEL_NAME", "tinyllama")
logging.info(f"Using model: {MODEL_NAME}")
`

Update the `ollama.generate` call:

`answer = ollama.generate(
    model=MODEL_NAME,
    prompt=f"Context:\n{context}\n\nQuestion: {q}\n\nAnswer clearly and concisely:`"


)

`Add request logging`

Inside the `/query endpoint`, add:

`logging.info(f"/query asked: {q}")`

Inside the `/add endpoint`, add

`logging.info(f"/add received new text (id will be generated)")
`

`Test your new endpoint`

* Open Swagger UI: http://127.0.0.1:8000/docs
* You should see both endpoints: `POST /query` and `POST /add`

![alt text](<RAG api/Screenshot 2026-02-17 at 3.11.25 PM.png>)

* Click on POST /add

In the text field, enter:

Docker is a platform that uses containers to package applications with all their dependencies.

* Click Execute

![alt text](<RAG api/Screenshot 2026-02-16 at 1.56.21 PM.png>)

You should see a success response with a unique ID

**Test that the new content works**

* Go back to POST /query in Swagger UI
* Click Try it out
* Enter: What is Docker?

![alt text](<RAG api/Screenshot 2026-02-16 at 1.57.51 PM.png>)

You should see an answer that includes Docker information!

## Mission Accomplished 
Congratulations! You've successfully:

* Set up Python and Ollama for local AI development

* Built a RAG API using FastAPI, Chroma, and tinyllama

* Created interactive API documentation with Swagger UI

* Tested your API with both curl and Swagger UI

You now understand how to build production-ready APIs with automatic documentation - the same way professional developers create AI-powered services.