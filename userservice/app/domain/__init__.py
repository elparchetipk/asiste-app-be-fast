"""Domain layer for user service."""

from .entities import User, UserRole, RefreshToken
from .value_objects import Email, DocumentNumber, DocumentType
from .exceptions import (
    UserDomainException,
    UserNotFoundError,
    UserAlreadyExistsError,
    InvalidUserDataError,
    UserInactiveError,
    InvalidPasswordError,
    AuthenticationError,
    AuthorizationError,
    UserSessionError,
    InvalidTokenError,
    WeakPasswordError,
)
from .repositories import UserRepositoryInterface, RefreshTokenRepositoryInterface

__all__ = [
    # Entities
    "User",
    "UserRole",
    "RefreshToken",
    # Value Objects
    "Email",
    "DocumentNumber",
    "DocumentType",
    # Exceptions
    "UserDomainException",
    "UserNotFoundError",
    "UserAlreadyExistsError",
    "InvalidUserDataError",
    "UserInactiveError",
    "InvalidPasswordError",
    "AuthenticationError",
    "AuthorizationError",
    "UserSessionError",
    "InvalidTokenError",
    "WeakPasswordError",
    # Repositories
    "UserRepositoryInterface",
    "RefreshTokenRepositoryInterface",
]
