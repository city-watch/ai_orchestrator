import os
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from google.cloud import vision # pip install google-cloud-vision
from dotenv import load_dotenv
import logging

load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

from models import (
    AssessPriorityRequest, 
    AssessPriorityResponse, 
    CategorizeResponse,
    PriorityLevel
)

# -------------------------------------------------------
# Configuration
# -------------------------------------------------------
# Ensure GOOGLE_APPLICATION_CREDENTIALS is set in your environment
# export GOOGLE_APPLICATION_CREDENTIALS="/path/to/gcp_key.json"

app = FastAPI(title="Civic AI Orchestrator", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------------------------------------
# AI Logic Helpers
# -------------------------------------------------------
def map_labels_to_category(labels) -> tuple[str, float]:
    """
    Maps Google Vision labels. 
    1. Checks for specific priority keywords (Potholes, etc).
    2. If no match, uses the top detected label dynamically.
    """
    # Critical categories we specifically want to track
    keyword_map = {
        "Pothole": ["pothole", "asphalt", "road surface", "tar"],
        "Graffiti": ["graffiti", "spray paint", "mural", "street art", "wall"],
        "Trash": ["trash", "waste", "garbage", "litter", "plastic bag", "rubbish"],
        "Street Light": ["street light", "lamp", "lighting", "electricity"]
    }

    # 1. Try to match specific keywords first
    for label in labels:
        label_text = label.description.lower()
        confidence = label.score

        for category, keywords in keyword_map.items():
            if any(k in label_text for k in keywords):
                return category, confidence

    # 2. If no keyword match, return the most confident label found
    # This allows "Trees", "Flooding", "Cars" etc. to be valid categories
    if labels:
        top_label = labels[0]
        return top_label.description.title(), top_label.score

    # 3. Fallback
    return "Uncategorized", 0.0


def determine_priority_from_text(text: str) -> tuple[PriorityLevel, str]:
    """
    Simple NLP rule-based logic to determine priority.
    """
    text = text.lower()
    
    high_keywords = ["danger", "accident", "huge", "blocked", "urgent", "broken glass", "flood", "fire"]
    medium_keywords = ["bad", "annoying", "large", "stuck", "leak"]
    
    if any(k in text for k in high_keywords):
        return PriorityLevel.HIGH, "Detected urgent keywords indicating safety risk."
    
    if any(k in text for k in medium_keywords):
        return PriorityLevel.MEDIUM, "Detected keywords indicating moderate inconvenience."
        
    return PriorityLevel.LOW, "No urgent keywords detected; standard priority."

# -------------------------------------------------------
# Endpoints
# -------------------------------------------------------

@app.get("/")
def root():
    return {"message": "Civic AI Orchestrator is running."}

@app.get("/health/live")
def liveness_check():
    return {"status": "alive"}

@app.post("/internal/ai/categorize", response_model=CategorizeResponse)
async def categorize_issue_image(file: UploadFile = File(...)):
    """
    Uses Google Cloud Vision API to detect labels in the image 
    and categorize the issue.
    """
    try:
        # 1. Initialize Client
        client = vision.ImageAnnotatorClient()

        # 2. Read Image Bytes
        content = await file.read()
        image = vision.Image(content=content)

        # 3. Call Google Vision API (Label Detection)
        response = client.label_detection(image=image)
        
        if response.error.message:
            raise HTTPException(status_code=500, detail=f"Google Vision API Error: {response.error.message}")

        # 4. Map Results
        category, confidence = map_labels_to_category(response.label_annotations)
        
        return CategorizeResponse(category=category, confidence=confidence)

    except HTTPException as e:
        raise e
    except Exception as e:
        logging.error(f"AI Error: {e}")
        return CategorizeResponse(category="Uncategorized", confidence=0.0)


@app.post("/internal/ai/assess-priority", response_model=AssessPriorityResponse)
def assess_issue_priority(payload: AssessPriorityRequest):
    """
    Analyzes description text for keywords to flag priority.
    """
    priority, reasoning = determine_priority_from_text(payload.description)
    return AssessPriorityResponse(priority=priority, reasoning=reasoning)