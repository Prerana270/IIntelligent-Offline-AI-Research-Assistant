import os
import shutil
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from langchain.schema import Document

from utils.embeddings import get_embeddings
from utils.loader import get_loader, split_documents
from vectorstore.faiss_store import FaissStore
from agents.query_agent import QueryAgent
from agents.retriever_agent import RetrieverAgent
from agents.generator_agent import GeneratorAgent
from agents.evaluator_agent import EvaluatorAgent

# --- 1. APP INITIALIZATION ---
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- 2. GLOBAL CONSTANTS ---
UPLOAD_DIR = "uploaded_files"
DB_DIR = "vector_db"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# --- 3. MODULE INITIALIZATION ---
print("[Startup] Initializing embedding model and agents...")
embeddings = get_embeddings(model_name="all-MiniLM-L6-v2")
faiss_store = FaissStore(DB_DIR, embeddings)
query_agent = QueryAgent()
retriever_agent = RetrieverAgent(faiss_store)
generator_agent = GeneratorAgent(model_name="llama3")
evaluator_agent = EvaluatorAgent()
conversation_history = []

print("[Startup] Initialization complete.")

# --- 4. STORE UTILS ---

def safe_load_vector_store():
    if not faiss_store.is_loaded():
        if os.path.exists(DB_DIR):
            faiss_store.load()
        else:
            raise FileNotFoundError("Vector DB folder not found. Please upload/index documents first.")


# --- 5. API ENDPOINTS ---

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    print(f"[Upload] Saved file {file.filename} to {UPLOAD_DIR}")
    return {"filename": file.filename, "status": "saved"}


@app.post("/index/")
async def index_files():
    print("[Index] Starting indexing process...")
    filenames = os.listdir(UPLOAD_DIR)

    if not filenames:
        raise HTTPException(status_code=400, detail="No files uploaded to index.")

    documents = []
    for filename in filenames:
        file_path = os.path.join(UPLOAD_DIR, filename)
        try:
            loader = get_loader(file_path)
            if hasattr(loader, "load"):
                loaded_docs = loader.load()
            else:
                loaded_docs = loader

            if not loaded_docs:
                print(f"[Index] Warning: no docs loaded from {filename}")
                continue

            documents.extend(loaded_docs)
        except Exception as e:
            print(f"[Index] Error loading {filename}: {e}")

    if not documents:
        raise HTTPException(status_code=500, detail="Could not load any valid documents.")

    chunks = split_documents(documents, chunk_size=1000, chunk_overlap=150)
    faiss_store.create(chunks)
    print(f"[Index] Completed indexing of {len(filenames)} files")

    return {"status": "success", "indexed_files": len(filenames), "chunk_count": len(chunks)}


@app.post("/query/")
async def query_rag(payload: dict):
    user_query = payload.get("text")
    if not user_query or not user_query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty.")

    try:
        safe_load_vector_store()
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))

    print(f"[Pipeline] Received query: '{user_query}'")
    rewritten = query_agent.rewrite(user_query, conversation_history)

    retrieved_docs = retriever_agent.retrieve(rewritten, top_k=5)
    if not retrieved_docs:
        raise HTTPException(status_code=404, detail="No relevant context retrieved.")

    print("[Pipeline] Retrieved docs for context:")
    for d in retrieved_docs:
        print(f"  - source={d.metadata.get('source', '')} chunk_len={len(d.page_content)}")

    answer = generator_agent.generate(rewritten, retrieved_docs)
    evaluation = evaluator_agent.evaluate(answer, retrieved_docs)

    if not evaluation.get("passed"):
        print(f"[Evaluator] Weak answer detected: {evaluation.get('reason')}. Retrying once...")
        answer = generator_agent.generate(rewritten + "\n\nPlease refine based on document content.", retrieved_docs)
        evaluation = evaluator_agent.evaluate(answer, retrieved_docs)

    conversation_history.append({"user": user_query, "assistant": answer})

    sources = list({os.path.basename(d.metadata.get("source", "")) for d in retrieved_docs if d.metadata.get("source")})

    return {
        "query": user_query,
        "rewritten_query": rewritten,
        "answer": answer,
        "sources": sources,
        "evaluation": evaluation,
    }


@app.get("/health/")
def health_check():
    return {"status": "online", "message": "Intelligent Offline AI Research Assistant is running."}


print("--- Starting Intelligent Offline AI Research Assistant Backend ---")

