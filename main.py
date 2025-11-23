from fastapi import FastAPI, UploadFile, File, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from .models import (
    AssessPriorityRequest, 
    AssessPriorityResponse, 
    CategorizeResponse,
    IssueCategory,
    PriorityLevel
)

# -------------------------------------------------------
# ⚙️ FastAPI App Setup
# -------------------------------------------------------
app = FastAPI(title="Civic AI Orchestrator", version="1.0.0")

# Enable CORS (Allowing frontend or other services to connect)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Adjust in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------------------------------------
# Health Check Endpoints
# -------------------------------------------------------
@app.get("/")
def root():
    return {"message": "Civic AI Orchestrator is running."}

@app.get("/health/live", tags=["Health"])
def liveness_check():
    """Liveness probe — confirms app process is alive."""
    return {"status": "alive"}

@app.get("/health/ready", tags=["Health"])
def readiness_check():
    """Readiness probe — confirms service is ready to accept traffic."""
    # If you add external dependencies (like OpenAI API or TensorFlow), check them here.
    return {"status": "ready"}

# -------------------------------------------------------
# AI Endpoints
# -------------------------------------------------------

@app.post("/internal/ai/categorize", response_model=CategorizeResponse)
async def categorize_issue_image(file: UploadFile = File(...)):
    """
    Analyzes an uploaded image file and determines the issue category.
    """
    # TODO: Implement Image Recognition Logic (e.g., TensorFlow, OpenAI Vision, AWS Rekognition)
    # 1. Read file bytes: contents = await file.read()
    # 2. Send to model
    # 3. Return result
    
    pass

@app.post("/internal/ai/assess-priority", response_model=AssessPriorityResponse)
def assess_issue_priority(payload: AssessPriorityRequest):
    """
    Analyzes the description text to determine urgency/priority.
    """
    # TODO: Implement NLP Logic (e.g., Keyword search, Sentiment Analysis, LLM)
    # 1. Parse payload.description
    # 2. Determine severity
    
    pass