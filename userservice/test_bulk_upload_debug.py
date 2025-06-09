#!/usr/bin/env python3
"""
Script para debuggear la carga masiva CSV.
"""
import asyncio
from fastapi.testclient import TestClient
from main import app
from tests.utils.test_helpers import AuthTestHelper
import base64

async def test_bulk_upload_debug():
    """Debuggear el endpoint de bulk upload."""
    print("🔧 Iniciando debug de bulk upload...")
    
    client = TestClient(app)
    auth_helper = AuthTestHelper(client)
    
    # Crear admin user
    admin_created = await auth_helper.seed_admin_user()
    if not admin_created:
        print("❌ No se pudo crear admin")
        return
        
    admin_token = auth_helper.get_admin_token()
    admin_headers = {"Authorization": f"Bearer {admin_token}"}
    
    # Crear CSV de test
    csv_content = """first_name,last_name,email,document_number,document_type,role,phone
Debug,User1,debug.user1@example.com,20000001,CC,apprentice,+573001111111
Debug,User2,debug.user2@example.com,20000002,CC,instructor,+573002222222"""
    
    print("📋 CSV Content:")
    print(csv_content)
    
    # Codificar a base64
    encoded_content = base64.b64encode(csv_content.encode('utf-8')).decode('utf-8')
    
    upload_data = {
        "file_content": encoded_content,
        "filename": "debug_users.csv"
    }
    
    # Probar upload
    upload_response = client.post(
        "/api/v1/admin/users/upload",
        json=upload_data,
        headers=admin_headers
    )
    
    print(f"📋 Upload response status: {upload_response.status_code}")
    print(f"📋 Upload response body: {upload_response.json()}")

if __name__ == "__main__":
    asyncio.run(test_bulk_upload_debug())
