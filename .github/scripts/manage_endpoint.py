import os
import requests
import time
import sys
from dotenv import load_dotenv

def get_headers():
    return {
        "Authorization": f"Bearer {os.getenv('HUGGINGFACE_API_TOKEN')}",
        "Content-Type": "application/json"
    }

def get_endpoint_status():
    endpoint_url = os.getenv('HUGGINGFACE_ENDPOINT_URL')
    endpoint_id = endpoint_url.split('/')[-2]  # Extract endpoint ID from URL
    api_url = f"https://api.endpoints.huggingface.cloud/v2/endpoint/{endpoint_id}"
    
    response = requests.get(api_url, headers=get_headers())
    if response.status_code == 200:
        return response.json()["status"]
    return None

def start_endpoint():
    endpoint_url = os.getenv('HUGGINGFACE_ENDPOINT_URL')
    endpoint_id = endpoint_url.split('/')[-2]  # Extract endpoint ID from URL
    api_url = f"https://api.endpoints.huggingface.cloud/v2/endpoint/{endpoint_id}/start"
    
    print("Starting endpoint...")
    response = requests.post(api_url, headers=get_headers())
    
    if response.status_code != 200:
        print(f"Failed to start endpoint: {response.text}")
        return False
    
    # Wait for endpoint to be ready
    max_retries = 30
    for i in range(max_retries):
        status = get_endpoint_status()
        if status == "running":
            print("Endpoint is running!")
            return True
        elif status == "failed":
            print("Endpoint failed to start")
            return False
        print(f"Waiting for endpoint to start... ({i+1}/{max_retries})")
        time.sleep(10)
    
    print("Timed out waiting for endpoint to start")
    return False

def stop_endpoint():
    endpoint_url = os.getenv('HUGGINGFACE_ENDPOINT_URL')
    endpoint_id = endpoint_url.split('/')[-2]  # Extract endpoint ID from URL
    api_url = f"https://api.endpoints.huggingface.cloud/v2/endpoint/{endpoint_id}/stop"
    
    print("Stopping endpoint...")
    response = requests.post(api_url, headers=get_headers())
    
    if response.status_code != 200:
        print(f"Failed to stop endpoint: {response.text}")
        return False
    
    return True

if __name__ == "__main__":
    # Load environment variables from the app directory
    load_dotenv('../app/.env')
    
    if len(sys.argv) != 2 or sys.argv[1] not in ["start", "stop", "status"]:
        print("Usage: python manage_endpoint.py [start|stop|status]")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "start":
        success = start_endpoint()
        sys.exit(0 if success else 1)
    elif command == "stop":
        success = stop_endpoint()
        sys.exit(0 if success else 1)
    elif command == "status":
        status = get_endpoint_status()
        print(f"Endpoint status: {status}")
        sys.exit(0 if status == "running" else 1) 