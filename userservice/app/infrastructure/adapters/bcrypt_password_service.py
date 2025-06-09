"""Bcrypt password service implementation."""

import secrets
import string
import re
from passlib.context import CryptContext

from ...application.interfaces import PasswordServiceInterface


class BcryptPasswordService(PasswordServiceInterface):
    """Bcrypt implementation of PasswordServiceInterface."""
    
    def __init__(self):
        self._pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        self._min_length = 8
        self._min_uppercase = 1
        self._min_lowercase = 1
        self._min_digits = 1
        self._min_special_chars = 1
    
    def hash_password(self, password: str) -> str:
        """Hash a plain text password using bcrypt."""
        return self._pwd_context.hash(password)
    
    def verify_password(self, password: str, hashed_password: str) -> bool:
        """Verify a password against its hash."""
        return self._pwd_context.verify(password, hashed_password)
    
    def generate_temporary_password(self) -> str:
        """Generate a secure temporary password."""
        # Ensure at least one character from each required category
        password_parts = [
            secrets.choice(string.ascii_uppercase),  # At least one uppercase
            secrets.choice(string.ascii_lowercase),  # At least one lowercase
            secrets.choice(string.digits),           # At least one digit
            secrets.choice("!@#$%^&*"),             # At least one special char
        ]
        
        # Fill the rest with random characters
        all_chars = string.ascii_letters + string.digits + "!@#$%^&*"
        for _ in range(self._min_length - len(password_parts)):
            password_parts.append(secrets.choice(all_chars))
        
        # Shuffle the password to avoid predictable patterns
        secrets.SystemRandom().shuffle(password_parts)
        
        return ''.join(password_parts)
    
    def validate_password_strength(self, password: str) -> bool:
        """Validate password meets security requirements."""
        if not password or len(password) < self._min_length:
            return False
        
        # Check for minimum uppercase letters
        if len(re.findall(r'[A-Z]', password)) < self._min_uppercase:
            return False
        
        # Check for minimum lowercase letters
        if len(re.findall(r'[a-z]', password)) < self._min_lowercase:
            return False
        
        # Check for minimum digits
        if len(re.findall(r'\d', password)) < self._min_digits:
            return False
        
        # Check for minimum special characters
        if len(re.findall(r'[!@#$%^&*()_+\-=\[\]{};\':"\\|,.<>\/?]', password)) < self._min_special_chars:
            return False
        
        # Check for common weak patterns
        weak_patterns = [
            r'(.)\1{2,}',        # Three or more repeated characters
            r'123456',           # Sequential numbers
            r'abcdef',           # Sequential letters
            r'qwerty',           # Common keyboard patterns
            r'^password\d*$',    # Starts with "password" optionally followed by digits
            r'^admin\d*$',       # Starts with "admin" optionally followed by digits
            r'^user\d*$',        # Starts with "user" optionally followed by digits
            r'^test\d*$',        # Starts with "test" optionally followed by digits
            r'^\d+$',            # Only digits
        ]
        
        password_lower = password.lower()
        for pattern in weak_patterns:
            if re.search(pattern, password_lower):
                return False
        
        return True
