"""User role value object."""

from enum import Enum


class UserRole(Enum):
    """Enumeration of user roles in the system."""
    
    APPRENTICE = "apprentice"
    INSTRUCTOR = "instructor"
    ADMINISTRATIVE = "administrative"
    ADMIN = "admin"
