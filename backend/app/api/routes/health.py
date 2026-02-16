"""
Health check endpoints
"""

from fastapi import APIRouter
from datetime import datetime, timezone

router = APIRouter()


@router.get("/")
async def health_check():
    """
    Basic health check endpoint.
    Returns:
        - status: "healthy" if service is running
        - timestamp: Current server time (for clock synchronization)
    """
    return {
        "status": "healthy",
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
