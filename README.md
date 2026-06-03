# Asynchronous Semantic RAG Engine for Financial Analytics

A high-velocity, production-ready Retrieval-Augmented Generation (RAG) pipeline engineered using **FastAPI** and **ChromaDB**. This system is specifically architected to handle low-latency ingestion, deterministic chunking, and context-isolated semantic querying of high-density financial text documents while strictly mitigating LLM hallucination.

---

## 🏗️ System Architecture & Data Flow

The architecture decouples the heavy computational ingestion pipeline from the user-facing retrieval interface to maintain low-latency response budgets:

1. **Ingestion Layer:** Asynchronous document ingestion pipelines parse raw unstructured financial text (PDFs, transcripts, reports).
2. **Processing Layer:** Employs a recursive character text splitter utilizing overlapping sliding windows (256-token chunk size, 32-token overlap) to preserve mathematical and temporal context boundaries.
3. **Vectorization Layer:** Generates high-density embeddings via localized embedding pipelines and indexes them natively inside a persistent **ChromaDB** vector database.
4. **Retrieval & Synthesis Layer:** Queries use a cosine-similarity distance metric blended with precise metadata filters. The resulting top-k relevant context blocks are injected into an isolated generation prompt layout sent to the generation endpoint.

---

## 🛠️ Technology Stack

* **Language Platform:** Python 3.11+
* **Web Framework:** FastAPI (Asynchronous REST API, Uvicorn worker management)
* **Vector Store:** ChromaDB (Native vector indexing & localized storage)
* **Orchestration Layer:** LangChain / Custom Python native execution engines
* **Data Processing:** Tokenizers, NumPy, Pandas

---

## 🔥 Key Production Features

* **True Asynchronous Ingestion:** Fully non-blocking API endpoints leveraging Python's `async/await` syntax to ingest large document sets without locking server worker threads.
* **Contextual Chunk Isolation:** Financial data contains highly dense information. Standard splitters corrupt context. This engine uses overlapping boundaries to ensure numbers remain tied to their specific financial metrics.
* **Deterministic Metadata Routing:** Every ingested document chunk automatically maps to user, date, and source metadata tags, enabling O(1) hard-filtering prior to semantic vector lookup.
* **Interactive API Schema:** Exposes structured validation models utilizing Pydantic v2 to guarantee clean inputs across all generation channels.

---

## 🗺️ API Endpoint Specification

### 1. Document Ingestion Pipeline
* **Endpoint:** `POST /api/v1/ingest`
* **Payload Type:** `multipart/form-data`
* **Description:** Asynchronously accepts raw documents, runs tokenized partitioning, computes embeddings, and updates the local ChromaDB index.

### 2. Semantic Context Query
* **Endpoint:** `POST /api/v1/query`
* **Payload Type:** `application/json`
* **Payload Structure:**
```json
  {
    "query": "What were the core revenue drivers for Q3?",
    "top_k": 4,
    "metadata_filter": {
      "fiscal_year": "2026"
    }
  }
```
Description: Executes semantic vector calculation with hard metadata restrictions to synthesize contextualized answers.
🚀 Installation & Local Execution
1. Initialize Repository Environment
```Bash
git clone [https://github.com/parthkeskar05-byte/rag-pipeline.git](https://github.com/parthkeskar05-byte/rag-pipeline.git)
cd rag-pipeline
```
2. Configure Local Settings
Create a production environment configuration file .env in the root project space:
```
Code snippet
OPENAI_API_KEY=sk-proj-...
CHROMADB_PERSIST_DIR=./data/chroma_db
HOST_PORT=8000
```
3. Build & Instantiate Service
```Bash
# Instantiate virtual dependency environment
python3 -m venv venv
source venv/bin/activate

# Install locked dependencies
pip install -r requirements.txt

# Launch high-concurrency server instance
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 2
```
Once running, navigate to http://localhost:8000/docs to interact natively with the automated Swagger UI engine.
