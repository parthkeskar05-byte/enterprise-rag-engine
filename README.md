# 📚 Enterprise Document Q&A Engine (Streamlit + FAISS)

A rapid-deployment Retrieval-Augmented Generation (RAG) application engineered to process, embed, and query PDF documents in real-time. Built with **Streamlit** for a seamless user interface and powered by **Meta's Llama 3.1** via **Groq** for ultra-low latency inference.

This system is designed for high-speed, ephemeral document analysis using in-memory vector storage, making it ideal for immediate, zero-setup document Q&A pipelines.

---

## 🏗️ System Architecture & Data Flow

1. **Dynamic Ingestion:** Unstructured PDF documents are uploaded via the Streamlit interface and securely processed through temporary local file handling.
2. **Deterministic Chunking:** Documents are parsed using a recursive character text splitter (1000-character chunks, 200-character overlap) to maintain paragraph-level semantic context.
3. **Ephemeral Vector Storage:** Utilizes **HuggingFace MiniLM** models to generate dense vector embeddings, which are instantly indexed in an in-memory **FAISS** vector database attached to the user's session state.
4. **High-Velocity Synthesis:** Queries are routed through a LangChain `RetrievalQA` chain to a **Groq-hosted Llama 3.1 (8B)** endpoint, delivering near-instantaneous synthesis of the retrieved context.

---

## 🛠️ Technology Stack

* **Language:** Python 3.11+
* **Frontend UI:** Streamlit
* **Orchestration Layer:** LangChain
* **LLM Inference:** Groq Cloud (Llama-3.1-8b-instant)
* **Embedding Model:** HuggingFace (`sentence-transformers/all-MiniLM-L6-v2`)
* **Vector Store:** FAISS (Facebook AI Similarity Search - CPU optimized)
* **Document Processing:** PyPDFLoader

---

## 🔥 Key Engineering Features

* **Session-State Caching:** Intelligently caches the FAISS vector database in the Streamlit session state, preventing expensive database rebuilds during sequential user queries.
* **Ultra-Low Latency Inference:** Swapped traditional LLM providers for Groq's LPU architecture, driving response times down to a fraction of standard API limits.
* **Ephemeral Processing:** Designed for secure, single-session analysis. Uploaded files are processed via the `tempfile` library and immediately purged from the local file system post-embedding.

---

## 🚀 Quick Start & Local Execution

### 1. Clone the Repository
```bash
git clone [https://github.com/parthkeskar05-byte/YOUR_REPO_NAME.git](https://github.com/parthkeskar05-byte/YOUR_REPO_NAME.git)
cd YOUR_REPO_NAME
```
2. Environment Configuration
Create a .env file in the root directory to store your Groq API key:

```bash
GROQ_API_KEY=gsk_your_api_key_here
```
3. Install Dependencies
Ensure you have an active virtual environment, then install the required packages:
```bash
pip install streamlit langchain-groq langchain-community langchain-text-splitters pypdf faiss-cpu sentence-transformers
```
4. Launch the Application
```Bash
streamlit run app.py
```
The web interface will automatically launch in your default browser at http://localhost:8501.
