from langchain_community.llms import Ollama
from typing import List


class GeneratorAgent:
    def __init__(self, model_name: str = "llama3"):
        print(f"[GeneratorAgent] Initializing Ollama model '{model_name}'...")
        self.llm = Ollama(model=model_name)

    def generate(self, question: str, context_docs: List[dict], max_tokens: int = 512) -> str:
        context_text = "\n\n".join([f"Source {i+1}: {d.page_content}" for i, d in enumerate(context_docs)])

        prompt = (
            "You are an offline AI research assistant."
            " Use only the provided context to answer the question and avoid hallucinations."
            " If the context does not contain the answer, say 'I could not find enough information in the documents.'"
            "\n\n" 
            f"Context:\n{context_text}\n\n"
            f"Question: {question}\n\nAnswer:"
        )

        print(f"[GeneratorAgent] Generating response with prompt length={len(prompt)}")
        response = self.llm.invoke(prompt)
        print(f"[GeneratorAgent] Raw response: {response}")
        return response
