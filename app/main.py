from fastapi import FastAPI
from langserve import add_routes
from langchain_huggingface import HuggingFaceEndpoint
# from langchain_community.llms import HuggingFaceHub # This import is not used, can be removed
import os
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="My LLM Backend", # Add a title
    version="1.0" # Add a version
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # WARNING: This allows ANY origin. Restrict this in production!
                          # If using Firebase Hosting Rewrites, you might not need wide open CORS.
                          # Consider removing this or restricting it once deployed via rewrites.
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Load the model from Hugging Face Hub
# Pass the API token if available. HuggingFaceEndpoint handles None token.
llm = HuggingFaceEndpoint(
    repo_id="JdoubleU/careconnect-llama3.2-3b",
    temperature=0.7,
    task='text-generation',
    max_new_tokens=1000,
)
# ---------------------------------------------------------

# Add LangServe endpoint
add_routes(app, llm, path="/llm")

# You can add a root endpoint for health checks or basic info
@app.get("/")
async def read_root():
    return {"message": "FastAPI Backend for LLM is running"}

# The if __name__ == "__main__": block is not strictly needed for Cloud Run
# when using the CMD in the Dockerfile, but it doesn't hurt to keep it for local testing.
# if __name__ == "__main__":
#     import uvicorn
#     port = int(os.environ.get("PORT", 8080))
#     uvicorn.run(app, host="0.0.0.0", port=port) # Use `app` directly here