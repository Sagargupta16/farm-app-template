from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_health_check():
    """Test the health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "message" in data


def test_root_endpoint():
    """Test the root endpoint when client_build doesn't exist"""
    response = client.get("/")
    assert response.status_code == 200


# Note: User CRUD tests require a running MongoDB instance.
# In a real scenario, use pytest fixtures with mongomock or a test database.
# Example:
#
# @pytest.fixture
# def mock_db(monkeypatch):
#     """Mock the database for testing"""
#     ...
#
# def test_create_user(mock_db):
#     user_data = {"name": "Test User", "email": "test@example.com"}
#     response = client.post("/api/v1/users", json=user_data)
#     assert response.status_code == 200
#     assert response.json()["name"] == "Test User"

# Delete this file if you don't want to use it. Use *_test.py pattern to create new test files.
