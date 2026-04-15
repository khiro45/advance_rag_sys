# Advanced RAG System — Architecture Deep Dive

> **Stack:** FastAPI · LangGraph · ChromaDB · SQLAlchemy · Gemini 2.0 Flash · sentence-transformers

---

## Table of Contents

1. [The Old Architecture — Naive RAG](#the-old-architecture--naive-rag)
2. [Downsides of the Old Approach](#downsides-of-the-old-approach)
3. [The New Architecture — This System](#the-new-architecture--this-system)
4. [Component Breakdown](#component-breakdown)
5. [Why This Architecture is Production-Ready](#why-this-architecture-is-production-ready)
6. [Environment Configuration](#environment-configuration)
7. [Getting Started](#getting-started)

---

## The Old Architecture — Naive RAG

The classic, widely-seen RAG pattern looks like this:

```
User Query
    ↓
Embed Query  →  Vector Search  →  Top-K Chunks
                                       ↓
                               Stuff into Prompt
                                       ↓
                               LLM → Response
```

Concretely, most "advanced RAG" tutorials you'll find online are still doing this:

- A single script or Jupyter notebook containing everything
- A fixed chunk size (e.g. 1000 chars with 60-char overlap) applied blindly
- One embedding call, one vector search, done
- LangChain `.invoke()` used as a black box
- No user management, no auth, no persistence of conversations
- No retry logic, no observability
- Hard-coded API keys or `.env` files loaded carelessly
- Zero tests

This approach is fine for a demo. It is not fine for anything that will ever touch a real user.

---

## Downsides of the Old Approach

**1. No separation of concerns.** Everything lives in one file. The ingestion logic, the retrieval logic, and the generation logic are entangled. Changing one breaks the others.

**2. No user or session context.** Queries are stateless. The system cannot remember what the user asked 30 seconds ago. Every turn is cold.

**3. No auth or security layer.** Anyone who can reach the endpoint can query anything. There is no concept of ownership over documents or conversation history.

**4. Brittle retrieval.** Naive top-K cosine similarity has no fallback. If the query phrasing doesn't closely match chunk phrasing, retrieval silently fails and the LLM hallucinates.

**5. No agentic reasoning.** The LLM is called once and trusted blindly. There is no loop, no self-correction, no tool use, no ability to decide whether to retrieve more context.

**6. No persistent storage.** Vectors live in memory. Restart the server, lose everything. There is no relational layer for users, documents, or chat history.

**7. Untestable.** With no module boundaries, you cannot write unit tests or integration tests without mocking the entire world.

**8. Not deployable.** No WSGI/ASGI server config, no migration strategy, no environment management — just `python main.py`.

---

## The New Architecture — This System

This system replaces the monolith with a layered, service-oriented FastAPI application. Responsibilities are cleanly separated across modules. The agentic loop is managed by LangGraph. Persistence is handled by SQLAlchemy with Alembic migrations. Auth is JWT-based. The vector store is ChromaDB with a configurable local embedding model.

```
HTTP Request
     ↓
FastAPI Router  →  Auth Middleware (JWT)
     ↓
Service Layer
  ├── RAG Service ──────────────────────────────────────────────┐
  │     ↓                                                        │
  │   LangGraph Agent Loop                                       │
  │     ├── Query Analysis Node                                  │
  │     ├── Retrieval Node  →  ChromaDB Vector Store            │
  │     ├── Grading Node (relevance check)                      │
  │     ├── Generation Node  →  Gemini 2.0 Flash                │
  │     └── Self-Reflection Node (hallucination guard)          │
  │                                                              │
  ├── Document Service  →  Ingestion + Chunking + Embedding     │
  ├── User Service      →  SQLAlchemy ORM  →  SQLite/Postgres   │
  └── Auth Service      →  JWT + bcrypt                         │
                                                                 │
Response ←───────────────────────────────────────────────────────┘
```

---

## Component Breakdown

### 1. `app/main.py` — Application Entry Point

The FastAPI application factory. Registers all routers, mounts middleware (CORS, logging, exception handlers), and initialises the database on startup. Exposes `/docs` (Swagger) and `/redoc` automatically.

**Role:** Glue. Keeps bootstrap logic separate from business logic. Changing a router or adding middleware never touches service code.

---

### 2. `app/core/config.py` — Settings via Pydantic-Settings

All configuration is read from environment variables and validated at startup using `pydantic-settings`. This includes the database URL, JWT secret, ChromaDB path, embedding model name, Gemini API key, and agent parameters.

**Role:** Single source of truth for configuration. If a required variable is missing or malformed, the app refuses to start with a clear error — not a silent runtime failure at 3AM.

---

### 3. `app/core/security.py` — Auth Layer

JWT token creation and verification via `python-jose`. Password hashing via `passlib[bcrypt]`. Dependency-injected into any route that requires authentication using FastAPI's `Depends()` pattern.

**Role:** Ensures every protected endpoint verifies identity before any business logic runs. Stateless, scalable, and standards-compliant.

---

### 4. `app/db/` — Relational Persistence (SQLAlchemy + Alembic)

SQLAlchemy ORM models for users, documents, and conversation history. Alembic handles schema migrations, meaning the database can evolve without dropping and recreating tables.

**Role:** Durable state. Users persist between sessions. Document metadata is tracked relationally. Chat history is stored and queryable — enabling multi-turn conversation context.

---

### 5. `app/vector_store/` — ChromaDB Integration

A service wrapper around ChromaDB. Documents are chunked, embedded using `sentence-transformers` (`all-MiniLM-L6-v2` by default, configurable), and persisted to a local directory. The collection name and device (CPU/GPU) are configurable via environment.

**Role:** Semantic memory. Converts unstructured text into a searchable vector space. Persists across restarts (unlike in-memory FAISS). Swappable — the config keys are abstract enough to back-swap to Pinecone or Qdrant without touching application logic.

---

### 6. `app/agent/` — LangGraph Agentic Loop

This is the core differentiator. Instead of a single LangChain chain, retrieval and generation are managed as a stateful graph using LangGraph. The graph nodes are:

- **Query Analysis Node:** Classifies the query type and rewrites it for better retrieval precision.
- **Retrieval Node:** Hits ChromaDB for top-K semantically similar chunks.
- **Grading Node:** Scores each retrieved chunk for relevance. Irrelevant chunks are dropped before generation — preventing hallucination from garbage context.
- **Generation Node:** Sends the graded context + original query to Gemini 2.0 Flash.
- **Self-Reflection Node:** Evaluates the generated answer for grounding. If the answer is not supported by the retrieved context, the loop re-routes back to retrieval with a refined query.

`AGENT_MAX_ITERATIONS` caps the loop to prevent infinite cycles.

**Role:** Replaces the dumb one-shot retrieval+generation pipeline with a reasoning loop that self-corrects. The system knows when it doesn't know.

---

### 7. `app/routers/` — API Layer

Clean, versioned REST endpoints under `/api/v1/`. Each router (auth, documents, chat) maps HTTP semantics to service calls. No business logic lives here — routers are thin.

**Role:** Clean API contract. Versioned from day one, meaning breaking changes can be introduced under `/api/v2/` without disrupting existing clients.

---

### 8. `app/services/` — Business Logic Layer

The service layer orchestrates between the routers, the agent, the vector store, and the database. This is where multi-turn context is assembled — pulling prior turns from the DB and prepending them to the agent's state before each invocation.

**Role:** Decouples HTTP concerns from domain logic. Services are testable in isolation without spinning up a web server.

---

### 9. `tests/` — Test Suite

Pytest-based tests with `httpx` as the async test client. Service-level unit tests and router-level integration tests are separate. The test database is isolated from the production database.

**Role:** Confidence. You can refactor the agent loop without being afraid you've broken user login.

---

## Why This Architecture is Production-Ready

| Dimension | Naive RAG | This System |
|---|---|---|
| Auth | None | JWT + bcrypt |
| Configuration | Hard-coded / `.env` loaded manually | Pydantic-Settings with startup validation |
| Persistence | In-memory | SQLAlchemy ORM + Alembic migrations |
| Vector Store | Ephemeral (restarts = data loss) | ChromaDB persisted to disk |
| Retrieval | One-shot top-K | Graded, iterative, self-correcting loop |
| LLM Calls | Single invoke | LangGraph stateful agent with max iterations |
| Multi-turn | Not supported | Chat history stored relationally |
| Testing | None | Pytest + httpx test client |
| API Design | None / ad-hoc | Versioned REST under `/api/v1/` |
| Deployability | `python main.py` | `uvicorn app.main:app` with proper ASGI config |
| Schema Evolution | Drop and recreate | Alembic migration files |

The system is not just a RAG demo renamed to "advanced". It is a backend service that happens to have RAG capabilities — built with the same discipline you would apply to any production API.

---

## Environment Configuration

Copy `.env.example` to `.env` and fill in your values:

```env
# App
PROJECT_NAME="FastAPI Robust Starter"
API_V1_STR="/api/v1"

# Database
DATABASE_URL=sqlite:///./sql_app.db

# Security
SECRET_KEY=your-super-secret-key-here   # openssl rand -hex 32
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Vector Store
VS_VECTOR_DB_PATH=./vector_db
VS_COLLECTION_NAME=main_collection
VS_EMBEDDING_MODEL_NAME=all-MiniLM-L6-v2
VS_DEVICE=cpu

# Agent (Gemini)
AGENT_GEMINI_API_KEY=your-gemini-api-key-here
AGENT_MODEL_NAME=gemini-2.0-flash
AGENT_TEMPERATURE=0.7
AGENT_MAX_ITERATIONS=10
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
# Edit .env with your keys

# 4. Run database migrations
alembic upgrade head

# 5. Start the server
uvicorn app.main:app --reload

# 6. Explore the API
# Swagger UI:  http://127.0.0.1:8000/docs
# ReDoc:       http://127.0.0.1:8000/redoc
```

---

*Built with FastAPI · LangGraph · ChromaDB · SQLAlchemy · Gemini 2.0 Flash*
