"""
Main FastAPI application entry point
"""

import logging
import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware

from app.core.config import settings
from app.core.database import Base, engine
from app.api.routes import health, auth, documents, search

# Configure logging
logging.basicConfig(level=settings.LOG_LEVEL)
logger = logging.getLogger(__name__)


# ========================
# Lifespan event handlers
# ========================

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application startup and shutdown events.
    
    Startup: Initialize database tables with retry logic
    Shutdown: Clean up resources
    """
    # Startup - with retry logic for database connection
    logger.info("🚀 Application starting up...")
    max_retries = 5
    retry_delay = 2  # seconds
    
    for attempt in range(max_retries):
        try:
            async with engine.begin() as conn:
                # Create all tables if they don't exist
                await conn.run_sync(Base.metadata.create_all)
            logger.info("✅ Database initialized successfully")
            break
        except Exception as e:
            if attempt < max_retries - 1:
                logger.warning(f"⚠️  Database connection attempt {attempt + 1}/{max_retries} failed: {str(e)}")
                logger.info(f"⏳ Retrying in {retry_delay} seconds...")
                await asyncio.sleep(retry_delay)
            else:
                logger.error(f"❌ Failed to connect to database after {max_retries} attempts")
                logger.error(f"Error: {str(e)}")
                # Continue anyway - database might be initializing
                logger.info("⚠️  Starting application without database connection (will retry on requests)")
    
    yield
    
    # Shutdown
    logger.info("🛑 Application shutting down...")
    await engine.dispose()
    logger.info("✅ Cleanup completed")


# ========================
# FastAPI app initialization
# ========================

app = FastAPI(
    title="Knowledge Assistant API",
    description="AI-powered enterprise knowledge Q&A platform",
    version="1.0.0",
    lifespan=lifespan,
)


# ========================
# Middleware configuration
# ========================

# CORS middleware - allow frontend to call backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # Local frontend
        "http://localhost",       # Nginx
    ] if settings.BACKEND_ENV == "development" else ["https://yourdomain.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Trusted host middleware - prevent host header attacks
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["localhost", "127.0.0.1"] if settings.BACKEND_ENV == "development" else ["yourdomain.com"],
)


# ========================
# Routes registration
# ========================

# Health check
app.include_router(health.router, prefix="/api/v1/health", tags=["health"])

# Authentication
app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])

# Document management
app.include_router(documents.router, prefix="/api/v1/documents", tags=["documents"])

# Search
app.include_router(search.router, prefix="/api/v1/search", tags=["search"])


# ========================
# Root endpoint
# ========================

@app.get("/")
async def root():
    """Root endpoint - API info"""
    return {
        "name": "Knowledge Assistant API",
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs",
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
