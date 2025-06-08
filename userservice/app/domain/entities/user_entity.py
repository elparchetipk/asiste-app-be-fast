import uuid
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum

class UserRole(Enum):
    APPRENTICE = "apprentice"
    INSTRUCTOR = "instructor"
    ADMINISTRATIVE = "administrative"
    ADMIN = "admin"

@dataclass
class User:
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    first_name: str
    last_name: str
    email: str  # Consider creating an Email value object later
    document_number: str # Consider creating a DocumentNumber value object later
    hashed_password: str
    role: UserRole
    is_active: bool = True
    must_change_password: bool = True
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    last_login_at: datetime | None = None

    def __post_init__(self):
        if not self.first_name or not self.first_name.strip():
            raise ValueError("First name cannot be empty")
        if not self.last_name or not self.last_name.strip():
            raise ValueError("Last name cannot be empty")
        # Basic email validation, more robust validation for Email value object
        if "@" not in self.email or "." not in self.email.split("@")[-1]:
            raise ValueError("Invalid email format")
        if not self.document_number or not self.document_number.strip():
            raise ValueError("Document number cannot be empty")
        # Add more validation as needed, e.g. password complexity if not handled elsewhere

    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"

    def update_profile(self, first_name: str | None = None, last_name: str | None = None, email: str | None = None):
        if first_name:
            self.first_name = first_name
        if last_name:
            self.last_name = last_name
        if email:
            # Add email validation if changed
            if "@" not in email or "." not in email.split("@")[-1]:
                raise ValueError("Invalid email format for update")
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
        
    def record_login(self):
        self.last_login_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()
