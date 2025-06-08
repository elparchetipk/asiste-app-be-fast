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
    print(f"   Admin password: {admin_data['password']}")
    print(f"   Admin document: {admin_data['document_number']}")
    
    # 3. Crear admin usando seeder
    success = await auth_helper.seed_admin_user()
    print(f"✅ Admin seeder result: {success}")
    
    # 4. Intentar login directo con endpoint de auth
    print("\n🔑 Probando login...")
    login_response = client.post("/auth/login", json={
        "email": admin_data["email"],
        "password": admin_data["password"]
    })
    print(f"Login status: {login_response.status_code}")
    if login_response.status_code != 200:
        print(f"Login error: {login_response.text}")
    else:
        token_data = login_response.json()
        print(f"Token obtenido: {token_data.get('access_token', 'N/A')[:50]}...")
        
        # 5. Probar endpoint protegido
        headers = {"Authorization": f"Bearer {token_data['access_token']}"}
        response = client.get("/users/", headers=headers)
        print(f"✅ GET /users/ status: {response.status_code}")
        
        if response.status_code == 200:
            users = response.json()
            print(f"✅ Usuarios encontrados: {len(users.get('users', []))}")
        else:
            print(f"❌ Error en GET /users/: {response.text}")
    
    # 6. Probar método helper
    token = auth_helper.get_auth_token(admin_data["email"], admin_data["password"])
    print(f"\n🔧 Helper token: {'SI' if token else 'NO'}")

if __name__ == "__main__":
    asyncio.run(test_integration_flow())
