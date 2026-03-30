from langchain_community.embeddings import HuggingFaceEmbeddings


def get_embeddings(model_name: str = "all-MiniLM-L6-v2"):
    print(f"[Embeddings] Loading embedding model '{model_name}'...")
    emb = HuggingFaceEmbeddings(model_name=model_name)
    print("[Embeddings] Model loaded.")
    return emb
