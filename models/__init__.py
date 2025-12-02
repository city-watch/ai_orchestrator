from pydantic import BaseModel
from enum import Enum

# -------------------------------------------------------
# Enums (Strict Type Definitions)
# -------------------------------------------------------
class PriorityLevel(str, Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

# Removed IssueCategory Enum to allow for dynamic categories

# -------------------------------------------------------
# Request Models
# -------------------------------------------------------
class AssessPriorityRequest(BaseModel):
    description: str

# -------------------------------------------------------
# Response Models
# -------------------------------------------------------
class CategorizeResponse(BaseModel):
    category: str  # Changed from Enum to str to allow any value
    confidence: float

class AssessPriorityResponse(BaseModel):
    priority: PriorityLevel
    reasoning: str