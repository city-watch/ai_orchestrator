from pydantic import BaseModel
from enum import Enum

# -------------------------------------------------------
# Enums (Strict Type Definitions)
# -------------------------------------------------------
class PriorityLevel(str, Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

class IssueCategory(str, Enum):
    POTHOLE = "Pothole"
    GRAFFITI = "Graffiti"
    TRASH = "Trash"
    STREET_LIGHT = "Street Light"
    OTHER = "Other"

# -------------------------------------------------------
# Request Models
# -------------------------------------------------------
class AssessPriorityRequest(BaseModel):
    description: str

# Note: /categorize accepts a raw file upload, so it doesn't use a Pydantic Request model.

# -------------------------------------------------------
# Response Models
# -------------------------------------------------------
class CategorizeResponse(BaseModel):
    category: IssueCategory
    confidence: float  # Good practice to include confidence score for AI models

class AssessPriorityResponse(BaseModel):
    priority: PriorityLevel
    reasoning: str  # Optional: explain why AI chose this priority