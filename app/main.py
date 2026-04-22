# ===== EMERGENCY KEYWORDS =====
EMERGENCY_KEYWORDS = [
    "chest pain", "can't breathe", "difficulty breathing", "shortness of breath",
    "asthma attack", "seizure", "heart attack", "stroke", "unconscious",
    "unable to stand", "uncontrolled bleeding", "poison", "overdose",
    "suicidal", "head injury", "confused", "slurred speech",
    "rapid heartbeat", "vomiting blood"
]

def emergency_override(user_message):
    message = user_message.lower()
    return any(keyword in message for keyword in EMERGENCY_KEYWORDS)


# ===== CONSISTENCY CHECKER =====
def consistency_checker(response):
    prohibited_words = ["diagnose", "cure"]

    for word in prohibited_words:
        if word in response.lower():
            response = response.replace(word, "suggest")

    if "consult a healthcare professional" not in response.lower():
        response += " Please consult a healthcare professional for medical advice."

    return response


# ===== SUMMARY GENERATOR =====
def extract_symptoms(user_input):
    symptoms = user_input.lower()
    extracted = []

    if "stomach" in symptoms or "abdominal" in symptoms:
        extracted.append("stomach pain")
    if "headache" in symptoms:
        extracted.append("headache")
    if "tooth" in symptoms:
        extracted.append("toothache")

    if not extracted:
        extracted.append("No clear symptoms provided")

    return extracted
    
from fastapi import FastAPI, Request, status, HTTPException # Import status
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from langchain_huggingface import HuggingFaceEndpoint
import os
import logging
from pathlib import Path
from pydantic import BaseModel

# --- Logging Config ---
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# --- FastAPI App Setup ---
app = FastAPI(
    title="CareConnect Backend",
    version="1.0",
    description="Backend API for CareConnect AI Health Assistant"
)

# --- CORS Middleware ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for local development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Logging Middleware for Requests ---
@app.middleware("http")
async def log_requests(request: Request, call_next):
    body = await request.body()
    # Decode body only if it exists and is not empty
    decoded_body = body.decode('utf-8') if body else 'No body'
    logger.info(f"🔹 Incoming request: {request.method} {request.url}")
    logger.info(f"🔹 Headers: {request.headers}")
    logger.info(f"🔹 Body: {decoded_body}") # Use the decoded_body here
    response = await call_next(request)
    logger.info(f"🔹 Response status: {response.status_code}")
    return response

# --- Hugging Face LLM Setup ---
try:
    llm = HuggingFaceEndpoint(
        endpoint_url="https://l3w62k457vzkn0yj.us-east4.gcp.endpoints.huggingface.cloud",
        huggingfacehub_api_token=os.getenv('HUGGINGFACE_API_KEY')
    )
    logger.info("✅ HuggingFace LLM initialized successfully")
except Exception as e:
    logger.error(f"❌ Failed to initialize HuggingFace LLM: {str(e)}")
    # Depending on criticality, you might want to let the app start but return an error on LLM requests,
    # or raise the exception to prevent the app from starting. Keeping the raise for now as in original.
    raise

# --- Input Model ---
class LLMInput(BaseModel):
    input: str

# --- Custom LLM Endpoint ---
@app.post("/llm/invoke")
async def invoke_llm(input_data: LLMInput):
    try:
        user_input = input_data.input

        # 🚨 EMERGENCY CHECK
        if emergency_override(user_input):
            return {
                "output": "⚠️ This may be a medical emergency. Please seek immediate medical attention or call emergency services."
            }

        # 🧠 CONTROLLED PROMPT (prevents hallucination)
        formatted_prompt = f"""
You are a healthcare assistant.

ONLY provide general advice.
DO NOT diagnose.
DO NOT add symptoms not mentioned.

User: {user_input}
Assistant:
"""

        response = await llm.ainvoke(formatted_prompt)

        processed_response = response.strip()

        if processed_response.lower().startswith("assistant:"):
            processed_response = processed_response[len("assistant:"):].strip()

        # ✅ CONSISTENCY CHECK
        processed_response = consistency_checker(processed_response)

        return {"output": processed_response}

    except Exception as e:
        logger.error(f"❌ Error: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to get response")

# --- Health Check ---
@app.get("/health")
async def health_check():
    try:
        # Simple test to check if endpoint is responding
        test_prompt = "Hello"
        await llm.ainvoke(test_prompt)
        endpoint_status = "online"
    except Exception as e:
        logger.error(f"Endpoint check failed: {str(e)}")
        endpoint_status = "offline"
    
    return {
        "status": "healthy",
        "version": "1.0",
        "endpoint_status": endpoint_status
    }

# Summary Endpoint
@app.post("/summary")
async def generate_summary_endpoint(input_data: LLMInput):
    try:
        conversation = input_data.input

        # Extract symptoms (same logic as Colab)
        symptoms = extract_symptoms(conversation)
        symptoms_text = "\n".join([f"- {s}" for s in symptoms])

        summary_prompt = f"""
Based on this conversation, provide:

Advice:
- ...

Next Steps:
- ...

Conversation:
{conversation}

Rules:
- Do NOT add symptoms
- Keep it concise
"""

        response = await llm.ainvoke(summary_prompt)
        output = response.strip()

        return {
            "symptoms": symptoms_text,
            "summary": output
        }

    except Exception as e:
        logger.error(f"❌ Summary Error: {str(e)}")
        raise HTTPException(status_code=500, detail="Summary failed")
        
# --- Static Files ---
# Mount the public directory to serve static files
# IMPORTANT: Mounted AFTER API routes to prevent potential conflicts
public_path = Path(__file__).parent / "public"
# Check if the directory exists before mounting
if public_path.is_dir():
    app.mount("/", StaticFiles(directory=str(public_path), html=True), name="static")
    logger.info(f"✅ Static files mounted from {public_path}")
else:
    logger.warning(f"⚠️ Static files directory not found: {public_path}. Static files will not be served.")


if __name__ == "__main__":
    import uvicorn
    logger.info("🚀 Starting CareConnect backend server...")
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8080,
        reload=True,
        log_level="info"
    )
