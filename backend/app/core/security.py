"""
JWT token generation and validation
Handles access and refresh tokens
"""

from datetime import datetime, timedelta, timezone
from typing import Optional
import logging

from jose import JWTError, jwt
from pydantic import BaseModel

from app.core.config import settings

logger = logging.getLogger(__name__)


class TokenData(BaseModel):
    """Data stored in JWT token"""
    sub: str  # Subject (user ID)
    exp: int  # Expiration time
    iat: int  # Issued at
    type: str  # "access" or "refresh"


class TokenResponse(BaseModel):
    """Token response model"""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Create a JWT access token.
    
    Args:
        data: Claims to encode in token (typically {"sub": user_id})
        expires_delta: Optional expiration time delta
    
    Returns:
        Encoded JWT token
    """
    to_encode = data.copy()
    
    # Set expiration time
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    
    to_encode.update({
        "exp": int(expire.timestamp()),
        "iat": int(datetime.now(timezone.utc).timestamp()),
        "type": "access"
    })
    
    # Encode with secret key
    encoded_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )
    
    return encoded_jwt


def create_refresh_token(data: dict) -> str:
    """
    Create a JWT refresh token.
    Refresh tokens have longer expiration and are used to obtain new access tokens.
    """
    to_encode = data.copy()
    
    expire = datetime.now(timezone.utc) + timedelta(
        days=settings.REFRESH_TOKEN_EXPIRE_DAYS
    )
    
    to_encode.update({
        "exp": int(expire.timestamp()),
        "iat": int(datetime.now(timezone.utc).timestamp()),
        "type": "refresh"
    })
    
    encoded_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )
    
    return encoded_jwt


def verify_token(token: str, token_type: str = "access") -> Optional[TokenData]:
    """
    Verify and decode a JWT token.
    
    Args:
        token: JWT token to verify
        token_type: Expected token type ("access" or "refresh")
    
    Returns:
        TokenData if valid, None if invalid
    
    Raises:
        JWTError: If token is invalid
    """
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        
        # Validate token type
        if payload.get("type") != token_type:
            logger.warning(f"Token type mismatch: expected {token_type}, got {payload.get('type')}")
            return None
        
        return TokenData(**payload)
    
    except JWTError as e:
        logger.warning(f"Token verification failed: {str(e)}")
        return None
