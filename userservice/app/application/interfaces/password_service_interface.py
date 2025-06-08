"""Password service interface for application layer."""

from abc import ABC, abstractmethod


class PasswordServiceInterface(ABC):
    """Interface for password management operations."""
    
    @abstractmethod
    def hash_password(self, password: str) -> str:
        """Hash a plain text password."""
        pass
    
    @abstractmethod
    def verify_password(self, password: str, hashed_password: str) -> bool:
        """Verify a password against its hash."""
        pass
    
    @abstractmethod
    def generate_temporary_password(self) -> str:
        """Generate a temporary password."""
        pass
    
    @abstractmethod
    def validate_password_strength(self, password: str) -> bool:
        """Validate password meets security requirements."""
        pass
