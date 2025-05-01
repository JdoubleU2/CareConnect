# CareConnect Web Application

This directory contains the backend server and API implementation for the CareConnect web application.

## 🏗️ Architecture Overview

The web application consists of three main components:
1. Frontend (React + Firebase Hosting)
2. Backend Server (Python + FastAPI)
3. AI Model (Hosted on Hugging Face)

## 🔧 Backend Server

The backend server (`main.py`) is built using FastAPI and provides the following functionality:

### API Endpoints
- `/chat`: Main endpoint for handling chat interactions with the AI model
- `/health`: Health check endpoint for monitoring
- `/docs`: Auto-generated API documentation (Swagger UI)

### Server Features
- Asynchronous request handling
- Rate limiting and request validation
- Error handling and logging
- CORS configuration for frontend integration
- Environment-based configuration

## 🤖 AI Model Integration

The AI model is hosted on Hugging Face's Inference API, which provides:
- Scalable model deployment
- Automatic load balancing
- Secure API access
- Version control for model updates

### Model Endpoint
- Model: `careconnect-llama3.2-3b`
- Host: Hugging Face Inference API
- Endpoint: `https://api-inference.huggingface.co/models/JdoubleU/careconnect-llama3.2-3b`

### API Integration
The server communicates with the Hugging Face endpoint using:
```python
headers = {
    "Authorization": f"Bearer {HF_API_KEY}",
    "Content-Type": "application/json"
}

response = requests.post(
    "https://api-inference.huggingface.co/models/JdoubleU/careconnect-llama3.2-3b",
    headers=headers,
    json={"inputs": user_input}
)
```

## 🚀 Deployment

### Google Cloud Run
The server is containerized and deployed on Google Cloud Run:
- Automatic scaling
- HTTPS endpoint
- Environment variable management
- Health monitoring

### Environment Variables
Required environment variables:
- `HF_API_KEY`: Hugging Face API key
- `PORT`: Server port (default: 8080)
- `ENVIRONMENT`: Deployment environment (dev/prod)

## 🛠️ Local Development

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Set up environment variables:
   ```bash
   export HF_API_KEY=your_huggingface_api_key
   export PORT=8080
   export ENVIRONMENT=dev
   ```

3. Run the development server:
   ```bash
   python main.py
   ```

4. Run tests:
   ```bash
   python -m pytest test_server.py
   ```

## 📦 Docker Deployment

Build the Docker image:
```bash
docker build -t careconnect-server .
```

Run the container:
```bash
docker run -p 8080:8080 \
  -e HF_API_KEY=your_huggingface_api_key \
  -e ENVIRONMENT=prod \
  careconnect-server
```

## 🔍 Testing

The application includes comprehensive tests in `test_server.py`:
- API endpoint testing
- Model integration testing
- Error handling tests
- Performance benchmarks

Run tests with:
```bash
python -m pytest test_server.py
```

## 📚 API Documentation

Access the interactive API documentation at:
- Swagger UI: `http://localhost:8080/docs`
- ReDoc: `http://localhost:8080/redoc`

## 🔒 Security

- API key management through environment variables
- Rate limiting to prevent abuse
- Input validation and sanitization
- CORS configuration for frontend security
- HTTPS enforcement in production

## 📈 Monitoring

The server includes:
- Health check endpoint (`/health`)
- Request logging
- Error tracking
- Performance metrics


## 📞 Support

For technical support or questions about the backend implementation, contact:
- Lead Web Developer: Aubrey Lister [alister3@pvamu.edu](mailto:alister3@pvamu.edu)
- Team Lead: Jabin Wade [jwade23@pvamu.edu](mailto:Jwade23@pvamu.edu) 
