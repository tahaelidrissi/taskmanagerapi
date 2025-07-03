import pytest
import httpx
import pytest_asyncio
import os

BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000") 

@pytest.mark.asyncio
async def test_health():
    async with httpx.AsyncClient(follow_redirects=True) as client:
        r = await client.get(f"{BASE_URL}/health")
        assert r.status_code == 200
        assert r.json() == {"status": "OK"}

@pytest_asyncio.fixture(scope="module")
async def created_task_id():
    task_data = {
        "title": "Test Task",
        "description": "This is a test",
        "priority": 1,
        "due_date": "2025-12-31T23:59:59",
        "completed": False
    }
    async with httpx.AsyncClient(follow_redirects=True) as client:
        r = await client.post(f"{BASE_URL}/api/v1/tasks", json=task_data)
        assert r.status_code in (200, 201)
        task = r.json()
        yield task["_id"]
        assert task["title"] == "Test Task"
        assert task["description"] == "This is a test"
        assert task["priority"] == 1
        assert task["due_date"] == "2025-12-31T23:59:59"
        assert task["completed"] == False


@pytest.mark.asyncio
async def test_get_all_tasks():
    async with httpx.AsyncClient(follow_redirects=True) as client:
        r = await client.get(f"{BASE_URL}/api/v1/tasks")
        assert r.status_code == 200
        data = r.json()
        assert isinstance(data, list)

@pytest.mark.asyncio
async def test_get_task(created_task_id):
    print("Received task ID:", created_task_id)
    async with httpx.AsyncClient(follow_redirects=True) as client:
        r = await client.get(f"{BASE_URL}/api/v1/tasks/{created_task_id}")
        assert r.status_code == 200
        data = r.json()
        assert data["title"] == "Test Task"
        assert "title" in data
        assert "description" in data
        assert "priority" in data
        assert "due_date" in data
        assert "completed" in data

@pytest.mark.asyncio
async def test_update_task(created_task_id):
    task_data = {
        "title": "Test Update Task",
        "description": "This is an update test",
        "priority": 1,
        "due_date": "2025-12-31T23:59:59",
        "completed": False
    }
    async with httpx.AsyncClient(follow_redirects=True) as client:
        r = await client.put(f"{BASE_URL}/api/v1/tasks/{created_task_id}", json=task_data)
        assert r.status_code == 200
        data = r.json()
        assert data["title"] == "Test Update Task"
        assert data["description"] == "This is an update test"
        assert data["priority"] == 1
        assert data["due_date"] == "2025-12-31T23:59:59"
        assert data["completed"] == False

@pytest.mark.asyncio
async def test_patch_task(created_task_id):
    task_data = {
        "completed": True
    }
    async with httpx.AsyncClient(follow_redirects=True) as client:
        r = await client.patch(f"{BASE_URL}/api/v1/tasks/{created_task_id}", json=task_data)
        assert r.status_code == 200
        data = r.json()
        assert data["completed"] == True

@pytest.mark.asyncio
async def test_delete_task(created_task_id):
    async with httpx.AsyncClient(follow_redirects=True) as client:
        r = await client.delete(f"{BASE_URL}/api/v1/tasks/{created_task_id}")
        assert r.status_code in (200, 204)
        r = await client.get(f"{BASE_URL}/api/v1/tasks/{created_task_id}")
        assert r.status_code == 404

@pytest.mark.asyncio
async def test_get_task_not_found():
    fake_id = "000000000000000000000000"  
    async with httpx.AsyncClient(follow_redirects=True) as client:
        r = await client.get(f"{BASE_URL}/api/v1/tasks/{fake_id}")
        assert r.status_code == 404

@pytest.mark.asyncio
async def test_delete_task_not_found():
    fake_id = "000000000000000000000000"
    async with httpx.AsyncClient(follow_redirects=True) as client:
        r = await client.delete(f"{BASE_URL}/api/v1/tasks/{fake_id}")
        assert r.status_code == 404

@pytest.mark.asyncio
async def test_create_task_invalid_data():
    invalid_task = {
        "title": "",
        "description": "Invalid task",
        "priority": -1,
        "due_date": "invalid-date-format"
    }
    async with httpx.AsyncClient(follow_redirects=True) as client:
        r = await client.post(f"{BASE_URL}/api/v1/tasks", json=invalid_task)
        assert r.status_code == 422 