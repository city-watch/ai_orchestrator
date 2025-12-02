# Civic AI Orchestrator

The Civic AI Orchestrator is a FastAPI-based service that provides AI-powered capabilities for civic issue reporting and management. It's designed to analyze citizen reports, categorize issues, and assess their priority.

## Features

*   **Issue Categorization**: Analyzes images to determine the type of issue (e.g., Pothole, Graffiti) using Google Cloud Vision.
*   **Priority Assessment**: Determines the urgency of an issue based on its description text.
*   **Health Checks**: Liveness probes to ensure service reliability.

## Getting Started

### Prerequisites

*   Python 3.8+
*   Pip
*   A Google Cloud Platform (GCP) project with the **Cloud Vision API** enabled.
*   A GCP service account key file (`.json`) with permissions to use the Vision API.

### 1. Installation

1.  Clone the repository:
    ```bash
    git clone https://github.com/your-username/ai_orchestrator.git
    cd ai_orchestrator
    ```
2.  Create a virtual environment and activate it:
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```
3.  Install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```

### 2. Configuration

This service requires Google Cloud credentials to be configured in your local environment.

1.  **Place your GCP Key**: Move your downloaded GCP service account JSON key file into the root of this project and **rename it to `gcp_key.json`**.

2.  **Create a `.env` file**: Create a file named `.env` in the project root. This file will store the path to your credentials, which the application loads at runtime.

3.  **Add the following content** to the `.env` file. This tells the application where to find the key.
    ```env
    # .env
    GOOGLE_APPLICATION_CREDENTIALS=gcp_key.json
    ```
    
    > **Note**: The `.gitignore` file is already configured to ignore `.env` and `gcp_key.json` files, so your credentials will not be committed to your repository.

### 3. Running the Service

With your virtual environment activated and your `.env` file created, use Uvicorn to run the FastAPI application:

```bash
uvicorn main:app --reload
```

The application will be available at `http://127.0.0.1:8000`. You can access the interactive API documentation at `http://127.0.0.1:8000/docs`.

## API Endpoints

*   `GET /`: Root endpoint, returns a welcome message.
*   `GET /health/live`: Liveness probe.
*   `POST /internal/ai/categorize`: Upload an image to categorize the issue.
*   `POST /internal/ai/assess-priority`: Submit a description to assess the issue's priority.

## Project Structure

```
.
├── .env                # Local environment variables (YOU CREATE THIS)
├── gcp_key.json        # GCP service account key (YOU PROVIDE THIS)
├── main.py             # FastAPI application, endpoints
├── models/__init__.py  # Pydantic models for requests/responses
├── requirements.txt    # Python dependencies
└── README.md           # This file
```