import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock

from main import app, map_labels_to_category, determine_priority_from_text
from models import PriorityLevel

client = TestClient(app)

# -------------------------------------------------------
# Mock Data for Google Vision
# -------------------------------------------------------
class MockLabel:
    def __init__(self, description, score):
        self.description = description
        self.score = score

# -------------------------------------------------------
# Unit Tests for Helper Functions
# -------------------------------------------------------

def test_map_labels_to_category_pothole():
    labels = [MockLabel("road surface", 0.9), MockLabel("asphalt", 0.8)]
    category, confidence = map_labels_to_category(labels)
    assert category == "Pothole"
    assert confidence == 0.9

def test_map_labels_to_category_graffiti():
    labels = [MockLabel("wall", 0.95), MockLabel("spray paint", 0.85)]
    category, confidence = map_labels_to_category(labels)
    assert category == "Graffiti"
    assert confidence == 0.95

def test_map_labels_to_category_trash():
    labels = [MockLabel("plastic bag", 0.88), MockLabel("garbage", 0.8)]
    category, confidence = map_labels_to_category(labels)
    assert category == "Trash"
    assert confidence == 0.88

def test_map_labels_to_category_street_light():
    labels = [MockLabel("lamp", 0.92), MockLabel("street light", 0.9)]
    category, confidence = map_labels_to_category(labels)
    assert category == "Street Light"
    assert confidence == 0.92

def test_map_labels_to_category_dynamic_category():
    labels = [MockLabel("Tree", 0.99), MockLabel("Plant", 0.98)]
    category, confidence = map_labels_to_category(labels)
    assert category == "Tree"
    assert confidence == 0.99

def test_map_labels_to_category_no_labels():
    labels = []
    category, confidence = map_labels_to_category(labels)
    assert category == "Uncategorized"
    assert confidence == 0.0

def test_determine_priority_high():
    text = "There is a huge dangerous pothole and it's an urgent problem."
    priority, reason = determine_priority_from_text(text)
    assert priority == PriorityLevel.HIGH
    assert "urgent keywords" in reason

def test_determine_priority_medium():
    text = "This is a large and annoying crack in the sidewalk."
    priority, reason = determine_priority_from_text(text)
    assert priority == PriorityLevel.MEDIUM
    assert "moderate inconvenience" in reason

def test_determine_priority_low():
    text = "The grass is getting a little long in the park."
    priority, reason = determine_priority_from_text(text)
    assert priority == PriorityLevel.LOW
    assert "standard priority" in reason

# -------------------------------------------------------
# API Endpoint Tests
# -------------------------------------------------------

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Civic AI Orchestrator is running."}

def test_liveness_check():
    response = client.get("/health/live")
    assert response.status_code == 200
    assert response.json() == {"status": "alive"}

@patch('main.vision.ImageAnnotatorClient')
def test_categorize_issue_image_success(mock_vision_client):
    # Arrange
    mock_labels = [MockLabel("pothole", 0.95)]
    mock_response = MagicMock()
    mock_response.label_annotations = mock_labels
    mock_response.error.message = ""
    
    mock_vision_instance = MagicMock()
    mock_vision_instance.label_detection.return_value = mock_response
    mock_vision_client.return_value = mock_vision_instance

    # Act
    with open("test_image.jpg", "wb") as f:
        f.write(b"fake image data")

    with open("test_image.jpg", "rb") as f:
        response = client.post("/internal/ai/categorize", files={"file": ("test_image.jpg", f, "image/jpeg")})

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data["category"] == "Pothole"
    assert data["confidence"] == 0.95

@patch('main.vision.ImageAnnotatorClient')
def test_categorize_issue_image_vision_api_error(mock_vision_client):
    # Arrange
    mock_response = MagicMock()
    mock_response.error.message = "Test API Error"
    
    mock_vision_instance = MagicMock()
    mock_vision_instance.label_detection.return_value = mock_response
    mock_vision_client.return_value = mock_vision_instance

    # Act
    with open("test_image.jpg", "wb") as f:
        f.write(b"fake image data")

    with open("test_image.jpg", "rb") as f:
        response = client.post("/internal/ai/categorize", files={"file": ("test_image.jpg", f, "image/jpeg")})

    # Assert
    assert response.status_code == 500
    assert "Google Vision API Error: Test API Error" in response.json()["detail"]

def test_assess_issue_priority_high():
    response = client.post("/internal/ai/assess-priority", json={"description": "A fire is blocking the road."})
    assert response.status_code == 200
    data = response.json()
    assert data["priority"] == "high"
    assert "urgent keywords" in data["reasoning"]

def test_assess_issue_priority_low():
    response = client.post("/internal/ai/assess-priority", json={"description": "A branch fell on the sidewalk."})
    assert response.status_code == 200
    data = response.json()
    assert data["priority"] == "low"
    assert "standard priority" in data["reasoning"]

# Cleanup the test image
import os
if os.path.exists("test_image.jpg"):
    os.remove("test_image.jpg")
