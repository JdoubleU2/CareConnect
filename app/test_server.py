import requests
import time
import sys
import os

def test_server():
    # Start the server in a separate process
    import subprocess
    try:
        # Get API key from environment or GitHub secrets
        api_key = os.getenv('HUGGINGFACE_API_KEY')
        if not api_key:
            raise Exception("HUGGINGFACE_API_KEY environment variable is not set")
        
        # Set the environment variable for the server process
        env = os.environ.copy()
        env['HUGGINGFACE_API_KEY'] = api_key
        
        print("Starting server from current directory")
        server_process = subprocess.Popen(
            ['python', 'main.py'],
            env=env
        )
        
        # Wait for server to start with retries
        max_retries = 5
        retry_count = 0
        server_started = False
        
        while retry_count < max_retries and not server_started:
            try:
                response = requests.get('http://localhost:8080/health', timeout=5)
                if response.status_code == 200:
                    server_started = True
                    print("✅ Server started successfully")
            except requests.exceptions.RequestException:
                print(f"Waiting for server to start... (attempt {retry_count + 1}/{max_retries})")
                time.sleep(10)
                retry_count += 1
        
        if not server_started:
            raise Exception("Server failed to start within the timeout period")
        
        # Test Hugging Face endpoint directly
        endpoint_url = "https://l3w62k457vzkn0yj.us-east4.gcp.endpoints.huggingface.cloud"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
            "Accept": "application/json"
        }
        
        data = {
            "inputs": "CareConnect. Are you ALIVE!?",
            "parameters": {
                "max_new_tokens": 100,
                "temperature": 0.7,
                "top_p": 0.95,
                "do_sample": True
            }
        }
        
        response = requests.post(
            endpoint_url,
            headers=headers,
            json=data,
            timeout=30
        )
        
        # Verify we got a response
        assert response.status_code == 200, f"Endpoint returned status code {response.status_code}"
        response_data = response.json()
        assert "choices" in response_data, "Response missing choices field"
        assert len(response_data["choices"]) > 0, "No choices in response"
        assert "message" in response_data["choices"][0], "Choice missing message field"
        assert "content" in response_data["choices"][0]["message"], "Message missing content field"
        
        print("✅ Hugging Face endpoint test passed")
        print(f"Response: {response_data['choices'][0]['message']['content'][:100]}...")
        
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")
        return 1
    finally:
        # Clean up
        if 'server_process' in locals():
            server_process.terminate()
            server_process.wait()
    
    print("✅ All tests passed")
    return 0

if __name__ == "__main__":
    sys.exit(test_server()) 