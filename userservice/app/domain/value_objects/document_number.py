"""Document number value object for user domain."""

import re
from dataclasses import dataclass
from enum import Enum
from typing import ClassVar

from .document_type import DocumentType
from ..exceptions import InvalidUserDataError


@dataclass(frozen=True)
class DocumentNumber:
    """Document number value object with validation."""
    
    value: str
    document_type: DocumentType
    
    # Validation patterns for Colombian documents
    _CC_PATTERN: ClassVar[str] = r'^\d{7,10}$'  # 7-10 digits
    _TI_PATTERN: ClassVar[str] = r'^\d{8,11}$'  # 8-11 digits
    _CE_PATTERN: ClassVar[str] = r'^[A-Z0-9]{6,15}$'  # Alphanumeric 6-15 chars
    _PA_PATTERN: ClassVar[str] = r'^[A-Z0-9]{6,12}$'  # Alphanumeric 6-12 chars
    
    def __post_init__(self):
        """Validate document number after initialization."""
        if not self.value:
            raise InvalidUserDataError("document_number", "Document number cannot be empty")
        
        if not isinstance(self.value, str):
            raise InvalidUserDataError("document_number", "Document number must be a string")
        
        # Normalize document number
        normalized_value = self.value.upper().strip()
        object.__setattr__(self, 'value', normalized_value)
        
        # Validate based on document type
        self._validate_document()
    
    def _validate_document(self) -> None:
        """Validate document number based on type."""
        patterns = {
            DocumentType.CC: self._CC_PATTERN,
            DocumentType.TI: self._TI_PATTERN,
            DocumentType.CE: self._CE_PATTERN,
            DocumentType.PA: self._PA_PATTERN,
        }
        
        pattern = patterns[self.document_type]
        if not re.match(pattern, self.value):
            raise InvalidUserDataError(
                "document_number",
                f"Invalid {self.document_type.value} format: {self.value}"
            )
    
    @property
    def full_document(self) -> str:
        """Get the full document representation."""
        return f"{self.document_type.value}-{self.value}"
    
    def __str__(self) -> str:
        """String representation of the document."""
        return self.full_document
