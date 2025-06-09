#!/usr/bin/env python3
"""
Script para probar la autenticación del admin y los endpoints del PASO 4.
"""
import asyncio
from fastapi.testclient import TestClient
from main import app
from tests.utils.test_helpers import AuthTestHelper

async def test_admin_auth():
    """Probar la creación del admin y autenticación."""
    print("🔧 Iniciando test de autenticación de admin...")
    
    client = TestClient(app)
    auth_helper = AuthTestHelper(client)
    
    # Probar salud de la aplicación
    response = client.get("/health")
    print(f"✅ Health check: Status {response.status_code}")
    
    # Crear admin user
    print("\n🔧 Creando usuario admin...")
    admin_created = await auth_helper.seed_admin_user()
    
    if admin_created:
        print("✅ Admin creado exitosamente")
        
        # Obtener token
        admin_token = auth_helper.get_admin_token()
        if admin_token:
            print(f"✅ Token obtenido: {admin_token[:20]}...")
            
            # Probar endpoint de administración
            headers = {"Authorization": f"Bearer {admin_token}"}
            
            # Test GET /api/v1/admin/users/{id} - usando un ID no existente para verificar el endpoint
            response = client.get("/api/v1/admin/users/550e8400-e29b-41d4-a716-446655440000", headers=headers)
            print(f"✅ Test GET admin/users/id: Status {response.status_code}")
            
            # Test POST /api/v1/admin/users/upload
            csv_content = "first_name,last_name,email,document_number,document_type,role\nTest,User,test.admin@example.com,12345678,CC,APPRENTICE"
            import base64
            encoded_content = base64.b64encode(csv_content.encode('utf-8')).decode('utf-8')
            
            upload_data = {
                "file_content": encoded_content,
                "filename": "test_users.csv"
            }
            response = client.post("/api/v1/admin/users/upload", json=upload_data, headers=headers)
            print(f"✅ Test POST admin/users/upload: Status {response.status_code}")
            
            if response.status_code != 200:
                print(f"   Detail: {response.json()}")
            
        else:
            print("❌ No se pudo obtener token")
    else:
        print("❌ No se pudo crear admin")

if __name__ == "__main__":
    asyncio.run(test_admin_auth())
