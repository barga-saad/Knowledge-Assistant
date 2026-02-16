# 📁 Complete Project File Tree

## Overview

```
Project/
│
├── 📄 README.md                    # Main documentation
├── 📄 QUICKSTART.md                # 5-minute setup guide
├── 📄 ARCHITECTURE.md              # Design decisions deep dive
├── 📄 GLOSSARY.md                  # Technical terms reference
├── 📄 PHASE1_SUMMARY.md            # This phase summary
├── 📄 .gitignore                   # Git configuration
├── 📄 .env.example                 # Environment template (NEVER commit .env!)
├── 📄 docker-compose.yml           # Full stack orchestration
│
├── 📂 backend/                     # Python FastAPI application
│   ├── 📄 Dockerfile               # Backend container definition
│   ├── 📄 requirements.txt          # Python dependencies
│   │
│   └── 📂 app/                     # Main application package
│       ├── 📄 __init__.py          # Package marker
│       ├── 📄 main.py              # FastAPI app entry point
│       │
│       ├── 📂 core/                # Core utilities
│       │   ├── 📄 __init__.py
│       │   ├── 📄 config.py        # Settings from .env
│       │   ├── 📄 database.py      # SQLAlchemy async setup
│       │   └── 📄 security.py      # JWT token generation
│       │
│       ├── 📂 models/              # SQLAlchemy ORM models
│       │   └── 📄 __init__.py      # User, Document, Chunk, etc.
│       │
│       ├── 📂 schemas/             # Pydantic request/response models
│       │   └── 📄 __init__.py      # Input/output validation schemas
│       │
│       ├── 📂 services/            # Business logic layer (TODO Phase 2+)
│       │   └── 📄 __init__.py      # DocumentService, SearchService, etc.
│       │
│       └── 📂 api/                 # REST API endpoints
│           ├── 📄 __init__.py
│           └── 📂 routes/          # Endpoint modules
│               ├── 📄 __init__.py
│               ├── 📄 health.py    # GET /health
│               ├── 📄 auth.py      # POST /auth/token, /auth/refresh
│               ├── 📄 documents.py # Document CRUD endpoints
│               └── 📄 search.py    # Search & RAG endpoints
│
├── 📂 ai-service/                  # Local LLM service (Ollama wrapper)
│   ├── 📄 Dockerfile               # AI service container
│   ├── 📄 requirements.txt          # Python dependencies
│   │
│   └── 📂 app/                     # FastAPI wrapper
│       ├── 📄 __init__.py
│       └── 📄 main.py              # /embed, /generate endpoints
│
├── 📂 frontend/                    # React application (TODO Phase 3)
│   ├── 📄 package.json             # Node dependencies (TODO)
│   ├── 📄 vite.config.ts           # Build config (TODO)
│   │
│   ├── 📂 src/                     # Source code (TODO)
│   │   ├── 📄 main.tsx
│   │   ├── 📄 App.tsx
│   │   └── 📂 components/
│   │
│   ├── 📂 public/                  # Static assets (TODO)
│   └── 📂 dist/                    # Built output (TODO)
│
├── 📂 database/                    # Database schema & migrations
│   ├── 📄 init.sql                 # PostgreSQL initialization script
│   │                               # (Users, Documents, Chunks, etc.)
│   │
│   └── 📂 migrations/              # Alembic migrations (TODO Phase 2+)
│       └── (migrations will be here after changes)
│
├── 📂 docker/                      # Docker configuration files
│   ├── 📄 nginx.conf               # Nginx reverse proxy config
│   ├── 📄 keycloak-realm.json      # Keycloak realm definition
│   │
│   └── 📂 certs/                   # HTTPS certificates (TODO production)
│       └── (SSL certs go here)
│
└── 📂 tests/                       # Testing (TODO Phase 2+)
    ├── 📂 unit/
    │   └── test_*.py               # Unit tests
    └── 📂 integration/
        └── test_*.py               # Integration tests
```

---

## File Descriptions

### Root Files

| File | Purpose | Must Read |
|------|---------|-----------|
| `README.md` | Project overview & setup | ✅ Yes |
| `QUICKSTART.md` | 5-minute getting started | ✅ Yes |
| `ARCHITECTURE.md` | Design decisions explained | ✅ Important |
| `GLOSSARY.md` | Technical terms reference | 📖 Reference |
| `PHASE1_SUMMARY.md` | This phase recap | ✅ Yes |
| `.env.example` | Configuration template | ✅ Copy to `.env` |
| `docker-compose.yml` | Service orchestration | ⚙️ Don't modify yet |
| `.gitignore` | Git configuration | 🔒 Protects secrets |

### Backend: Core Layer

| File | Purpose |
|------|---------|
| `app/main.py` | FastAPI app initialization, middleware, routes |
| `app/core/config.py` | Settings from `.env` |
| `app/core/database.py` | PostgreSQL connection, async sessions |
| `app/core/security.py` | JWT token generation & verification |

### Backend: Database Layer

| File | Purpose |
|------|---------|
| `app/models/__init__.py` | SQLAlchemy ORM models (User, Document, etc.) |
| `app/schemas/__init__.py` | Pydantic validation schemas |
| `database/init.sql` | PostgreSQL initialization (tables, indexes) |

### Backend: API Layer

| File | Purpose |
|------|---------|
| `app/api/routes/health.py` | Health check endpoint |
| `app/api/routes/auth.py` | Authentication endpoints |
| `app/api/routes/documents.py` | Document management endpoints |
| `app/api/routes/search.py` | Search & RAG endpoints |

### Backend: Support

| File | Purpose |
|------|---------|
| `backend/Dockerfile` | Docker image for backend |
| `backend/requirements.txt` | Python dependencies |

### AI Service

| File | Purpose |
|------|---------|
| `ai-service/app/main.py` | FastAPI wrapper for Ollama |
| `ai-service/Dockerfile` | Docker image for AI service |
| `ai-service/requirements.txt` | Python dependencies |

### Docker Configuration

| File | Purpose |
|------|---------|
| `docker-compose.yml` | Orchestrates all 7 services |
| `docker/nginx.conf` | Routes requests to backend/keycloak |
| `docker/keycloak-realm.json` | Keycloak SSO configuration |

---

## Typical Development Workflow

### 1. Starting Development
```powershell
cd Project
cp .env.example .env
docker-compose up -d
```

### 2. Edit Backend Code
- Edit files in `backend/app/`
- FastAPI auto-reloads (check `--reload` in docker-compose)
- View changes at http://localhost:8000/docs

### 3. View Database
- Use `database/init.sql` to understand schema
- Query via SQL: `docker exec knowledge-db psql -U khassistant ...`

### 4. Test Endpoints
- Visit http://localhost:8000/docs (Swagger UI)
- Click "Try it out" on any endpoint
- Or use curl/Postman

### 5. Check Logs
```powershell
docker-compose logs -f backend    # See backend logs
docker-compose logs -f ai-service # See AI service logs
```

### 6. Debug Issues
- Read error messages in logs
- Check `.env` configuration
- Verify containers running: `docker-compose ps`

---

## Key Files to Understand First

### Must Read (In Order)
1. 📄 `README.md` - Start here
2. 📄 `QUICKSTART.md` - Get it running
3. 📄 `backend/app/main.py` - Entry point
4. 📄 `backend/app/core/config.py` - Settings
5. 📄 `backend/app/core/database.py` - Database

### Should Understand
6. 📄 `backend/app/models/__init__.py` - Data structure
7. 📄 `backend/app/schemas/__init__.py` - Request/Response format
8. 📄 `backend/app/api/routes/health.py` - Simple endpoint
9. 📄 `docker-compose.yml` - How services connect
10. 📄 `database/init.sql` - Database tables

### Reference as Needed
- 📄 `ARCHITECTURE.md` - Design explanations
- 📄 `GLOSSARY.md` - Technical terms
- 📄 `docker/nginx.conf` - Reverse proxy
- 📄 `docker/keycloak-realm.json` - SSO config

---

## Where to Add Code (Phase 2+)

| Task | Where | File(s) |
|------|-------|---------|
| Add new endpoint | `backend/app/api/routes/` | New `.py` or existing |
| Add business logic | `backend/app/services/` | `document_service.py`, etc. |
| Add database model | `backend/app/models/__init__.py` | Add new class |
| Add validation schema | `backend/app/schemas/__init__.py` | Add new Pydantic model |
| Modify database | `database/` | Create migration |
| Add frontend page | `frontend/src/` | New component |
| Add tests | `backend/tests/` | Test files |

---

## Quick Navigation

### Want to understand...

**Authentication?**
- ➡️ `backend/app/core/security.py`
- ➡️ `backend/app/api/routes/auth.py`

**Database?**
- ➡️ `database/init.sql`
- ➡️ `backend/app/models/__init__.py`
- ➡️ `backend/app/core/database.py`

**API endpoints?**
- ➡️ `backend/app/main.py` (registration)
- ➡️ `backend/app/api/routes/*.py` (implementation)
- ➡️ http://localhost:8000/docs (live docs)

**Docker setup?**
- ➡️ `docker-compose.yml` (orchestration)
- ➡️ Each `Dockerfile` (container definition)

**Keycloak?**
- ➡️ `docker/keycloak-realm.json` (config)
- ➡️ http://localhost:8080 (admin console)

**Configuration?**
- ➡️ `.env.example` (template)
- ➡️ `backend/app/core/config.py` (loading)

---

## Statistics

| Category | Count | Status |
|----------|-------|--------|
| Python files | 12 | ✅ Complete |
| Configuration files | 5 | ✅ Complete |
| Documentation | 5 | ✅ Complete |
| SQL files | 1 | ✅ Complete |
| Docker files | 2 | ✅ Complete |
| **Total** | **25+** | **✅ Phase 1 Done** |

---

## Next: Populate These (Phase 2+)

```
backend/app/services/        # Business logic layer
backend/tests/               # Unit & integration tests
frontend/src/                # React components
database/migrations/         # Database schema changes
docker/certs/                # HTTPS certificates (production)
```

---

## Pro Tips 💡

1. **Use `grep` to find things:**
   ```powershell
   grep -r "def get_documents" backend/
   grep -r "Document" backend/app/models/
   ```

2. **VS Code shortcuts:**
   - Ctrl+Shift+F: Find in all files
   - Ctrl+P: Quick file open
   - Ctrl+`: Toggle terminal

3. **File naming conventions:**
   - `app/services/document_service.py` ✅ (business logic)
   - `app/api/routes/documents.py` ✅ (endpoints)
   - `test_documents.py` ✅ (tests)

4. **Before modifying existing files:**
   - Understand what's there first
   - Run existing tests
   - Make small changes
   - Run tests again

---

That's your complete file map! Bookmark this for reference. 📚

**Next: Read [QUICKSTART.md](QUICKSTART.md) to get services running!**
