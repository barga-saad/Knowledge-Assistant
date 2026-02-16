"""
Authentication endpoints
Handles JWT tokens, refresh, and Keycloak integration
"""

import logging
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import create_access_token, create_refresh_token, verify_token
from app.schemas import TokenResponse, RefreshTokenRequest

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/token", response_model=TokenResponse)
async def login(db: AsyncSession = Depends(get_db)):
    """
    Login endpoint - currently returns demo tokens.
    
    In production, this would:
    1. Validate credentials against Keycloak
    2. Sync user with our database
    3. Return JWT tokens
    
    For now, returns test tokens for development.
    """
    
    # TODO: Integrate with Keycloak
    # This is a placeholder for the full OAuth2 flow
    
    test_user_id = "test-user-123"
    
    access_token = create_access_token({"sub": test_user_id})
    refresh_token = create_refresh_token({"sub": test_user_id})
    
    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
    )


@router.post("/refresh", response_model=TokenResponse)
async def refresh_access_token(
    request: RefreshTokenRequest,
    db: AsyncSession = Depends(get_db),
):
    """
    Refresh access token using refresh token.
    
    Args:
        request: Contains refresh_token
    
    Returns:
        New access_token and refresh_token
    
    Raises:
        HTTPException: If refresh token is invalid
    """
    
    # Verify refresh token
    token_data = verify_token(request.refresh_token, token_type="refresh")
    
    if not token_data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
        )
    
    # Generate new tokens
    access_token = create_access_token({"sub": token_data.sub})
    refresh_token = create_refresh_token({"sub": token_data.sub})
    
    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
    )
