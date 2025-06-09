"""Domain repositories module."""

from .user_repository_interface import UserRepositoryInterface
from .refresh_token_repository_interface import RefreshTokenRepositoryInterface

__all__ = [
    "UserRepositoryInterface",
    "RefreshTokenRepositoryInterface",
]
