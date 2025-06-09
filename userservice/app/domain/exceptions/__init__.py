"""Domain exceptions module."""

from .user_exceptions import (
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

__all__ = [
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
]
