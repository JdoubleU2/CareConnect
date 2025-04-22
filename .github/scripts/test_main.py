from fastapi.testclient import TestClient
import pytest
from unittest.mock import patch, MagicMock, AsyncMock
import logging

# Mock the HuggingFaceEndpoint before importing app
with patch('app.main.HuggingFaceEndpoint', return_value=MagicMock()):
    from app.main import app

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create a test client that will make requests to our FastAPI app
client = TestClient(app)

def test_health_check():
    """
    Test the health check endpoint (/health)
    This endpoint should return a 200 status code and include status, version, and endpoint_status
    """
    logger.info("🔍 Testing health check endpoint...")
    response = client.get("/health")
    logger.info(f"📊 Health check response status: {response.status_code}")
    logger.info(f"📦 Health check response data: {response.json()}")
    
    assert response.status_code == 200, "Health check should return 200 status code"
    data = response.json()
    assert "status" in data, "Response should include 'status' field"
    assert "version" in data, "Response should include 'version' field"
    assert "endpoint_status" in data, "Response should include 'endpoint_status' field"
    assert data["endpoint_status"] in ["online", "offline"], "endpoint_status should be either 'online' or 'offline'"
    logger.info("✅ Health check test passed!")

@pytest.mark.asyncio
@patch('app.main.llm')
async def test_llm_invoke_success(mock_llm):
    """
    Test successful LLM invocation
    This test mocks the LLM response and verifies the endpoint returns the expected response
    """
    logger.info("🔍 Testing successful LLM invocation...")
    
    # Mock the LLM to return a test response
    test_response = "This is a test response"
    mock_llm.ainvoke = AsyncMock(return_value=test_response)
    logger.info(f"🤖 Mocked LLM response: {test_response}")
    
    # Prepare test input
    test_input = {"input": "Hello, how are you?"}
    logger.info(f"📤 Sending test input: {test_input}")
    
    # Make the request
    response = client.post("/llm/invoke", json=test_input)
    logger.info(f"📊 Response status: {response.status_code}")
    logger.info(f"📦 Response data: {response.json()}")
    
    # Verify the response
    assert response.status_code == 200, "LLM invocation should return 200 status code"
    data = response.json()
    assert "output" in data, "Response should include 'output' field"
    assert data["output"] == test_response, "Response should match mocked LLM output"
    logger.info("✅ LLM success test passed!")

@pytest.mark.asyncio
@patch('app.main.llm')
async def test_llm_invoke_error(mock_llm):
    """
    Test LLM invocation error handling
    This test simulates an error from the LLM and verifies proper error handling
    """
    logger.info("🔍 Testing LLM error handling...")
    
    # Mock the LLM to raise an exception
    error_message = "Test error"
    mock_llm.ainvoke = AsyncMock(side_effect=Exception(error_message))
    logger.info(f"❌ Mocked LLM error: {error_message}")
    
    # Prepare test input
    test_input = {"input": "Hello, how are you?"}
    logger.info(f"📤 Sending test input: {test_input}")
    
    # Make the request
    response = client.post("/llm/invoke", json=test_input)
    logger.info(f"📊 Response status: {response.status_code}")
    logger.info(f"📦 Response data: {response.json()}")
    
    # Verify error response
    assert response.status_code == 500, "Error should return 500 status code"
    data = response.json()
    assert "detail" in data, "Error response should include 'detail' field"
    assert data["detail"]["error"] == "Failed to get response from AI", "Error message should match expected"
    assert data["detail"]["detail"] == error_message, "Error detail should match the exception message"
    logger.info("✅ LLM error test passed!")

def test_static_files():
    """
    Test static file serving
    This test verifies that the static files endpoint is working
    """
    logger.info("🔍 Testing static file serving...")
    
    # Try to access the root endpoint which should serve static files
    response = client.get("/")
    logger.info(f"📊 Static files response status: {response.status_code}")
    
    # The response should be either 200 (if index.html exists) or 404 (if it doesn't)
    assert response.status_code in [200, 404], "Static files endpoint should return 200 or 404"
    logger.info("✅ Static files test passed!") 