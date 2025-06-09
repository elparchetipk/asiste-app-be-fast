#!/usr/bin/env python3
"""
Test para validar que los usuarios seed tienen contraseñas válidas.
"""
import sys
import os

# Agregar el directorio de la aplicación al path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from app.infrastructure.adapters.bcrypt_password_service import BcryptPasswordService
from tests.utils.test_helpers import AuthTestHelper


def test_seed_users_validation():
    """Verificar que los usuarios seed tienen contraseñas válidas."""
    print("🧪 Probando validación de contraseñas de usuarios seed...")
    
    password_service = BcryptPasswordService()
    
    # Crear un AuthTestHelper ficticio para solo validar las contraseñas
    auth_helper = AuthTestHelper(client=None)  # Solo para crear seed users
    
    # Crear usuarios seed
    seed_users = auth_helper.create_seed_users()
    
    for role, user_info in seed_users.items():
        print(f"\n🔍 Testing seed user '{role}':")
        
        password = user_info["password"]
        data_password = user_info["data"]["password"]
        
        # Verificar que las contraseñas son iguales
        if password != data_password:
            print(f"   ❌ Contraseñas no coinciden: '{password}' vs '{data_password}'")
            return False
        
        # Verificar fortaleza de contraseña
        is_valid = password_service.validate_password_strength(password)
        print(f"   Contraseña: {password}")
        print(f"   ✅ Contraseña válida: {is_valid}")
        
        if not is_valid:
            print(f"   ❌ Contraseña no cumple requisitos de seguridad")
            return False
    
    print(f"\n✅ Todos los usuarios seed tienen contraseñas válidas")
    return True


if __name__ == "__main__":
    success = test_seed_users_validation()
    if success:
        print(f"\n🎉 Usuarios seed tienen contraseñas válidas!")
        sys.exit(0)
    else:
        print(f"\n💥 Usuarios seed tienen contraseñas inválidas - revisar implementación")
        sys.exit(1)
