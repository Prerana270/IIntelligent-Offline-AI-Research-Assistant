import streamlit as st
import requests

st.title("Intelligent Offline AI Research Assistant")
st.write("Use this local Streamlit UI to query your indexed documents.")

API_URL = "http://localhost:8000"

if "history" not in st.session_state:
    st.session_state.history = []

query = st.text_input("Ask your question", "Summarize the key points")

if st.button("Submit"):
    if not query.strip():
        st.error("Please enter a question.")
    else:
        payload = {"text": query}
        try:
            res = requests.post(f"{API_URL}/query/", json=payload, timeout=60)
            res.raise_for_status()
            data = res.json()
            st.session_state.history.append(data)
        except Exception as e:
            st.error(f"Error calling backend: {e}")

if st.session_state.history:
    for i, entry in enumerate(reversed(st.session_state.history), start=1):
        st.subheader(f"Response #{i}")
        st.write("**Query:**", entry.get("query"))
        st.write("**Rewritten Query:**", entry.get("rewritten_query"))
        st.write("**Answer:**", entry.get("answer"))
        st.write("**Sources:**", entry.get("sources"))
        st.write("**Evaluation:**", entry.get("evaluation"))
        st.write("---")
