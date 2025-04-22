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
        logger.info(f"Processing input: {user_input}")

        # --- Prompt Engineering ---
        # Format the input to guide the model to respond like an assistant
        # This format is common for chat models like Llama variants
        formatted_prompt = f"User: {user_input}\nAssistant:"

        logger.info(f"Sending formatted prompt to LLM: {formatted_prompt}")

        # Use ainvoke for async operation with Langchain
        response = await llm.ainvoke(formatted_prompt)

        logger.info("✅ LLM raw response generated successfully")
        logger.info(f"Raw LLM response: {response}") # Log raw response for debugging

        # --- Post-processing (Optional but Recommended) ---
        # The model's output might still include the "Assistant:" part or leading/trailing whitespace.
        # We can trim this. It might also sometimes include a stray newline or space before the actual response.
        processed_response = response.strip()

        # Some models might regenerate the "Assistant:" tag, let's remove it if it's at the start
        if processed_response.lower().startswith("assistant:"):
             processed_response = processed_response[len("assistant:"):].strip()

        logger.info(f"Processed LLM response: {processed_response}")

        return {"output": processed_response}

    except Exception as e:
        logger.error(f"❌ Error in LLM invocation: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error": "Failed to get response from AI",
                "detail": str(e)
            }
        )

# --- Health Check ---
@app.get("/health")
async def health_check():
    # Check if LLM object is initialized
    llm_status = "connected" if 'llm' in globals() and llm else "disconnected"
    return {
        "status": "healthy",
        "version": "1.0",
        "llm_status": llm_status
    }

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