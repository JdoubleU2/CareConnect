# CareConnect User Operation Manual

## Table of Contents
1. [Running the Model Locally with Ollama](#1-running-the-model-locally-with-ollama)
2. [Running the Development Server](#2-running-the-development-server)
3. [Creating Custom Endpoints](#3-creating-custom-endpoints)

## 1. Running the Model Locally with Ollama

### Prerequisites
- Install Ollama from [ollama.ai](https://ollama.ai)
- Ensure you have sufficient disk space (at least 4GB for the model)

### Steps to Run the Model
1. Open your terminal
2. Pull and run the CareConnect model using:
   ```bash
   ollama run hf.co/JdoubleU/careconnect-llama3.2-3b
   ```
3. The model will be downloaded and started automatically
4. You can interact with the model directly in the terminal

### Model Information
- Model: careconnect-llama3.2-3b
- Source: Hugging Face repository [careconnect-llama3.2-3b](https://huggingface.co/JdoubleU/careconnect-llama3.2-3b)
- Note: A newer version (careconnect-gemma3-4b) is coming soon

## 2. Running the Development Server

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Git

### Setup Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/JdoubleU2/CareConnect.git
   cd CareConnect
   ```

2. Navigate to the app directory:
   ```bash
   cd app
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Start the development server:
   ```bash
   python main.py
   ```

5. Access the web interface:
   - Open your browser
   - Navigate to `http://localhost:5000` (or the port specified in the console output)

### Development Server Features
- Hot-reloading for development
- API endpoints for model interaction
- Web interface for user interaction
- Comprehensive testing suite

## 3. Creating Custom Endpoints

### Understanding the Structure
The main server code is in `app/main.py`. To add new endpoints:

1. Open `main.py` in your preferred editor
2. Locate the route definitions (using Flask's `@app.route` decorators)
3. Add your new endpoint following the existing pattern

### Example Endpoint Creation
```python
@app.route('/api/your-endpoint', methods=['POST'])
def your_endpoint():
    # Your endpoint logic here
    return jsonify({'response': 'your response'})
```

### Testing Your Endpoint
1. Use the included test suite:
   ```bash
   python test_server.py
   ```

2. Test manually using curl or Postman:
   ```bash
   curl -X POST http://localhost:5000/api/your-endpoint
   ```

### Best Practices
1. Always include error handling
2. Document your endpoint in the code
3. Add appropriate tests
4. Follow the existing code style
5. Use type hints for better code clarity

### Communication with Frontend
- Endpoints should return JSON responses
- Use appropriate HTTP status codes
- Include error messages in the response when needed
- Follow RESTful API design principles

### Security Considerations
1. Validate all input data
2. Implement rate limiting if needed
3. Use appropriate authentication for sensitive endpoints
4. Sanitize all user inputs
5. Follow security best practices for API design

## Support and Resources
For additional help or questions, contact:
- Team Lead & LLM Training Lead: Jabin Wade (jwade23@pvamu.edu)
- Lead Data Engineer: Zero Nelson (jnelson50@pvamu.edu)
- Lead Web Developer: Aubrey Lister (alister3@pvamu.edu)
- Lindsey Littlejohn (llittlejohn@pvamu.edu) 