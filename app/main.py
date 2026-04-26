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
import httpx
import os
import logging
import re
from pathlib import Path
from typing import Any, Optional
from pydantic import BaseModel, Field

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
HF_ENDPOINT_URL = os.getenv(
    "HUGGINGFACE_ENDPOINT_URL",
    "https://njpcqfadrmo0m5xq.us-east4.gcp.endpoints.huggingface.cloud"
)
HF_API_KEY = os.getenv("HUGGINGFACE_API_KEY") or os.getenv("HUGGINGFACE_API_TOKEN")

if HF_API_KEY:
    logger.info("✅ HuggingFace LLM configuration loaded successfully")
else:
    logger.warning(
        "⚠️ No Hugging Face API key found. LLM requests will return a service-unavailable error until configured."
    )

EMERGENCY_KEYWORDS = [
    "chest pain",
    "can't breathe",
    "difficulty breathing",
    "shortness of breath",
    "asthma attack",
    "seizure",
    "heart attack",
    "stroke",
    "unconscious",
    "unable to stand",
    "uncontrolled bleeding",
    "poison",
    "overdose",
    "suicidal",
    "head injury",
    "confused",
    "slurred speech",
    "rapid heartbeat",
    "vomiting blood",
]

EMERGENCY_RESPONSE = (
    "⚠️ This may be a medical emergency. Please seek immediate medical attention or call emergency services right away."
)

SUMMARY_SYMPTOM_HINTS = {
    "stomach pain": ["stomach", "abdominal", "abdomen", "belly pain"],
    "headache": ["headache", "migraine", "head hurts"],
    "toothache": ["tooth", "toothache", "dental pain"],
    "chest pain": ["chest pain", "chest tightness"],
    "shortness of breath": ["shortness of breath", "difficulty breathing", "can't breathe"],
    "fever": ["fever", "temperature", "high temp"],
    "nausea": ["nausea", "nauseous", "queasy"],
    "vomiting": ["vomit", "vomiting", "threw up"],
    "diarrhea": ["diarrhea", "loose stool"],
    "sore throat": ["sore throat", "throat pain"],
    "cough": ["cough", "coughing"],
    "dizziness": ["dizzy", "dizziness", "lightheaded"],
}

# --- Input Model ---
class GenerationParameters(BaseModel):
    max_new_tokens: int = Field(default=200, ge=1)
    temperature: float = Field(default=0.7, ge=0.0)
    top_p: float = Field(default=0.9, ge=0.0, le=1.0)
    do_sample: bool = True


class LLMInput(BaseModel):
    inputs: Optional[str] = None
    input: Optional[str] = None
    parameters: GenerationParameters = Field(default_factory=GenerationParameters)


class ChatMessage(BaseModel):
    role: str
    content: str


class SummaryInput(BaseModel):
    conversation: list[ChatMessage] = Field(default_factory=list)
    parameters: GenerationParameters = Field(default_factory=GenerationParameters)


async def call_hf_endpoint(payload: dict[str, Any]) -> Any:
    if not HF_API_KEY:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail={
                "error": "Hugging Face API key is not configured",
                "detail": "Set HUGGINGFACE_API_KEY or HUGGINGFACE_API_TOKEN in the runtime environment."
            }
        )

    headers = {
        "Authorization": f"Bearer {HF_API_KEY}",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }

    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.post(HF_ENDPOINT_URL, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()


def extract_generated_text(response_data: Any) -> str:
    if isinstance(response_data, list) and response_data:
        first_item = response_data[0]
        if isinstance(first_item, dict):
            for key in ("generated_text", "text", "content"):
                if key in first_item and first_item[key]:
                    return str(first_item[key])
    elif isinstance(response_data, dict):
        for key in ("generated_text", "text", "content", "output"):
            if key in response_data and response_data[key]:
                return str(response_data[key])

        if "choices" in response_data and response_data["choices"]:
            first_choice = response_data["choices"][0]
            if isinstance(first_choice, dict):
                message = first_choice.get("message", {})
                if isinstance(message, dict) and message.get("content"):
                    return str(message["content"])
                if first_choice.get("text"):
                    return str(first_choice["text"])

    return str(response_data)


def contains_emergency_keywords(text: str) -> bool:
    lowered = text.lower()
    return any(keyword in lowered for keyword in EMERGENCY_KEYWORDS)


def strip_assistant_prefix(text: str) -> str:
    cleaned = text.strip()
    if cleaned.lower().startswith("assistant:"):
        return cleaned[len("assistant:"):].strip()
    return cleaned


def extract_symptoms_from_conversation(conversation: list[ChatMessage]) -> list[str]:
    user_text = "\n".join(
        message.content.lower()
        for message in conversation
        if message.role.lower() == "user" and message.content.strip()
    )

    extracted: list[str] = []
    for symptom, hints in SUMMARY_SYMPTOM_HINTS.items():
        if any(hint in user_text for hint in hints):
            extracted.append(symptom)

    return extracted or ["No clear symptoms provided"]


def format_symptoms(symptoms: list[str]) -> str:
    return "\n".join(f"- {symptom}" for symptom in symptoms)


def build_summary_prompt(symptoms_text: str, conversation_text: str) -> str:
    return (
        "Based on this medical support conversation, provide:\n\n"
        "Advice:\n"
        "- ...\n\n"
        "Next Steps:\n"
        "- ...\n\n"
        "Known Symptoms (already extracted from user messages):\n"
        f"{symptoms_text}\n\n"
        "Conversation:\n"
        f"{conversation_text}\n\n"
        "Rules:\n"
        "- Do NOT add new symptoms\n"
        "- Do NOT repeat lines or ideas\n"
        "- Keep it concise and practical\n"
        "- Keep language supportive and non-diagnostic\n"
        "- Max 5 bullets in Advice and max 5 bullets in Next Steps\n"
    )


def extract_advice_and_steps(text: str) -> tuple[str, str]:
    """Extract only Advice and Next Steps sections from model output, discarding everything else."""
    advice_lines: list[str] = []
    steps_lines: list[str] = []
    current_section: str | None = None

    for line in text.splitlines():
        stripped = line.strip()
        lower_stripped = stripped.lower()

        # Check if this line marks a section header
        if lower_stripped.startswith("advice"):
            current_section = "advice"
            continue
        elif lower_stripped.startswith("next steps"):
            current_section = "steps"
            continue

        # If we hit unrelated headers, stop collecting for current section
        if any(
            lower_stripped.startswith(header)
            for header in ["rules", "conversation", "known symptoms", "based on", "symptoms:"]
        ):
            current_section = None
            continue

        # Only collect content bullets/items (lines starting with -, *, digits+)
        if current_section and stripped and (
            stripped.startswith("-")
            or stripped.startswith("*")
            or (len(stripped) > 1 and stripped[0].isdigit() and stripped[1] in [".", ")"])
        ):
            if current_section == "advice":
                advice_lines.append(stripped)
            elif current_section == "steps":
                steps_lines.append(stripped)

    # Deduplicate within each section
    def deduplicate(lines: list[str]) -> list[str]:
        seen: set[str] = set()
        unique: list[str] = []
        for line in lines:
            normalized = re.sub(r"\s+", " ", line.lower())
            normalized = re.sub(r"^[-*]\d+[\.)]\s*", "", normalized)
            if normalized not in seen:
                seen.add(normalized)
                unique.append(line)
        return unique

    advice_lines = deduplicate(advice_lines)[:5]  # Max 5
    steps_lines = deduplicate(steps_lines)[:5]  # Max 5

    advice_text = "\n".join(advice_lines) if advice_lines else "- Monitor symptoms and rest"
    steps_text = "\n".join(steps_lines) if steps_lines else "- Consult a healthcare professional if symptoms persist"

    return advice_text, steps_text


def conversation_to_text(conversation: list[ChatMessage]) -> str:
    return "\n".join(f"{message.role.title()}: {message.content}" for message in conversation if message.content.strip())

# --- Custom LLM Endpoint ---
@app.post("/api/llm/invoke")
@app.post("/llm/invoke")
async def invoke_llm(input_data: LLMInput):
    try:
        user_input = input_data.inputs or input_data.input
        if not user_input:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={"error": "Missing 'inputs' field in request body"}
            )

        logger.info(f"Processing input: {user_input}")

        if contains_emergency_keywords(user_input):
            logger.info("🚨 Emergency keyword detected in user input; returning emergency override response")
            return {
                "output": EMERGENCY_RESPONSE,
                "response_type": "emergency",
                "emergency_detected": True,
            }

try:
    formatted_prompt = f"""
You are CareConnect, a healthcare assistant chatbot.

STRICT RULES:
- Answer ONLY what the user says
- DO NOT assume conditions
- DO NOT introduce new symptoms or diseases
- DO NOT diagnose
- Keep responses SHORT (2-4 sentences max)
- Provide general advice only

User: {user_input}
Assistant:
"""

    payload = {
        "inputs": formatted_prompt,
        "parameters": input_data.parameters.model_dump(),
    }

    logger.info(f"Sending payload to LLM endpoint: {payload}")

        response_data = await call_hf_endpoint(payload)

        logger.info("✅ LLM raw response generated successfully")
        logger.info(f"Raw LLM response: {response_data}") # Log raw response for debugging

        processed_response = strip_assistant_prefix(extract_generated_text(response_data))

        if contains_emergency_keywords(processed_response):
            logger.info("🚨 Emergency keyword detected in model output; returning emergency override response")
            return {
                "output": EMERGENCY_RESPONSE,
                "response_type": "emergency",
                "emergency_detected": True,
            }

        # ✅ CONSISTENCY CHECK
        processed_response = consistency_checker(processed_response)

        return {
            "output": processed_response,
            "response_type": "assistant",
            "emergency_detected": False,
        }

    except Exception as e:
        logger.error(f"❌ Error in LLM invocation: {str(e)}")
        if isinstance(e, HTTPException):
            raise
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error": "Failed to get response from AI",
                "detail": str(e)
            }
        )


# --- Conversation Summary Endpoint ---
@app.post("/api/llm/summary")
@app.post("/llm/summary")
async def summarize_conversation(input_data: SummaryInput):
    try:
        if not input_data.conversation:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={"error": "Missing 'conversation' field in request body"}
            )

        symptoms = extract_symptoms_from_conversation(input_data.conversation)
        symptoms_text = format_symptoms(symptoms)

        conversation_text = conversation_to_text(input_data.conversation)
        # Keep prompt short enough for stable summarization
        conversation_excerpt = conversation_text[-1500:]
        summary_prompt = build_summary_prompt(symptoms_text, conversation_excerpt)

        payload = {
            "inputs": summary_prompt,
            "parameters": input_data.parameters.model_dump(),
        }

        logger.info("Sending summary payload to LLM endpoint")
        response_data = await call_hf_endpoint(payload)
        processed_summary = strip_assistant_prefix(extract_generated_text(response_data))
        
        # Extract only Advice and Next Steps, discard everything else
        advice_text, steps_text = extract_advice_and_steps(processed_summary)

        summary_output = (
            f"Symptoms:\n{symptoms_text}\n\n"
            f"Advice:\n{advice_text}\n\n"
            f"Next Steps:\n{steps_text}"
        )

        return {
            "summary": summary_output,
            "conversation_length": len(input_data.conversation),
            "symptoms": symptoms,
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Error generating summary: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error": "Failed to generate conversation summary",
                "detail": str(e)
            }
        )

# --- Health Check ---
@app.get("/api/health")
@app.get("/health")
async def health_check():
    try:
        # Simple test to check if endpoint is responding
        test_payload = {
            "inputs": "Hello",
            "parameters": GenerationParameters().model_dump(),
        }
        await call_hf_endpoint(test_payload)
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
