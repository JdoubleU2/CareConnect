from fastapi import FastAPI
from langserve import add_routes
from langchain_huggingface import HuggingFaceEndpoint
from langchain_community.llms import HuggingFaceHub
import os

app = FastAPI()

# Load the model from Hugging Face Hub
llm = HuggingFaceEndpoint(
    repo_id="JdoubleU/careconnect-llama3.2-3b",
    temperature=0.7,
    max_new_tokens=512,
    huggingfacehub_api_token=os.environ.get("HF_TOKEN")
)

# Add LangServe endpoint
add_routes(app, llm, path="/")

# Serve the app with correct port
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run("app.main:app", host="0.0.0.0", port=port)

