import uuid
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum

from ..value_objects import Email, DocumentNumber, DocumentType
from ..value_objects.user_role import UserRole
from ..exceptions import InvalidUserDataError

@dataclass
class User:
    first_name: str
    last_name: str
    email: Email
    document_number: DocumentNumber
    hashed_password: str
    role: UserRole
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    is_active: bool = True
    must_change_password: bool = True
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    last_login_at: datetime | None = None
    deleted_at: datetime | None = None  # PASO 4: Soft delete support
    phone: str | None = None  # PASO 4: Additional user field
    # PASO 5: Password reset token support
    reset_password_token: str | None = None
    reset_password_token_expires_at: datetime | None = None

    def __post_init__(self):
        if not self.first_name or not self.first_name.strip():
            raise InvalidUserDataError("first_name", "First name cannot be empty")
        if not self.last_name or not self.last_name.strip():
            raise InvalidUserDataError("last_name", "Last name cannot be empty")
        
        # Ensure email and document_number are value objects
        if isinstance(self.email, str):
            object.__setattr__(self, 'email', Email(self.email))
        if isinstance(self.document_number, str):
            # For backward compatibility, assume CC if string is provided
            object.__setattr__(self, 'document_number', DocumentNumber(self.document_number, DocumentType.CC))

    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"

    def update_profile(self, first_name: str | None = None, last_name: str | None = None, email: Email | str | None = None):
        if first_name:
            if not first_name.strip():
                raise InvalidUserDataError("first_name", "First name cannot be empty")
            self.first_name = first_name
        if last_name:
            if not last_name.strip():
                raise InvalidUserDataError("last_name", "Last name cannot be empty")
            self.last_name = last_name
        if email:
            if isinstance(email, str):
                email = Email(email)
            self.email = email
        self.updated_at = datetime.utcnow()

    def change_password(self, new_hashed_password: str):
        self.hashed_password = new_hashed_password
        self.must_change_password = False
        self.updated_at = datetime.utcnow()

    def activate(self):
        self.is_active = True
        self.updated_at = datetime.utcnow()

    def deactivate(self):
        self.is_active = False
        self.updated_at = datetime.utcnow()
    
    def soft_delete(self):
        """Mark user as deleted (soft delete)."""
        self.is_active = False
        self.deleted_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()
        
    def record_login(self):
        self.last_login_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()
    
    # PASO 5: Password reset token methods
    def set_reset_password_token(self, token: str, expires_at: datetime):
        """Set password reset token and expiration."""
        self.reset_password_token = token
        self.reset_password_token_expires_at = expires_at
        self.updated_at = datetime.utcnow()
    
    def clear_reset_password_token(self):
        """Clear password reset token after use or expiration."""
        self.reset_password_token = None
        self.reset_password_token_expires_at = None
        self.updated_at = datetime.utcnow()
    
    def is_reset_token_valid(self, token: str) -> bool:
        """Check if the provided reset token is valid and not expired."""
        if not self.reset_password_token or not self.reset_password_token_expires_at:
            return False
        
        # Check token match and expiration
        return (
            self.reset_password_token == token and
            datetime.utcnow() < self.reset_password_token_expires_at
        )
    
    def force_change_password(self, new_hashed_password: str):
        """Force change password and update must_change_password flag."""
        self.hashed_password = new_hashed_password
        self.must_change_password = False
        self.updated_at = datetime.utcnow()
