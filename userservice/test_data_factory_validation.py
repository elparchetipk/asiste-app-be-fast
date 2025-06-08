#!/usr/bin/env python3
"""
Test para validar que TestDataFactory genera datos válidos.
"""
import sys
import os
import re

# Agregar el directorio de la aplicación al path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from app.domain.value_objects.user_role import UserRole
from app.domain.value_objects.document_number import DocumentNumber, DocumentType
from app.domain.value_objects.email import Email
from app.infrastructure.adapters.bcrypt_password_service import BcryptPasswordService
from tests.utils.test_helpers import TestDataFactory


def test_user_data_validation():
    """Verificar que los datos generados por TestDataFactory son válidos."""
    print("🧪 Probando generación de datos válidos con TestDataFactory...")
    
    password_service = BcryptPasswordService()
    
    # Test con diferentes roles y prefijos
    test_cases = [
        (UserRole.APPRENTICE, "test"),
        (UserRole.INSTRUCTOR, "instructor"),
        (UserRole.ADMIN, "admin"),
        (UserRole.ADMINISTRATIVE, "staff")
    ]
    
    for role, prefix in test_cases:
        print(f"\n🔍 Testing role {role.value} con prefix '{prefix}':")
        
        # Generar datos de usuario
        user_data = TestDataFactory.create_user_data(role=role, prefix=prefix)
        
        # 1. Validar email
        try:
            email = Email(user_data["email"])
            print(f"   ✅ Email válido: {email.value}")
        except Exception as e:
            print(f"   ❌ Email inválido: {e}")
            return False
        
        # 2. Validar document_number
        try:
            document = DocumentNumber(user_data["document_number"], DocumentType.CC)
            print(f"   ✅ Documento válido: {document.value}")
        except Exception as e:
            print(f"   ❌ Documento inválido: {e}")
            return False
        
        # 3. Validar contraseña
        password = user_data["password"]
        is_valid = password_service.validate_password_strength(password)
        print(f"   ✅ Contraseña válida: {password} -> {is_valid}")
        
        if not is_valid:
            print(f"   ❌ Contraseña no cumple requisitos de seguridad")
            return False
        
        # 4. Verificar que el número de documento sea numérico para CC
        if not re.match(r'^\d{7,10}$', user_data["document_number"]):
            print(f"   ❌ Documento CC debe ser 7-10 dígitos: {user_data['document_number']}")
            return False
        
        print(f"   ✅ Todos los datos válidos para {role.value}")
    
    # Test de cambio de contraseña
    print(f"\n🔐 Testing datos de cambio de contraseña:")
    password_data = TestDataFactory.create_password_change_data()
    
    current_valid = password_service.validate_password_strength(password_data["current_password"])
    new_valid = password_service.validate_password_strength(password_data["new_password"])
    
    print(f"   Contraseña actual: {password_data['current_password']} -> válida: {current_valid}")
    print(f"   Contraseña nueva: {password_data['new_password']} -> válida: {new_valid}")
    
    if not current_valid or not new_valid:
        print(f"   ❌ Las contraseñas de cambio no son válidas")
        return False
    
    print(f"   ✅ Datos de cambio de contraseña válidos")
    
    print(f"\n✅ Todos los tests de validación de datos PASARON")
    return True


if __name__ == "__main__":
    success = test_user_data_validation()
    if success:
        print(f"\n🎉 TestDataFactory genera datos válidos!")
        sys.exit(0)
    else:
        print(f"\n💥 TestDataFactory genera datos inválidos - revisar implementación")
        sys.exit(1)
