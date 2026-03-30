from typing import List

class EvaluatorAgent:
    """Simple heuristics-based evaluator to reduce hallucinations."""

    def evaluate(self, answer: str, retrieved_docs: List[dict]) -> dict:
        if not answer or not answer.strip():
            return {"passed": False, "score": 0.0, "reason": "Empty answer."}

        normalized = answer.strip().lower()
        weak_signals = ["i don't know", "not enough information", "can't answer", "unable to find"]
        if any(sig in normalized for sig in weak_signals):
            return {"passed": False, "score": 0.2, "reason": "Low confidence/unknown in answer."}

        if len(answer.split()) < 10:
            return {"passed": False, "score": 0.3, "reason": "Answer too short, maybe incomplete."}

        # Basic sanity: presence of source snippet words.
        context_text = " ".join(doc.page_content.lower() for doc in retrieved_docs)
        overlap = sum(1 for w in normalized.split() if w in context_text)
        score = min(1.0, overlap / max(1, len(normalized.split())))

        passed = score >= 0.2
        reason = "Good quality" if passed else "Low context overlap; potential hallucination." 
        return {"passed": passed, "score": score, "reason": reason}
