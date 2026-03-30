# � Intelligent Offline AI Research Assistant

### Multi-Agent RAG System for Private Document Analysis

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.111.0-green.svg)
![LangChain](https://img.shields.io/badge/LangChain-0.2.1-orange.svg)
![Ollama](https://img.shields.io/badge/Ollama-Llama3-red.svg)
![FAISS](https://img.shields.io/badge/FAISS-VectorDB-purple.svg)

---

## 🌟 Overview

**Intelligent Offline AI Research Assistant** is a cutting-edge, **100% offline** Retrieval-Augmented Generation (RAG) system powered by multiple AI agents. Upload your personal documents (PDFs, CSVs) and chat with them using advanced AI without any data leaving your computer.

### ✨ Key Features

- 🔒 **100% Private & Offline** - No cloud, no data leaks
- 🧠 **Multi-Agent Architecture** - Query understanding, retrieval, generation, and evaluation agents
- 📚 **Smart Document Processing** - PDF and CSV support with intelligent chunking
- 🧪 **Quality Assurance** - Built-in hallucination detection and retry mechanisms
- 🎨 **Optional Web UI** - Streamlit interface for easy interaction
- 🚀 **Interview-Ready Code** - Clean, modular, and production-grade

---

## 🏗️ Architecture

### Multi-Agent Pipeline

```
User Query
    ↓
Query Agent (Rewrite & Improve)
    ↓
Retriever Agent (FAISS Vector Search)
    ↓
Generator Agent (Ollama LLM)
    ↓
Evaluator Agent (Quality Check & Retry)
    ↓
Final Response
```

### Project Structure

```
Intelligent-Offline-RAG-Assistant/
│
├── backend/
│   ├── main.py                    # FastAPI server & agent orchestration
│   ├── agents/
│   │   ├── query_agent.py         # Query rewriting & clarification
│   │   ├── retriever_agent.py     # FAISS retrieval wrapper
│   │   ├── generator_agent.py     # Ollama LLM integration
│   │   └── evaluator_agent.py     # Answer quality evaluation
│   ├── utils/
│   │   ├── embeddings.py          # HuggingFace embeddings loader
│   │   └── loader.py              # Document loading & chunking
│   ├── vectorstore/
│   │   └── faiss_store.py         # FAISS vector database management
│   ├── requirements.txt           # Python dependencies
│   ├── streamlit_app.py           # Optional web UI
│   ├── uploaded_files/            # User documents (created)
│   └── vector_db/                 # FAISS index (created)
│
├── frontend/                      # React UI (original)
└── README.md
```

---

## 🛠️ Installation & Setup

### Prerequisites

- **Python 3.10+** - [Download](https://python.org/downloads/)
- **Ollama** - [Download](https://ollama.com) → Run `ollama pull llama3`

### Quick Start

1. **Clone or Download**
   ```bash
   git clone https://github.com/YOUR_USERNAME/Intelligent-Offline-RAG-Assistant.git
   cd Intelligent-Offline-RAG-Assistant/backend
   ```

2. **Setup Virtual Environment**
   ```bash
   python -m venv venv
   .\venv\Scripts\Activate.ps1  # Windows
   # source venv/bin/activate  # Linux/Mac
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Start Backend Server**
   ```bash
   python -m uvicorn main:app --reload
   ```
   - Server: `http://127.0.0.1:8000`
   - Health check: `http://127.0.0.1:8000/health/`

5. **(Optional) Start Web UI**
   ```bash
   streamlit run streamlit_app.py
   ```
   - UI: `http://localhost:8501`

---

## 📖 Usage

### API Endpoints

#### 1. Upload Document
```bash
curl -X POST "http://127.0.0.1:8000/upload/" \
  -F "file=@/path/to/your/document.pdf"
```

#### 2. Index Documents
```bash
curl -X POST "http://127.0.0.1:8000/index/"
```

#### 3. Query Documents
```bash
curl -X POST "http://127.0.0.1:8000/query/" \
  -H "Content-Type: application/json" \
  -d '{"text": "What are the key findings?"}'
```

**Response Example:**
```json
{
  "query": "What are the key findings?",
  "rewritten_query": "Please clarify and expand: What are the key findings?",
  "answer": "Based on the document, the key findings include...",
  "sources": ["document.pdf"],
  "evaluation": {
    "passed": true,
    "score": 0.85,
    "reason": "Good quality"
  }
}
```

---

## 🤖 Agent Details

### 1. Query Agent
- **Purpose**: Improves user queries for better retrieval
- **Features**: Adds question format, expands short queries, handles vague terms
- **Example**: "info" → "In a precise way, what information do you need?"

### 2. Retriever Agent
- **Purpose**: Efficient document retrieval using FAISS
- **Features**: Semantic search, top-k results, metadata tracking

### 3. Generator Agent
- **Purpose**: Answer generation using retrieved context
- **Features**: Grounded responses, hallucination prevention, Ollama integration

### 4. Evaluator Agent
- **Purpose**: Quality assurance and error correction
- **Features**: Hallucination detection, confidence scoring, automatic retry

---

## 🔧 Configuration

### Environment Variables
Create `.env` file in `backend/`:

```env
OLLAMA_MODEL=llama3
EMBEDDING_MODEL=all-MiniLM-L6-v2
CHUNK_SIZE=1000
CHUNK_OVERLAP=150
TOP_K_RESULTS=5
```

### Customization
- **Change LLM**: Edit `OLLAMA_MODEL` in `agents/generator_agent.py`
- **Change Embeddings**: Update `EMBEDDING_MODEL` in `utils/embeddings.py`
- **Add File Types**: Extend `utils/loader.py`

---

## 🧪 Testing

### Unit Tests
```bash
cd backend
python -m pytest tests/  # If you add test files
```

### Manual Testing
1. Upload a PDF
2. Index it
3. Ask questions
4. Check evaluation scores

---

## 🚀 Deployment

### Local Production
```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

### Docker (Optional)
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0"]
```

---

## 📊 Performance

- **Indexing**: ~1-2 min for 100-page PDF
- **Query Response**: ~5-10 seconds
- **Memory Usage**: ~2-4GB RAM
- **Storage**: Vector DB ~10% of document size

---

## 🤝 Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push: `git push origin feature/amazing-feature`
5. Open Pull Request

---

## 📄 License

MIT License - see [LICENSE](LICENSE) file

---

## 🙏 Acknowledgments

- **LangChain** for orchestration framework
- **Ollama** for offline LLM support
- **FAISS** for efficient vector search
- **Sentence Transformers** for embeddings

---

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/YOUR_USERNAME/Intelligent-Offline-RAG-Assistant/issues)
- **Discussions**: [GitHub Discussions](https://github.com/YOUR_USERNAME/Intelligent-Offline-RAG-Assistant/discussions)

---

**Built with ❤️ for privacy-conscious AI research**





