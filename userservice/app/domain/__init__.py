"""Domain layer for user service."""

from .entities import User, UserRole
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
)
from .repositories import UserRepositoryInterface

__all__ = [
    # Entities
    "User",
    "UserRole",
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
    # Repositories
    "UserRepositoryInterface",
]
