# Civic AI Orchestrator

The Civic AI Orchestrator is a FastAPI-based service that provides AI-powered capabilities for civic issue reporting and management. It's designed to analyze citizen reports, categorize issues, and assess their priority.

## Features

*   **Issue Categorization**: Analyzes images to determine the type of issue (e.g., Pothole, Graffiti).
*   **Priority Assessment**: Determines the urgency of an issue based on its description.
*   **Health Checks**: Liveness and readiness probes to ensure service reliability.

## API Endpoints

*   `GET /`: Root endpoint, returns a welcome message.
*   `GET /health/live`: Liveness probe.
*   `GET /health/ready`: Readiness probe.
*   `POST /internal/ai/categorize`: Upload an image to categorize the issue.
*   `POST /internal/ai/assess-priority`: Submit a description to assess the issue's priority.

## Getting Started

### Prerequisites

*   Python 3.8+
*   Pip

### Installation

1.  Clone the repository:
    ```bash
    git clone https://github.com/your-username/ai_orchestrator.git
    cd ai_orchestrator
    ```
2.  Install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```

### Running the Service

Use Uvicorn to run the FastAPI application:

```bash
uvicorn main:app --reload
```

The application will be available at `http://127.0.0.1:8000`.

## Project Structure

```
.
├── main.py             # FastAPI application, endpoints
├── models/__init__.py  # Pydantic models for requests/responses
├── requirements.txt    # Python dependencies
└── README.md           # This file
```
