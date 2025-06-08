#!/usr/bin/env python3
"""
Test de integración para verificar el flujo completo de autenticación.
"""

import asyncio
from fastapi.testclient import TestClient

from main import app
from tests.utils.test_helpers import AuthTestHelper

client = TestClient(app)

async def test_integration_flow():
    """Test de integración del flujo completo"""
    print("🚀 Iniciando test de integración...")
    
    # 1. Crear helper
    auth_helper = AuthTestHelper(client)
    print("✅ AuthTestHelper creado")
    
    # 2. Crear seed users
    auth_helper.create_seed_users()
    admin_data = auth_helper._seed_users["admin"]["data"]
    print(f"✅ Seed users creados. Admin email: {admin_data['email']}")
    
    # 3. Crear admin usando seeder
    success = await auth_helper.seed_admin_user()
    print(f"✅ Admin seeder result: {success}")
    
    # 4. Intentar login
    token = auth_helper.get_auth_token(admin_data["email"], admin_data["password"])
    print(f"✅ Token obtenido: {'SI' if token else 'NO'}")
    
    if token:
        print(f"Token: {token[:50]}...")
        
        # 5. Probar endpoint protegido
        headers = auth_helper.get_auth_headers(token)
        response = client.get("/users/", headers=headers)
        print(f"✅ GET /users/ status: {response.status_code}")
        
        if response.status_code == 200:
            users = response.json()
            print(f"✅ Usuarios encontrados: {len(users.get('users', []))}")
        else:
            print(f"❌ Error en GET /users/: {response.text}")
    else:
        print("❌ No se pudo obtener token")
        
        # Intentar ver qué hay en la base de datos
        try:
            response = client.get("/users/")
            print(f"GET /users/ sin auth: {response.status_code}")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(test_integration_flow())
