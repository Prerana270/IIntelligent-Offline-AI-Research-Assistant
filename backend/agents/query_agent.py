from typing import List

class QueryAgent:
    """Improves user queries for retrieval and generation."""

    def rewrite(self, query: str, conversation_history: List[dict] = None) -> str:
        if not query or not query.strip():
            raise ValueError("Query cannot be empty.")

        original = query.strip()
        improved = original

        # 1) Ensure the query is phrased as a question for better generation.
        if "?" not in improved:
            improved += "?"

        # 2) Expand short queries.
        if len(original) < 20:
            improved = f"Please clarify and expand: {improved}"

        # 3) Handle vague queries by adding a hint.
        vague_keywords = ["something", "anything", "info", "details", "stuff"]
        if any(word in original.lower() for word in vague_keywords):
            improved = f"In a precise way, {improved}"

        # 4) Include conversation context if available.
        if conversation_history:
            last_user = conversation_history[-1].get("user") if conversation_history[-1] else None
            if last_user and last_user.strip().lower() != original.lower():
                improved = f"Considering the previous statement: '{last_user}', {improved}"

        print(f"[QueryAgent] original={original}")
        print(f"[QueryAgent] improved={improved}")

        return improved
