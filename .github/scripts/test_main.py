import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["version"] == "1.0"
    assert data["llm_status"] == "connected"

def test_llm_invoke_success():
    response = client.post(
        "/llm/invoke",
        json={"prompt": "Hello, how are you?"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "response" in data
    assert isinstance(data["response"], str)

def test_llm_invoke_error():
    response = client.post(
        "/llm/invoke",
        json={"prompt": ""}
    )
    assert response.status_code == 400
    data = response.json()
    assert "detail" in data
    assert "error" in data

def test_static_files():
    response = client.get("/static/index.html")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"] 