# 📖 Technical Glossary & Concepts

A reference guide for technical terms used in this project.

---

## A

### Async/Await
Non-blocking code execution. While one request waits for database, the server handles other requests.

**Example:**
```python
async def get_users():
    users = await db.query()  # Doesn't block other requests
    return users
```

### API (Application Programming Interface)
Contract between frontend and backend. Defines endpoints, parameters, responses.

**Example:**
```
POST /api/v1/documents/upload
Request: {title, file}
Response: {id, status}
```

### Authentication
Verifying who you are (login). Uses JWT tokens.

### Authorization
Verifying what you're allowed to do (permissions). Uses roles (admin, user, viewer).

---

## B

### Backend
Server-side code. Handles database, business logic, authentication.

### Batch Processing
Processing many items at once. E.g., embedding all chunks of a document.

---

## C

### CORS (Cross-Origin Resource Sharing)
Browser security feature. Allows frontend on port 3000 to call backend on port 8000.

### Celery
Task queue for background jobs (TODO in Phase 2). E.g., process document uploads.

### Chunk
A piece of a document. Large documents split into ~512 token chunks for better search.

### Container
Isolated environment (Docker). Each service runs in its own container.

### CRUD
Create, Read, Update, Delete operations on data.

---

## D

### Database
Persistent data storage. PostgreSQL in our case.

### Docker
Containerization platform. Packages app with dependencies.

### Docker Compose
Orchestrates multiple containers. Defines services, networking, volumes.

---

## E

### Embedding
Vector representation of text. 1536 numbers representing semantic meaning.

**Example:**
```
"How do I authenticate?" → [0.12, 0.34, ..., 0.56]  // 1536 dims
```

### Endpoint
A specific URL that does something. E.g., `POST /api/v1/documents/upload`.

### Environment Variables
Configuration injected from outside code. Loaded from `.env` file.

---

## F

### FastAPI
Modern Python web framework. Async, automatic docs, data validation.

### Frontend
Client-side code (browser). React in our case.

### Function
Reusable block of code. Takes inputs, returns outputs.

---

## G

### GET Request
HTTP method to retrieve data. Idempotent (safe to call multiple times).

---

## H

### HTTP
Protocol for web communication. Methods: GET, POST, PUT, DELETE, etc.

### HTTPException
Error response from API. E.g., 401 Unauthorized, 404 Not Found.

---

## I

### IVFFlat
Index type for fast vector search in pgvector. Trade-off: speed vs. accuracy.

---

## J

### JWT (JSON Web Token)
Stateless authentication token. Contains encrypted user information.

**Structure:**
```
header.payload.signature
eyJhbGc...   .eyJzdWI...  .TpCndo...
```

---

## K

### Keycloak
Identity provider. Handles authentication, SSO, OAuth2.

### Kubernetes
Container orchestration for production (TODO - future phase).

---

## L

### LLM (Large Language Model)
AI model that understands and generates text. Llama2-7B in our case.

### Load Balancing
Distributing requests across multiple servers. Nginx does this.

---

## M

### Middleware
Code that runs before/after every request. CORS, logging, etc.

### Materialized View
Pre-computed database view. Fast for analytics queries.

---

## N

### Nginx
Reverse proxy & web server. Routes requests to backend services.

---

## O

### OAuth2
Authentication protocol. Used by Keycloak.

### ORM (Object-Relational Mapping)
Maps database tables to Python objects. SQLAlchemy in our case.

### Ollama
Tool to run LLMs locally. Serves Llama2-7B via HTTP API.

---

## P

### Pydantic
Data validation library. Validates request/response data.

### PostgreSQL
Relational database. Open-source, reliable, pgvector support.

### pgvector
PostgreSQL extension for vector operations. Enables semantic search.

### Prompt
Instructions given to LLM. E.g., "Answer this question based on context:".

---

## Q

### Query
Request to database. E.g., `SELECT * FROM documents WHERE user_id = 123`.

### RAG (Retrieval Augmented Generation)
AI technique: retrieve relevant documents → feed to LLM → generate answer.

**Flow:**
```
User Question
    ↓
Embed question
    ↓
Search vector DB for similar chunks
    ↓
Format as prompt with retrieved context
    ↓
Send to LLM
    ↓
Return answer with citations
```

### Redis
In-memory cache. Fast temporary storage (sessions, cache, etc.).

### REST (Representational State Transfer)
Architectural style for APIs. Uses HTTP methods (GET, POST, PUT, DELETE).

### Refresh Token
Long-lived token used to get new access tokens.

---

## S

### Schema
Structure of data. Defines tables (database schema) or request format (Pydantic schema).

### Semantic Search
Search by meaning, not keywords. Uses vector similarity.

**Example:**
```
Query: "How do I authenticate?"
Results: Documents about login, JWT, passwords
(Not just keyword matches)
```

### Service
Background process or API endpoint. Each Docker container is a service.

### SQLAlchemy
Python ORM library. Lets you write SQL-like code in Python.

### SSL/TLS
Encryption protocol for HTTPS. (TODO - production phase)

---

## T

### Token
Authentication credential. JWT in our case.

### Transaction
Atomic operation on database. Either all succeeds or all fails.

---

## U

### UUID
Unique identifier. 128-bit random string. Used for IDs.

---

## V

### Vector Space
Mathematical space where embeddings live. Vectors close together = similar meaning.

### Vite
Modern frontend build tool. Fast, minimal config.

---

## W

### WebSocket
Two-way communication protocol. Used for chat/real-time (TODO - Phase 4).

---

## Z

### Zero-Trust Security
Assume no request is trusted. Verify everything (auth, origin, etc.).

---

## Key Acronyms Quick Reference

| Acronym | Full | What |
|---------|------|------|
| API | Application Programming Interface | Contract between services |
| CORS | Cross-Origin Resource Sharing | Browser security |
| CRUD | Create Read Update Delete | Basic operations |
| JWT | JSON Web Token | Auth token |
| ORM | Object-Relational Mapping | Database abstraction |
| RAG | Retrieval Augmented Generation | AI with knowledge base |
| REST | Representational State Transfer | API style |
| SSO | Single Sign-On | One login for multiple services |
| TLS | Transport Layer Security | Encryption |

---

## Performance Concepts

### Latency
Time for single request. Goal: < 100ms for API calls.

### Throughput
Requests per second. Goal: 100+ req/s for small team.

### Indexing
Speed up queries. Database indexes are crucial:
- B-tree for text search
- IVFFlat for vector search

### Caching
Store results to avoid recomputation. Redis for sessions/cache.

### Connection Pooling
Reuse database connections. FastAPI does this automatically.

---

## Database Concepts

### ACID
- **Atomicity**: Transaction all-or-nothing
- **Consistency**: Data validity
- **Isolation**: Concurrent requests don't interfere
- **Durability**: Data survives crashes

### Foreign Key
Links records between tables. E.g., Document.owner_id → User.id

### Index
Speeds up queries. Trade-off: slower writes, faster reads.

### Materialized View
Pre-computed query result stored as table.

### Trigger
Code that runs on data change. E.g., auto-update `updated_at` timestamp.

---

## Security Concepts

### Authentication
"Who are you?" - Login with credentials

### Authorization
"What can you do?" - Permissions based on role

### Encryption
Scrambling data so only intended recipient can read it.

### Rate Limiting
Restrict requests per user/IP. Prevents abuse.

### SQL Injection
Attack inserting SQL into input. ORM prevents this.

### CSRF (Cross-Site Request Forgery)
Trick user into making unwanted request. CORS prevents this.

---

## AI/ML Concepts

### Embeddings
Numbers representing meaning. Found via neural networks.

### Fine-tuning
Adapting pre-trained model to specific task.

### Inference
Running model to generate outputs (not training).

### Model Parameters
Weights in neural network. Llama2-7B has 7 billion parameters.

### Similarity Score
How similar two embeddings are (0-1, usually cosine distance).

### Temperature
Controls randomness in LLM responses:
- Low (0.1): Deterministic
- High (0.9): Creative

---

## This is Getting Big! 📚

Bookmark this page. Come back when you see unfamiliar terms.

**Pro Tip:** As you work through phases 2-5, you'll naturally understand these concepts better.

Continue to Phase 2 when ready! 🚀
