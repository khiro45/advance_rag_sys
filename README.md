# Advanced RAG System — Core Architecture

> **Stack:** FastAPI · LangGraph · ChromaDB · Cross-Encoders · Gemini 2.0 Flash · sentence-transformers

---

## Table of Contents

1. [System Overview](#system-overview)
2. [The RAG Pipeline](#the-rag-pipeline)
3. [Component Breakdown](#component-breakdown)
4. [User Query Lifecycle](#user-query-lifecycle)
5. [Document Ingestion Lifecycle](#document-ingestion-lifecycle)
6. [Environment Configuration](#environment-configuration)
7. [Getting Started](#getting-started)

---

## System Overview

This system is an **Advanced Retrieval-Augmented Generation (RAG)** pipeline designed for high-precision document question-answering. Instead of a naive "embed -> retrieve -> generate" approach, it employs a multi-agent system built on **LangGraph** orchestrating query expansion, multi-vector retrieval, and cross-encoder reranking.

The entire pipeline is wrapped in a high-performance **FastAPI** application, ensuring it's ready to be integrated as a backend service.

---

## The RAG Pipeline

The classic, naive RAG pattern suffers from several fatal flaws: brittle retrieval algorithms, inability to handle complex queries, and hallucination when context is irrelevant. 

To solve this, our system introduces a state-of-the-art retrieval sequence:

1. **Sub-Query Expansion:** An agent intercepts the user query, analyzing it and generating multiple sub-queries to maximize lexical and semantic surface area.
2. **Multi-Vector Retrieval:** Each sub-query is vectorized and searched against the `ChromaDB` vector store independently, broadening the scope of retrieved documents.
3. **Cross-Encoder Reranking:** A secondary reranker scores the pooled retrieved documents against the original user query, sorting them by absolute relevance and culling irrelevant chunks.
4. **Agentic Generation:** A final reasoning agent consumes the highly-curated context and the original query to generate an accurate, grounded, and hallucination-free response.

---

## Component Breakdown

### 1. `RagOrchestrator` (`app/orchestrators/`)
The brain of the system. It glues the LangGraph agents and the Vector Store together. It orchestrates the 4-step pipeline: Expansion -> Retrieval -> Reranking -> Generation.

### 2. LangGraph Agents (`app/services/agentic/workflows/`)
Instead of fixed LangChain chains, the reasoning steps are distinct graphs:
- **`sub_queries_agent`:** Takes a complex user query and breaks it down into multiple specific sub-queries.
- **`question_response_agent`:** Takes the final reranked context and the user query to formulate the final answer.

### 3. Vector Store (`app/services/rag_sys/vector_store/`)
A robust wrapper around **ChromaDB**. 
- Embeds using configurable `sentence-transformers` (e.g. `all-MiniLM-L6-v2`).
- Handles data processing and chunking (`ProcessorFactory`).
- Implements `cross_encoder_reranking` to accurately score query-document pairs beyond simple cosine similarity.

### 4. API Layer (`app/api/v1/endpoints/rag.py`)
Clean FastAPI REST endpoints exposing:
- `POST /api/v1/rag/query`: For executing the full RAG pipeline.
- `POST /api/v1/rag/ingest`: For document ingestion and embedding.

---

## User Query Lifecycle

When a user submits a query via the `/query` endpoint, the following lifecycle occurs:

1. **Initial Request HTTP POST:** User sends `{"query": "How does the system handle concurrent connections?"}`.
2. **Agentic Expansion:** The `sub_queries_agent` expands this query into several sub-queries (e.g., *"system concurrent connections architecture"*, *"handling simultaneous requests"*, etc.).
3. **Parallel Retrieval:** The `VectorStore` fetches the top N chunks for *each* of those sub-queries from ChromaDB.
4. **Reranking:** The `VectorStore` runs the pooled chunks through a Cross-Encoder against the original user query. The most relevant chunks are selected, and those with a low confidence score are discarded.
5. **Contextual Assembly:** The final chunks are merged into a single system prompt context.
6. **Generation:** The `question_response_agent` (powered by the LLM) reads the curated context and constructs the final answer.
7. **Response:** The grounded answer is returned to the user via JSON.

---

## Document Ingestion Lifecycle

When adding new knowledge through the `/ingest` endpoint:

1. **Raw Text:** System receives an array of raw document strings and associated metadata.
2. **Chunking & Processing:** The `ProcessorFactory` cleans the text and splits it into optimal overlapping chunks.
3. **Embedding:** The chunks are passed through the local embedding model (`sentence-transformers`).
4. **Storage:** Vectors, raw text chunks, and metadata are persisted locally to the `ChromaDB` directory for durable semantic memory.

---

## Environment Configuration

Configure your `.env` file based on `.env.example`:

```env
# Vector Store
VS_VECTOR_DB_PATH=./vector_db
VS_COLLECTION_NAME=main_collection
VS_EMBEDDING_MODEL_NAME=all-MiniLM-L6-v2
VS_DEVICE=cpu

# Agent (Gemini)
AGENT_GEMINI_API_KEY=your-gemini-api-key-here
AGENT_MODEL_NAME=gemini-2.0-flash
AGENT_TEMPERATURE=0.7
```

---

## Getting Started

```bash
# 1. Clone and create a virtual environment
python -m venv venv
source venv/bin/activate          # Windows: .\venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure environment
cp .env.example .env
# Add your Gemini API key and other environment variables

# 4. Start the server
uvicorn app.main:app --reload

# 5. Explore the API
# Swagger UI:  http://127.0.0.1:8000/docs
# ReDoc:       http://127.0.0.1:8000/redoc
```
