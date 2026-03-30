from vectorstore.faiss_store import FaissStore

class RetrieverAgent:
    """Wraps the FAISS vector store retrieval logic."""

    def __init__(self, faiss_store: FaissStore):
        self.faiss_store = faiss_store

    def ensure_store(self):
        if not self.faiss_store.is_loaded():
            self.faiss_store.load()

    def retrieve(self, query: str, top_k: int = 5):
        self.ensure_store()
        docs = self.faiss_store.search(query, k=top_k)
        print(f"[RetrieverAgent] Retrieved {len(docs)} docs")
        return docs
