"""JWT token service implementation."""

import os
from datetime import datetime, timedelta
from typing import Dict, Any, Set
from uuid import UUID

import jwt
from jwt.exceptions import InvalidTokenError, ExpiredSignatureError

from app.config import settings
from app.application.interfaces.token_service_interface import TokenServiceInterface
from app.domain.exceptions.user_exceptions import InvalidTokenError as DomainInvalidTokenError


class JWTTokenService(TokenServiceInterface):
    """JWT implementation of TokenServiceInterface."""
    
    def __init__(self):
        self._secret_key = settings.JWT_SECRET_KEY
        self._algorithm = settings.JWT_ALGORITHM
        self._access_token_expire_minutes = settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES
        self._refresh_token_expire_days = settings.JWT_REFRESH_TOKEN_EXPIRE_DAYS
        
        # In production, this should be stored in Redis or a database
        self._revoked_tokens: Set[str] = set()
    
    def create_access_token(self, user_id: UUID, role: str, expires_delta: int = None) -> str:
        """Create an access token for a user."""
        if expires_delta:
            expire = datetime.utcnow() + timedelta(minutes=expires_delta)
        else:
            expire = datetime.utcnow() + timedelta(minutes=self._access_token_expire_minutes)
        
        to_encode = {
            "sub": str(user_id),
            "role": role,
            "type": "access",
            "exp": expire,
            "iat": datetime.utcnow(),
        }
        
        encoded_jwt = jwt.encode(to_encode, self._secret_key, algorithm=self._algorithm)
        return encoded_jwt
    
    def create_refresh_token(self, user_id: UUID) -> str:
        """Create a refresh token for a user."""
        expire = datetime.utcnow() + timedelta(days=self._refresh_token_expire_days)
        
        to_encode = {
            "sub": str(user_id),
            "type": "refresh",
            "exp": expire,
            "iat": datetime.utcnow(),
        }
        
        encoded_jwt = jwt.encode(to_encode, self._secret_key, algorithm=self._algorithm)
        return encoded_jwt
    
    def decode_token(self, token: str) -> Dict[str, Any]:
        """Decode and validate a JWT token."""
        try:
            payload = jwt.decode(token, self._secret_key, algorithms=[self._algorithm])
            return payload
        except ExpiredSignatureError:
            raise InvalidTokenError("Token has expired")
        except InvalidTokenError as e:
            raise InvalidTokenError(f"Invalid token: {str(e)}")
    
    def is_token_valid(self, token: str) -> bool:
        """Check if a token is valid and not expired."""
        try:
            self.decode_token(token)
            return True
        except InvalidTokenError:
            return False
    
    def get_token_expiration(self, token: str) -> datetime:
        """Get the expiration date of a token."""
        payload = self.decode_token(token)
        exp_timestamp = payload.get("exp")
        if not exp_timestamp:
            raise InvalidTokenError("Token does not have expiration")
        
        return datetime.fromtimestamp(exp_timestamp)
    
    def revoke_token(self, token: str) -> None:
        """Revoke a token (add to blacklist)."""
        # In production, store this in Redis with expiration
        self._revoked_tokens.add(token)
    
    def is_token_revoked(self, token: str) -> bool:
        """Check if a token has been revoked."""
        return token in self._revoked_tokens
