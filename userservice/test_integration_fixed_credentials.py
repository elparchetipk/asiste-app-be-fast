#!/usr/bin/env python3
"""
Test de integración con credenciales fijas para verificar el flujo completo de autenticación.
"""

import asyncio
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession

from main import app
from app.infrastructure.config.database import get_db_session
from app.infrastructure.seeders.admin_seeder import AdminSeeder

client = TestClient(app)

# Credenciales fijas para testing
FIXED_ADMIN_EMAIL = "test.admin@sicora.test.com"
FIXED_ADMIN_PASSWORD = "TestAdminPass123!"
FIXED_ADMIN_DOCUMENT = "1000000099"

async def test_integration_with_fixed_credentials():
    """Test de integración con credenciales fijas"""
    print("🚀 Iniciando test de integración con credenciales fijas...")
    
    # 1. Crear admin usando AdminSeeder con credenciales fijas
    print(f"📝 Credenciales fijas:")
    print(f"   Email: {FIXED_ADMIN_EMAIL}")
    print(f"   Password: {FIXED_ADMIN_PASSWORD}")
    print(f"   Document: {FIXED_ADMIN_DOCUMENT}")
    
    try:
        async for session in get_db_session():
            seeder = AdminSeeder(session)
            
            # Crear admin con force_recreate=True para asegurar credenciales correctas
            admin_user = await seeder.seed_test_admin(
                email=FIXED_ADMIN_EMAIL,
                password=FIXED_ADMIN_PASSWORD,
                first_name="Test",
                last_name="Admin",
                document_number=FIXED_ADMIN_DOCUMENT,
                force_recreate=True  # Forzar recreación para asegurar credenciales
            )
            
            if admin_user:
                print(f"✅ Admin creado/actualizado exitosamente")
            break
                
    except Exception as e:
        print(f"❌ Error al crear admin: {e}")
        return False
    
    # 2. Intentar login directo con endpoint de auth
    print("\n🔑 Probando login con credenciales fijas...")
    login_response = client.post("/auth/login", json={
        "email": FIXED_ADMIN_EMAIL,
        "password": FIXED_ADMIN_PASSWORD
    })
    
    print(f"Login status: {login_response.status_code}")
    
    if login_response.status_code != 200:
        print(f"❌ Login error: {login_response.text}")
        return False
    else:
        token_data = login_response.json()
        access_token = token_data.get('access_token')
        print(f"✅ Token obtenido: {access_token[:50]}...")
        
        # 3. Probar endpoint protegido
        headers = {"Authorization": f"Bearer {access_token}"}
        response = client.get("/users/", headers=headers)
        print(f"✅ GET /users/ status: {response.status_code}")
        
        if response.status_code == 200:
            users = response.json()
            users_list = users.get('users', [])
            print(f"✅ Usuarios encontrados: {len(users_list)}")
            
            # Mostrar información de usuarios
            for user in users_list:
                print(f"   - {user.get('first_name')} {user.get('last_name')} ({user.get('email')})")
        else:
            print(f"❌ Error en GET /users/: {response.text}")
            return False
    
    # 4. Probar creación de un nuevo usuario
    print("\n👤 Probando creación de nuevo usuario...")
    new_user_data = {
        "first_name": "Nuevo",
        "last_name": "Usuario",
        "email": "nuevo.usuario@test.com",
        "document_number": "12345678",
        "document_type": "CC",
        "password": "NuevoPass123!",
        "role": "APPRENTICE"
    }
    
    create_response = client.post("/users/", json=new_user_data, headers=headers)
    print(f"Creación de usuario status: {create_response.status_code}")
    
    if create_response.status_code == 201:
        created_user = create_response.json()
        print(f"✅ Usuario creado: {created_user.get('first_name')} {created_user.get('last_name')}")
        
        # 5. Probar login del nuevo usuario
        print("\n🔐 Probando login del nuevo usuario...")
        new_user_login = client.post("/auth/login", json={
            "email": new_user_data["email"],
            "password": new_user_data["password"]
        })
        
        if new_user_login.status_code == 200:
            print("✅ Login del nuevo usuario exitoso")
        else:
            print(f"❌ Error en login del nuevo usuario: {new_user_login.text}")
    else:
        print(f"❌ Error al crear usuario: {create_response.text}")
    
    print("\n🎉 Test de integración completado!")
    return True

if __name__ == "__main__":
    asyncio.run(test_integration_with_fixed_credentials())
