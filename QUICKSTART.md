# 🚀 QUICK START GUIDE

## 5-Minute Setup

### Step 1: Prepare Environment

```powershell
cd c:\Users\u482547\Desktop\Project

# Copy example env
copy .env.example .env

# Edit .env with your settings (optional for dev)
# Most defaults work out-of-box
```

### Step 2: Start Services

```powershell
# Start all containers
docker-compose up -d

# Check status
docker-compose ps
```

Expected output:
```
NAME                COMMAND             STATUS              PORTS
knowledge-db        postgres...         Up 30 seconds       5432/tcp
knowledge-redis     redis-server...     Up 20 seconds       6379/tcp
knowledge-ollama    ollama serve        Up 10 seconds       11434/tcp
knowledge-keycloak  start-dev           Up 5 seconds        8080/tcp
knowledge-backend   uvicorn app...      Up 2 seconds        8000/tcp
knowledge-ai-...    uvicorn app...      Up 1 second         8001/tcp
knowledge-nginx     nginx               Up 1 second         80/tcp
```

### Step 3: Pull LLM Model (First Time Only)

```powershell
# Download Llama2-7B model (~4GB, takes 2-5 minutes)
docker exec knowledge-ollama ollama pull llama2:7b

# Verify
curl http://localhost:11434/api/tags
# Should show llama2:7b in the output
```

### Step 4: Verify Everything Works

```powershell
# Backend health check
curl http://localhost:8000/api/v1/health

# Should return:
# {"status":"healthy","timestamp":"2026-02-16T..."}

# API documentation
start http://localhost:8000/docs
```

---

## 📊 Service URLs

| Service | URL | Use |
|---------|-----|-----|
| Backend API | http://localhost:8000 | REST API |
| API Docs (Swagger UI) | http://localhost:8000/docs | Test endpoints |
| Keycloak Admin | http://localhost:8080 | User management |
| Ollama Health | http://localhost:11434/api/tags | Check LLM |
| Redis | localhost:6379 | Cache (no web UI) |
| PostgreSQL | localhost:5432 | Database (use pgAdmin or CLI) |

---

## 🔑 Credentials

```
Keycloak Admin:
  Username: admin
  Password: admin_secure_password

PostgreSQL:
  User: khassistant
  Password: your_secure_password_here
  Database: knowledge_assistant

Redis:
  No authentication by default
```

---

## 🧪 Test the API

### 1. Get a Token

```powershell
curl -X POST http://localhost:8000/api/v1/auth/token
# Returns: {"access_token": "...", "refresh_token": "...", "token_type": "bearer"}
```

### 2. Use Token to Call API

```powershell
$token = "your_token_here"
$headers = @{"Authorization" = "Bearer $token"}

curl -Headers $headers http://localhost:8000/api/v1/documents
```

---

## 🐛 Troubleshooting

### Services won't start

```powershell
# Check Docker is running
docker ps

# See error logs
docker-compose logs backend
docker-compose logs postgres
docker-compose logs ollama
```

### Port already in use

```powershell
# Find what's using port 8000
netstat -ano | findstr :8000

# Or use different port in docker-compose.yml
```

### Out of memory

```powershell
# Increase Docker Desktop memory
# Settings → Resources → Memory: 8GB or higher
```

### Ollama model not loading

```powershell
# Check Ollama logs
docker-compose logs ollama

# Ensure model is downloaded
docker exec knowledge-ollama ollama list

# Download again if missing
docker exec knowledge-ollama ollama pull llama2:7b
```

---

## 📝 Common Commands

```powershell
# Start all services
docker-compose up -d

# Stop all services
docker-compose down

# View live logs
docker-compose logs -f backend

# View specific service logs (last 100 lines)
docker-compose logs --tail=100 backend

# Restart a service
docker-compose restart backend

# Rebuild backend image
docker-compose build backend

# Run one-off command in backend container
docker exec knowledge-backend bash

# Access database
docker exec -it knowledge-db psql -U khassistant -d knowledge_assistant

# Clean everything (removes volumes too!)
docker-compose down -v
```

---

## 🔄 Development Workflow

### Working on Backend

1. Edit files in `backend/`
2. FastAPI will auto-reload (because of `--reload` flag)
3. Check http://localhost:8000/docs for changes
4. View logs: `docker-compose logs -f backend`

### Working on AI Service

1. Edit files in `ai-service/`
2. Auto-reload enabled
3. Check http://localhost:8001/health

### Testing Database Changes

1. Edit `database/init.sql`
2. Remove database volume: `docker-compose down -v`
3. Start again: `docker-compose up -d`
4. Database will reinitialize

---

## 📚 Next Steps

Once everything is running:

1. **Read ARCHITECTURE.md** - Understand design decisions
2. **Explore API Docs** - Visit http://localhost:8000/docs
3. **Check Database** - Connect with pgAdmin or CLI
4. **Review Database Schema** - See what tables exist
5. **Continue to Phase 2** - Implement document upload

---

## ❓ Quick FAQ

**Q: Is my data persistent?**
A: Yes! Docker volumes preserve data even if containers restart.

**Q: How do I reset everything?**
A: `docker-compose down -v` (removes volumes, keeps images)

**Q: Can I use this on Mac/Linux?**
A: Yes! Just use `docker-compose` instead of PowerShell syntax.

**Q: How much disk space do I need?**
A: ~30GB (Ollama model is 4GB, rest is containers/volumes)

---

## 🎯 You're All Set!

Your enterprise knowledge assistant infrastructure is ready. 

Next: **Phase 2 - Backend Features** (document upload, embeddings, search)

Any issues? Check logs with `docker-compose logs -f` 👆
