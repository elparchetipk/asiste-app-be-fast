"""User DTOs for application layer."""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from uuid import UUID

from ...domain import UserRole, DocumentType


@dataclass(frozen=True)
class CreateUserDTO:
    """DTO for creating a new user."""
    
    first_name: str
    last_name: str
    email: str
    document_number: str
    document_type: DocumentType
    password: str
    role: UserRole


@dataclass(frozen=True)
class UpdateUserDTO:
    """DTO for updating user information."""
    
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None


@dataclass(frozen=True)
class ChangePasswordDTO:
    """DTO for changing user password."""
    
    current_password: str
    new_password: str


@dataclass(frozen=True)
class UserResponseDTO:
    """DTO for user response data."""
    
    id: UUID
    first_name: str
    last_name: str
    email: str
    document_number: str
    document_type: str
    role: str
    is_active: bool
    must_change_password: bool
    created_at: datetime
    updated_at: datetime
    last_login_at: Optional[datetime]
    
    @property
    def full_name(self) -> str:
        """Get the full name of the user."""
        return f"{self.first_name} {self.last_name}"


@dataclass(frozen=True)
class LoginDTO:
    """DTO for user login."""
    
    email: str
    password: str


@dataclass(frozen=True)
class TokenResponseDTO:
    """DTO for authentication token response."""
    
    access_token: str
    token_type: str
    expires_in: int
    user: UserResponseDTO


@dataclass(frozen=True)
class UserListDTO:
    """DTO for paginated user list."""
    
    users: list[UserResponseDTO]
    total: int
    page: int
    page_size: int
    total_pages: int


@dataclass(frozen=True)
class UserFilterDTO:
    """DTO for user filtering parameters."""
    
    role: Optional[UserRole] = None
    is_active: Optional[bool] = None
    search_term: Optional[str] = None  # Search in name, email, document
    document_type: Optional[DocumentType] = None
