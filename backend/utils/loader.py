import os
from langchain_community.document_loaders import PyPDFLoader, UnstructuredCSVLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document


def get_loader(file_path: str):
    ext = os.path.splitext(file_path)[1].lower()
    if ext == ".pdf":
        return PyPDFLoader(file_path)
    elif ext == ".csv":
        return UnstructuredCSVLoader(file_path, mode="elements")
    elif ext in [".txt", ".md"]:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            text = f.read()
        return [Document(page_content=text, metadata={"source": file_path})]
    else:
        raise ValueError(f"Unsupported file extension: {ext}")


def split_documents(documents, chunk_size: int = 1000, chunk_overlap: int = 150):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    print(f"[Loader] Splitting {len(documents)} documents into chunks...")
    chunks = text_splitter.split_documents(documents)
    print(f"[Loader] Resulted in {len(chunks)} chunks")
    return chunks
