"""Email value object for user domain."""

import re
from dataclasses import dataclass
from typing import ClassVar

from ..exceptions import InvalidUserDataError


@dataclass(frozen=True)
class Email:
    """Email value object with validation."""
    
    value: str
    
    # Email regex pattern (RFC 5322 compliant)
    _EMAIL_PATTERN: ClassVar[str] = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    def __post_init__(self):
        """Validate email format after initialization."""
        if not self.value:
            raise InvalidUserDataError("email", "Email cannot be empty")
        
        if not isinstance(self.value, str):
            raise InvalidUserDataError("email", "Email must be a string")
        
        # Normalize email to lowercase
        object.__setattr__(self, 'value', self.value.lower().strip())
        
        if len(self.value) > 254:  # RFC 5321 limit
            raise InvalidUserDataError("email", "Email is too long (max 254 characters)")
        
        if not re.match(self._EMAIL_PATTERN, self.value):
            raise InvalidUserDataError("email", "Invalid email format")
    
    @property
    def domain(self) -> str:
        """Get the domain part of the email."""
        return self.value.split('@')[1]
    
    @property
    def local_part(self) -> str:
        """Get the local part of the email."""
        return self.value.split('@')[0]
    
    def __str__(self) -> str:
        """String representation of the email."""
        return self.value
