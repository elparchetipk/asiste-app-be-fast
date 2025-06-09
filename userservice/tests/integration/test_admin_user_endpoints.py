"""
Tests for PASO 4: Admin user management endpoints.
"""

import pytest
from uuid import uuid4
from fastapi.testclient import TestClient
from httpx import AsyncClient

from main import app
from tests.utils.test_helpers import AuthTestHelper
from app.domain.value_objects.user_role import UserRole


class TestAdminUserEndpoints:
    """Test class for admin user management endpoints (PASO 4)."""
    
    @pytest.fixture(autouse=True)
    async def setup_test_environment(self, test_client: TestClient, db_tables_ready):
        """Set up test environment for each test."""
        self.client = test_client
        self.auth_helper = AuthTestHelper(test_client)
        
        # Create admin user and get token
        admin_created = await self.auth_helper.seed_admin_user()
        if not admin_created:
            pytest.fail("No se pudo crear usuario admin para tests")
            
        self.admin_token = self.auth_helper.get_admin_token()
        self.admin_headers = {"Authorization": f"Bearer {self.admin_token}"}
        
        # Create test user for admin operations
        import uuid
        import random
        unique_suffix = str(uuid.uuid4())[:8]
        random_doc_number = f"{random.randint(10000000, 99999999)}"
        self.test_user_data = {
            "first_name": "Test",
            "last_name": "User",
            "email": f"test.user.{unique_suffix}@example.com",
            "document_number": random_doc_number,
            "document_type": "CC",
            "password": "TestUser123!",
            "role": "apprentice"
        }
        
        # Create the test user
        response = self.client.post(
            "/api/v1/users/",
            json=self.test_user_data,
            headers=self.admin_headers
        )
        
        if response.status_code == 201:
            self.test_user_id = response.json()["id"]
        else:
            pytest.fail(f"Failed to create test user: {response.text}")
    
    def test_get_user_detail_success(self):
        """Test HU-BE-013: GET /api/v1/admin/users/{id} - Obtener usuario específico."""
        response = self.client.get(
            f"/api/v1/admin/users/{self.test_user_id}",
            headers=self.admin_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        
        # Verify response structure
        required_fields = [
            "id", "first_name", "last_name", "email", "document_number",
            "document_type", "role", "is_active", "must_change_password",
            "created_at", "updated_at", "links"
        ]
        for field in required_fields:
            assert field in data, f"Field {field} missing in response"
        
        # Verify HATEOAS links
        assert "links" in data
        assert "self" in data["links"]
        assert "update" in data["links"]
        assert "delete" in data["links"]
        
        # Verify user data
        assert data["email"] == self.test_user_data["email"]
        assert data["first_name"] == self.test_user_data["first_name"]
        assert data["role"] == self.test_user_data["role"]
    
    def test_get_user_detail_not_found(self):
        """Test get user detail with non-existent ID."""
        fake_id = str(uuid4())
        response = self.client.get(
            f"/api/v1/admin/users/{fake_id}",
            headers=self.admin_headers
        )
        
        assert response.status_code == 404
    
    def test_get_user_detail_unauthorized(self):
        """Test get user detail without admin token."""
        response = self.client.get(
            f"/api/v1/admin/users/{self.test_user_id}"
        )
        
        assert response.status_code == 403
    
    def test_update_user_success(self):
        """Test HU-BE-014: PUT /api/v1/admin/users/{id} - Actualizar usuario."""
        update_data = {
            "first_name": "Updated",
            "last_name": "Name",
            "role": "instructor",
            "is_active": True
        }
        
        response = self.client.put(
            f"/api/v1/admin/users/{self.test_user_id}",
            json=update_data,
            headers=self.admin_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        
        # Verify updates were applied
        assert data["first_name"] == update_data["first_name"]
        assert data["last_name"] == update_data["last_name"]
        assert data["role"] == update_data["role"]
        assert data["is_active"] == update_data["is_active"]
    
    def test_update_user_email_conflict(self):
        """Test update user with existing email."""
        # First create another user
        another_user_data = {
            "first_name": "Another",
            "last_name": "User",
            "email": "another.user@example.com",
            "document_number": "11111111",
            "document_type": "CC",
            "password": "AnotherUser123!",
            "role": "apprentice"
        }
        
        response = self.client.post(
            "/api/v1/users/",
            json=another_user_data,
            headers=self.admin_headers
        )
        
        if response.status_code == 201:
            # Try to update test user with existing email
            update_data = {"email": another_user_data["email"]}
            
            response = self.client.put(
                f"/api/v1/admin/users/{self.test_user_id}",
                json=update_data,
                headers=self.admin_headers
            )
            
            assert response.status_code == 400
            assert "already exists" in response.text
    
    def test_update_user_unauthorized(self):
        """Test update user without admin token."""
        update_data = {"first_name": "Unauthorized"}
        
        response = self.client.put(
            f"/api/v1/admin/users/{self.test_user_id}",
            json=update_data
        )
        
        assert response.status_code == 403
    
    def test_delete_user_success(self):
        """Test HU-BE-015: DELETE /api/v1/admin/users/{id} - Eliminar usuario."""
        response = self.client.delete(
            f"/api/v1/admin/users/{self.test_user_id}",
            headers=self.admin_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        
        # Verify response structure
        assert "message" in data
        assert "user_id" in data
        assert "deleted_at" in data
        
        # Verify user was soft deleted
        response = self.client.get(
            f"/api/v1/admin/users/{self.test_user_id}",
            headers=self.admin_headers
        )
        
        assert response.status_code == 200
        user_data = response.json()
        assert user_data["is_active"] is False
        assert user_data["deleted_at"] is not None
    
    def test_delete_user_self_prevention(self):
        """Test that admin cannot delete their own account."""
        # Get admin user ID from token
        admin_response = self.client.get(
            "/api/v1/auth/me",
            headers=self.admin_headers
        )
        admin_user_id = admin_response.json()["id"]
        
        response = self.client.delete(
            f"/api/v1/admin/users/{admin_user_id}",
            headers=self.admin_headers
        )
        
        assert response.status_code == 400
        assert "cannot delete their own account" in response.text
    
    def test_delete_user_unauthorized(self):
        """Test delete user without admin token."""
        response = self.client.delete(
            f"/api/v1/admin/users/{self.test_user_id}"
        )
        
        assert response.status_code == 403
    
    def test_bulk_upload_users_success(self):
        """Test HU-BE-016: POST /api/v1/admin/users/upload - Carga masiva CSV."""
        import base64
        import uuid
        
        # Create CSV content with unique emails
        suffix = str(uuid.uuid4())[:8]
        csv_content = f"""first_name,last_name,email,document_number,document_type,role,phone
Maria,Garcia,maria.garcia.{suffix}@example.com,22222{suffix[:3]},CC,instructor,+573001234567
Carlos,Lopez,carlos.lopez.{suffix}@example.com,33333{suffix[:3]},CC,apprentice,+573007654321"""
        
        # Encode to base64
        encoded_content = base64.b64encode(csv_content.encode('utf-8')).decode('utf-8')
        
        upload_data = {
            "file_content": encoded_content,
            "filename": "test_users.csv"
        }
        
        response = self.client.post(
            "/api/v1/admin/users/upload",
            json=upload_data,
            headers=self.admin_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        
        # Verify response structure
        assert "message" in data
        assert "total_processed" in data
        assert "successful" in data
        assert "failed" in data
        assert "created_users" in data
        
        # Verify users were created
        assert data["total_processed"] == 2
        assert data["successful"] == 2
        assert data["failed"] == 0
        assert len(data["created_users"]) == 2
    
    def test_bulk_upload_users_with_errors(self):
        """Test bulk upload with invalid data."""
        import base64
        import uuid
        
        # Create CSV with invalid data and unique document numbers
        suffix = str(uuid.uuid4())[:8]
        csv_content = f"""first_name,last_name,email,document_number,document_type,role
Valid,User,valid.user.{suffix}@example.com,44444{suffix[:3]},CC,apprentice
Invalid,Email,invalid-email,55555{suffix[:3]},CC,apprentice
Duplicate,Document,duplicate.user.{suffix}@example.com,44444{suffix[:3]},CC,instructor"""
        
        encoded_content = base64.b64encode(csv_content.encode('utf-8')).decode('utf-8')
        
        upload_data = {
            "file_content": encoded_content,
            "filename": "test_errors.csv"
        }
        
        response = self.client.post(
            "/api/v1/admin/users/upload",
            json=upload_data,
            headers=self.admin_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        
        # Verify some users were created and some failed
        assert data["total_processed"] == 3
        assert data["successful"] >= 1  # At least the valid user should be created
        assert data["failed"] >= 1  # At least one should fail
        assert len(data["errors"]) >= 1
    
    def test_bulk_upload_unauthorized(self):
        """Test bulk upload without admin token."""
        upload_data = {
            "file_content": "dGVzdA==",  # "test" in base64
            "filename": "test.csv"
        }
        
        response = self.client.post(
            "/api/v1/admin/users/upload",
            json=upload_data
        )
        
        assert response.status_code == 403


class TestAdminUserEndpointsIntegration:
    """Integration tests for admin user management workflow."""
    
    @pytest.fixture(autouse=True)
    async def setup_test_environment(self, test_client: TestClient, db_tables_ready):
        """Set up test environment for integration tests."""
        self.client = test_client
        self.auth_helper = AuthTestHelper(test_client)
        
        # Create admin user and get token
        admin_created = await self.auth_helper.seed_admin_user()
        if not admin_created:
            pytest.fail("No se pudo crear usuario admin para tests")
            
        self.admin_token = self.auth_helper.get_admin_token()
        self.admin_headers = {"Authorization": f"Bearer {self.admin_token}"}
    
    def test_complete_admin_user_workflow(self):
        """Test complete workflow: create -> get -> update -> delete."""
        # 1. Create user via bulk upload
        import base64
        import uuid
        import random
        
        unique_suffix = str(uuid.uuid4())[:8]
        random_doc_number = f"{random.randint(10000000, 99999999)}"
        csv_content = f"first_name,last_name,email,document_number,document_type,role\\nWorkflow,Test,workflow.test.{unique_suffix}@example.com,{random_doc_number},CC,apprentice"
        encoded_content = base64.b64encode(csv_content.encode('utf-8')).decode('utf-8')
        
        upload_response = self.client.post(
            "/api/v1/admin/users/upload",
            json={"file_content": encoded_content, "filename": "workflow.csv"},
            headers=self.admin_headers
        )
        
        assert upload_response.status_code == 200
        upload_data = upload_response.json()
        assert upload_data["successful"] == 1
        
        user_id = upload_data["created_users"][0]["id"]
        
        # 2. Get user detail
        get_response = self.client.get(
            f"/api/v1/admin/users/{user_id}",
            headers=self.admin_headers
        )
        
        assert get_response.status_code == 200
        user_data = get_response.json()
        assert f"workflow.test.{unique_suffix}@example.com" in user_data["email"]
        
        # 3. Update user
        update_response = self.client.put(
            f"/api/v1/admin/users/{user_id}",
            json={"role": "instructor", "first_name": "Updated"},
            headers=self.admin_headers
        )
        
        assert update_response.status_code == 200
        updated_data = update_response.json()
        assert updated_data["role"] == "instructor"
        assert updated_data["first_name"] == "Updated"
        
        # 4. Delete user
        delete_response = self.client.delete(
            f"/api/v1/admin/users/{user_id}",
            headers=self.admin_headers
        )
        
        assert delete_response.status_code == 200
        delete_data = delete_response.json()
        assert "successfully deactivated" in delete_data["message"]
        
        # 5. Verify user is soft deleted
        final_get_response = self.client.get(
            f"/api/v1/admin/users/{user_id}",
            headers=self.admin_headers
        )
        
        assert final_get_response.status_code == 200
        final_user_data = final_get_response.json()
        assert final_user_data["is_active"] is False
        assert final_user_data["deleted_at"] is not None
