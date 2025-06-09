#!/usr/bin/env python3

from tests.utils.test_helpers import TestDataFactory
from app.domain.value_objects.user_role import UserRole
import json

def test_password_generation():
    # Crear datos de usuario de test
    user_data = TestDataFactory.create_user_data(role=UserRole.APPRENTICE, prefix='testbase')
    print('Datos del usuario de test:')
    print(json.dumps(user_data, indent=2))

    # Verificar contraseña específicamente
    password = user_data['password']
    print(f'\nContraseña generada: {password}')
    print(f'Longitud: {len(password)}')
    print(f'Tiene mayúscula: {any(c.isupper() for c in password)}')
    print(f'Tiene minúscula: {any(c.islower() for c in password)}')
    print(f'Tiene dígito: {any(c.isdigit() for c in password)}')
    print(f'Tiene especial: {any(c in "!@#$%^&*()_+-=" for c in password)}')

if __name__ == "__main__":
    test_password_generation()
