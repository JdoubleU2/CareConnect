import requests
import time
import sys
import os
from openai import OpenAI

def test_server():
    # Start the server in a separate process
    import subprocess
    server_process = subprocess.Popen(['python', 'main.py'])
    
    # Wait for server to start
    time.sleep(5)
    
    try:
        # Test basic health check endpoint
        response = requests.get('http://localhost:8080/health')
        assert response.status_code == 200, f"Health check failed with status {response.status_code}"
        print("✅ Health check passed")
        
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
        server_process.terminate()
        server_process.wait()
    
    print("✅ All tests passed")
    return 0

if __name__ == "__main__":
    sys.exit(test_server()) 