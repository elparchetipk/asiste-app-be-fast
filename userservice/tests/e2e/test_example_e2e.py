import pytest
from httpx import AsyncClient

# This test assumes your FastAPI application is running
@pytest.mark.asyncio
async def test_example_e2e():
    async with AsyncClient(base_url="http://127.0.0.1:8000") as ac:
        response = await ac.get("/health") # Assuming you have a health check endpoint
    assert response.status_code == 200
    # assert response.json() == {"status": "ok"} # Or whatever your health check returns
