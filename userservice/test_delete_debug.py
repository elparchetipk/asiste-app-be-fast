#!/usr/bin/env python3
"""
Script para debuggear el test de delete user.
"""
import asyncio
from fastapi.testclient import TestClient
from main import app
from tests.utils.test_helpers import AuthTestHelper
import uuid
import random

async def test_delete_debug():
    """Debuggear el endpoint de delete."""
    print("🔧 Iniciando debug de delete...")
    
    client = TestClient(app)
    auth_helper = AuthTestHelper(client)
    
    # Crear admin user
    admin_created = await auth_helper.seed_admin_user()
    if not admin_created:
        print("❌ No se pudo crear admin")
        return
        
    admin_token = auth_helper.get_admin_token()
    admin_headers = {"Authorization": f"Bearer {admin_token}"}
    
    # Crear usuario de test
    unique_suffix = str(uuid.uuid4())[:8]
    random_doc_number = f"{random.randint(10000000, 99999999)}"
    test_user_data = {
        "first_name": "Test",
        "last_name": "User",
        "email": f"test.user.{unique_suffix}@example.com",
        "document_number": random_doc_number,
        "document_type": "CC",
        "password": "TestUser123!",
        "role": "apprentice"
    }
    
    # Crear el usuario
    create_response = client.post(
        "/api/v1/users/",
        json=test_user_data,
        headers=admin_headers
    )
    
    if create_response.status_code != 201:
        print(f"❌ Error creando usuario: {create_response.status_code}")
        print(f"Detail: {create_response.json()}")
        return
    
    user_id = create_response.json()["id"]
    print(f"✅ Usuario creado: {user_id}")
    
    # Probar delete
    delete_response = client.delete(
        f"/api/v1/admin/users/{user_id}",
        headers=admin_headers
    )
    
    print(f"📋 Delete response status: {delete_response.status_code}")
    print(f"📋 Delete response body: {delete_response.json()}")

if __name__ == "__main__":
    asyncio.run(test_delete_debug())
