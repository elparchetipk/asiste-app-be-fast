#!/usr/bin/env python3

import asyncio
from fastapi.testclient import TestClient
from main import app
from tests.utils.test_helpers import AuthTestHelper, TestDataFactory
from app.domain.value_objects.user_role import UserRole
from app.infrastructure.config.database import database_config

async def debug_create_user():
    """Debug específico para el test de crear usuario"""
    # Setup base de datos
    await database_config.create_tables()
    
    # Crear cliente de test
    client = TestClient(app)
    
    # Crear helper de autenticación
    auth_helper = AuthTestHelper(client)
    
    # Crear admin usando el seeder
    admin_created = await auth_helper.seed_admin_user()
    print(f"Admin creado: {admin_created}")
    
    # Crear datos de usuario para test
    user_data = TestDataFactory.create_user_data(
        role=UserRole.INSTRUCTOR,
        prefix="newuser"
    )
    
    print(f"Datos del usuario a crear:")
    print(f"  - Email: {user_data['email']}")
    print(f"  - Contraseña: {user_data['password']}")
    print(f"  - Documento: {user_data['document_number']}")
    print(f"  - Rol: {user_data['role']}")
    
    # Obtener headers de admin
    admin_headers = auth_helper.get_admin_headers()
    print(f"Admin headers: {admin_headers}")
    
    if not admin_headers:
        print("❌ No se pudieron obtener headers de admin")
        return
        
    # Intentar crear usuario
    response = client.post("/users/", json=user_data, headers=admin_headers)
    
    print(f"Respuesta del servidor:")
    print(f"  - Status code: {response.status_code}")
    print(f"  - Contenido: {response.text}")
    
    if response.status_code != 201:
        print("❌ Error al crear usuario")
        try:
            error_detail = response.json()
            print(f"  - Error JSON: {error_detail}")
        except:
            print(f"  - Error texto: {response.text}")
    else:
        print("✅ Usuario creado exitosamente")
        print(f"  - Datos: {response.json()}")

if __name__ == "__main__":
    asyncio.run(debug_create_user())
