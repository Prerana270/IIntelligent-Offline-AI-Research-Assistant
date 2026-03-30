import os
from typing import List
from langchain_community.vectorstores import FAISS
from langchain.schema import Document


class FaissStore:
    def __init__(self, db_dir: str, embeddings):
        self.db_dir = db_dir
        self.embeddings = embeddings
        self.store = None

    def is_loaded(self) -> bool:
        return self.store is not None

    def save(self):
        if self.store:
            self.store.save_local(self.db_dir)
            print(f"[FaissStore] Saved index in {self.db_dir}")

    def load(self):
        if not os.path.exists(self.db_dir):
            raise FileNotFoundError(f"Vector store directory not found: {self.db_dir}")

        self.store = FAISS.load_local(self.db_dir, self.embeddings, allow_dangerous_deserialization=True)
        print(f"[FaissStore] Loaded index from {self.db_dir}")
        return self.store

    def create(self, documents: List[Document]):
        self.store = FAISS.from_documents(documents, self.embeddings)
        print(f"[FaissStore] Created vector store with {len(documents)} chunks")
        self.save()

    def search(self, query: str, k: int = 5):
        if not self.store:
            raise RuntimeError("Vector store is not loaded. Call load() or create() first.")

        retrieved = self.store.similarity_search(query, k=k)
        print(f"[FaissStore] Retrieved {len(retrieved)} documents for query '{query}'")
        return retrieved

    def add_documents(self, documents: List[Document]):
        if not self.store:
            raise RuntimeError("Vector store is not loaded. Call load() or create() first.")

        self.store.add_documents(documents)
        self.save()
        print(f"[FaissStore] Added {len(documents)} documents to the index")
