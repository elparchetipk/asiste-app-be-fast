"""Value objects module for user domain."""

from .email import Email
from .document_number import DocumentNumber, DocumentType

__all__ = [
    "Email",
    "DocumentNumber", 
    "DocumentType",
]
