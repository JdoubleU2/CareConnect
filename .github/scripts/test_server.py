import requests
import time
import sys
import os
from openai import OpenAI

def test_server():
    # Start the server in a separate process
    import subprocess
    try:
        server_process = subprocess.Popen(['python', 'app/main.py'])
        
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
        
        # Test Hugging Face endpoint using OpenAI client
        client = OpenAI(
            base_url="https://l3w62k457vzkn0yj.us-east4.gcp.endpoints.huggingface.cloud/v1/",
            api_key=os.getenv("HUGGINGFACE_API_KEY")
        )
        
        chat_completion = client.chat.completions.create(
            model="tgi",
            messages=[
                {
                    "role": "user",
                    "content": "CareConnect. Are you ALIVE!?"
                }
            ],
            top_p=None
        )
        
        # Verify we got a response
        assert chat_completion.choices[0].message.content is not None, "No response content received"
        print("✅ Hugging Face endpoint test passed")
        print(f"Response: {chat_completion.choices[0].message.content[:100]}...")
        
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