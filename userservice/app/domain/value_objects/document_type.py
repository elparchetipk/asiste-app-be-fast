"""Document type value object."""

from enum import Enum


class DocumentType(Enum):
    """Supported document types in Colombia."""
    
    CC = "CC"  # Cédula de Ciudadanía
    TI = "TI"  # Tarjeta de Identidad
    CE = "CE"  # Cédula de Extranjería
    PA = "PA"  # Pasaporte
