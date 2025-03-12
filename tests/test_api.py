# tests/test_api.py
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_read_projects_unauthorized():
    response = client.get("/projects/")
    # Since the /projects GET endpoint requires a valid JWT, an unauthorized request should return 401
    assert response.status_code == 401