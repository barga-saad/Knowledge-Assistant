# 🧠 Knowledge Assistant - AI-Powered Enterprise Q&A Platform

> A production-ready full-stack application demonstrating modern software engineering practices with AI integration.

## 📋 Table of Contents
- [Architecture Overview](#architecture-overview)
- [Tech Stack](#tech-stack)
- [Quick Start](#quick-start)
- [Project Structure](#project-structure)
- [Phase 1: Foundation](#phase-1-foundation)
- [Development Guide](#development-guide)

---

## 🏗️ Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    FRONTEND (React + Vite)                   │
│  Chat UI • Document Upload • Admin Dashboard               │
└─────────────────────────┬───────────────────────────────────┘
                          │
            ┌─────────────┴──────────────┐
            │   NGINX (Reverse Proxy)    │
            └─────────────┬──────────────┘
                          │
        ┌─────────────────┼─────────────────┐
        │                 │                 │
    ┌───▼────────┐  ┌────▼────────┐  ┌───▼──────┐
    │  Backend   │  │  AI Service │  │ Keycloak │
    │  (FastAPI) │  │  (Ollama)   │  │  (OAuth2)│
    └───┬────────┘  └────┬────────┘  └──────────┘
        │                │
    ┌───▼─────────────────▼────────────┐
    │     PostgreSQL + pgvector        │
    │  (Data, Embeddings, Analytics)   │
    └─────────────────────────────────┘
```

### Key Design Decisions

1. **pgvector for Semantic Search**: No separate vector DB needed
2. **Async FastAPI**: Handles concurrent requests efficiently
3. **Local Llama2-7B**: Privacy + cost-effective
4. **Keycloak SSO**: Enterprise-ready authentication
5. **Docker Compose**: One-command deployment

---

## 🛠️ Tech Stack

| Component | Technology | Why |
|-----------|-----------|-----|
| Backend | FastAPI (Python 3.11) | Async, modern, great for AI |
| Frontend | React 18 + Vite | Type-safe (if using TS), fast |
| Database | PostgreSQL 16 | Reliable, pgvector support |
| Vector DB | pgvector (in PG) | Simpler than separate DB |
| Auth | Keycloak + JWT | Enterprise SSO + OAuth2 |
| LLM | Ollama (Llama2-7B) | Local, private, no API costs |
| Cache | Redis | Sessions, rate limiting |
| DevOps | Docker Compose | Local dev ≈ production |

---

## 🚀 Quick Start

### Prerequisites
- Docker & Docker Compose
- Python 3.11+ (for local development)
- Node.js 18+ (for frontend)
- 8GB RAM minimum (for Ollama)

### 1️⃣ Clone & Setup

```bash
cd c:\Users\u482547\Desktop\Project

# Copy environment template
copy .env.example .env

# Update .env with your values (especially SECRET_KEY)
```

### 2️⃣ Start Services

```bash
# Start all services (PostgreSQL, Redis, Keycloak, Backend, AI, Nginx)
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f backend
```

### 3️⃣ Access Services

| Service | URL | Credentials |
|---------|-----|-------------|
| Backend API | `http://localhost:8000` | - |
| API Docs | `http://localhost:8000/docs` | - |
| Keycloak | `http://localhost:8080` | admin / admin_secure_password |
| Frontend | `http://localhost:3000` | (not yet built) |

### 4️⃣ Initialize LLM

```bash
# Pull Llama2-7B model (first run only, ~4GB)
docker exec knowledge-ollama ollama pull llama2:7b

# Verify it's running
curl http://localhost:11434/api/tags
```

---

## 📁 Project Structure

```
Project/
├── backend/                    # FastAPI application
│   ├── app/
│   │   ├── api/
│   │   │   ├── routes/        # API endpoints
│   │   │   │   ├── health.py
│   │   │   │   ├── auth.py
│   │   │   │   ├── documents.py
│   │   │   │   └── search.py
│   │   ├── core/
│   │   │   ├── config.py      # Settings from .env
│   │   │   ├── database.py    # SQLAlchemy setup
│   │   │   └── security.py    # JWT tokens
│   │   ├── models/            # SQLAlchemy ORM models
│   │   ├── schemas/           # Pydantic request/response models
│   │   ├── services/          # Business logic (TODO)
│   │   └── main.py            # FastAPI app entry point
│   ├── tests/                 # Unit & integration tests (TODO)
│   ├── Dockerfile
│   └── requirements.txt
│
├── ai-service/                # Ollama wrapper service
│   ├── app/
│   │   └── main.py           # FastAPI wrapper for Ollama
│   ├── Dockerfile
│   └── requirements.txt
│
├── frontend/                  # React + Vite (TODO)
│   ├── src/
│   ├── public/
│   └── package.json
│
├── database/
│   ├── init.sql              # PostgreSQL schema with pgvector
│   └── migrations/           # Alembic migrations (TODO)
│
├── docker/
│   ├── nginx.conf            # Reverse proxy configuration
│   ├── keycloak-realm.json   # Keycloak realm definition
│   └── certs/                # HTTPS certificates (TODO)
│
├── docker-compose.yml        # Orchestration
├── .env.example             # Environment template
└── README.md                # This file
```

---

## 🔨 Phase 1: Foundation (Current)

### ✅ Completed

1. **Project Structure**
   - Clean, scalable folder layout
   - Separation of concerns

2. **Docker Compose Setup**
   - PostgreSQL + pgvector
   - Redis cache
   - Keycloak (SSO)
   - Ollama (LLM)
   - Backend API
   - AI Service
   - Nginx reverse proxy

3. **Database Schema**
   - Users (Keycloak-synced)
   - Documents & chunks with embeddings
   - Search history & analytics
   - Audit logs
   - Conversation sessions
   - Materialized views

4. **Backend Skeleton**
   - FastAPI application structure
   - Database layer (async SQLAlchemy)
   - JWT security utilities
   - Pydantic schemas (validated I/O)
   - ORM models
   - Health, auth, document, search routes (stubs)

5. **Environment Management**
   - `.env.example` template
   - Type-safe settings with Pydantic
   - Secrets management

6. **AI Service Skeleton**
   - FastAPI wrapper for Ollama
   - Embed and generate endpoints (stubs)

### 📋 Next Steps (Phase 2)

1. **Backend Functionality** → Implement endpoints
2. **Document Processing** → PDF/TXT parsing
3. **Embeddings** → Connect to Ollama
4. **Semantic Search** → pgvector queries
5. **Keycloak Integration** → Real authentication
6. **Frontend** → React chat UI

---

## 💻 Development Guide

### Backend Development

#### Running Locally (without Docker)

```bash
# 1. Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows

# 2. Install dependencies
pip install -r backend/requirements.txt

# 3. Set environment variables
$env:POSTGRES_HOST = "localhost"
$env:POSTGRES_USER = "khassistant"
# ... etc

# 4. Run backend
cd backend
uvicorn app.main:app --reload
```

#### Key Files to Know

- `app/core/config.py` - Read this first to understand settings
- `app/core/database.py` - How database connections work
- `app/core/security.py` - JWT token generation/verification
- `app/models/__init__.py` - Database table definitions
- `app/schemas/__init__.py` - Request/response validation
- `app/api/routes/` - REST endpoints

#### Common Tasks

**Add a new endpoint:**
```python
# backend/app/api/routes/documents.py
@router.post("/new-feature")
async def new_feature(
    request: SomeSchema,
    db: AsyncSession = Depends(get_db),
):
    """Endpoint documentation"""
    # Implementation
    return response
```

**Query the database:**
```python
from sqlalchemy import select
from app.models import User

# In an async function:
stmt = select(User).where(User.email == "user@example.com")
result = await db.execute(stmt)
user = result.scalar_one_or_none()
```

**Create a database migration:**
```bash
# After modifying models, create migration
alembic revision --autogenerate -m "Add new column"
alembic upgrade head
```

### Frontend Development (Soon)

Will cover in Phase 3 with:
- React hooks setup
- API integration
- Chat UI
- Authentication flow

### Testing

```bash
# Run backend tests (once implemented)
pytest backend/tests -v

# With coverage
pytest backend/tests --cov=app --cov-report=html
```

---

## 🔐 Security Checklist

- [x] Database credentials in `.env`
- [x] JWT token generation
- [ ] Keycloak integration
- [ ] HTTPS/TLS (nginx)
- [ ] Rate limiting (Redis)
- [ ] Input validation (Pydantic)
- [ ] SQL injection prevention (ORM)
- [ ] CORS configured
- [ ] Audit logging
- [ ] Password hashing

---

## 📊 Understanding the Database

### Key Tables

**users**
- Synced from Keycloak
- Role-based access (admin, user, viewer)

**documents**
- Files uploaded by users
- Status tracking (pending → processing → completed)
- Metadata (page count, etc.)

**document_chunks**
- Split documents into chunks (~512 tokens each)
- **embedding**: Vector for semantic search (1536 dimensions)
- Indexed with pgvector for fast similarity search

**search_queries**
- Every search is logged
- User feedback (thumbs up/down)
- Analytics (response time, satisfaction)

**conversation_sessions & conversation_messages**
- Multi-turn chat support
- Store conversation history

**audit_logs**
- Every important action logged
- Who, what, when, where, status

### Vector Search Example

```sql
-- Find documents most similar to a query embedding
SELECT 
    chunk_id,
    content,
    embedding <-> query_embedding AS similarity
FROM document_chunks
ORDER BY similarity
LIMIT 5;
```

The `<->` operator computes cosine distance (lower = more similar).

---

## 🚢 Deployment (Future)

Production checklist:
- [ ] Remove debug mode
- [ ] Setup HTTPS certs
- [ ] Configure real database credentials
- [ ] Setup monitoring & logging (ELK stack)
- [ ] Rate limiting & DDoS protection
- [ ] Backup strategy
- [ ] CI/CD pipeline (GitHub Actions)
- [ ] Kubernetes manifests (if scaling)

---

## 📚 Resources

- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [SQLAlchemy 2.0](https://docs.sqlalchemy.org/en/20/)
- [pgvector Docs](https://github.com/pgvector/pgvector)
- [Keycloak Documentation](https://www.keycloak.org/documentation.html)
- [Ollama GitHub](https://github.com/ollama/ollama)
- [Docker Compose](https://docs.docker.com/compose/)

---

## ❓ FAQ

**Q: Why not use OpenAI API?**
A: Local LLM means privacy (data never leaves your server), no API costs, full control, enterprise-friendly.

**Q: Why pgvector instead of separate vector DB?**
A: Simpler deployment, transaction consistency, easier access control, one database to manage.

**Q: How do I scale this?**
A: Start simple. When ready: Redis caching, database read replicas, multi-worker backend, load balancing.

**Q: Can I use a different LLM?**
A: Yes! Ollama supports many models. Just change `OLLAMA_MODEL` in `.env`.

---

## 📝 License

This project is for educational purposes. Use as you like!

---

## 🎯 Next: Phase 2 - Backend Implementation

Ready to implement the actual features? Next steps:
1. Document upload & PDF parsing
2. Embedding generation (Ollama)
3. Semantic search with pgvector
4. RAG pipeline with LLM
5. Keycloak integration for real auth

Let me know what you'd like to tackle next! 🚀
