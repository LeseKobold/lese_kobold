"""Lesekobold ADK/FastAPI Application

This module defines the main FastAPI application for the Lesekobold project.
It serves as the API layer, providing two endpoints for interacting with
the Lesekobold agent:
- `/api/latest/chat`: Interactive chat with the Lesekobold agent.
- `/api/latest/generate`: Generate a story based on the user's request.

Key functionalities include:
- Initializing ADK services (InMemorySessionService, InMemoryArtifactService).
- Orchestrating agent interactions using the ADK Runner.
- Managing conversational sessions.
- Returning story responses.

NOTE: We plan to extend this to support multimodal input (text AND images).

Reference:
https://medium.com/google-cloud/get-schwifty-with-the-fastapi-adding-a-rest-api-to-our-agentic-application-with-google-adk-6b87a4ea7567
"""

import logging
import os

import fastapi

# import google.adk.cli.fast_api
import uvicorn
from src.config import app_config
from src.core.kobold_service import KoboldService
from src.dataclasses.api import APIResponse, APIStatus, UserRequest

logging.basicConfig(level=logging.DEBUG)

API_NAME = f"{app_config.APP_NAME}_api"

# Example allowed origins for CORS
# ALLOWED_ORIGINS = ["http://localhost", "http://localhost:8080", "*"]

# Set web=True if you intend to serve a web interface, False otherwise
# SERVE_WEB_INTERFACE = True

# Call the function to get the FastAPI app instance
# Ensure the agent directory name ('capital_agent') matches your agent folder
# app: fastapi.FastAPI = google.adk.cli.fast_api.get_fast_api_app(
#    agents_dir=AGENT_DIR,
#    # session_service_uri=SESSION_SERVICE_URI, # FIXME: add in memory session service
#    allow_origins=ALLOWED_ORIGINS,
#    web=SERVE_WEB_INTERFACE,
# )

logging.debug("Initialising FastAPI app...")
app: fastapi.FastAPI = fastapi.FastAPI()
# TODO: use the google adk cli to get the fast api app

# Initialize services and runner on startup
logging.debug("Initialising Kobold runner...")
kobold_service = KoboldService(name=f"{app_config.APP_NAME}_service")
# artifact_service = get_artifact_service() # FIXME: add in memory artifact service


# You can add more FastAPI routes or configurations below if needed
# Example:
@app.get("/health")
async def health_check():
    return {"status": "ok"}


@app.get("/")
def read_root():
    """Root endpoint for the API."""
    return {"greeting": "Hello, World!"}


@app.post("/api/latest/chat")
async def chat_with_kobold(request: UserRequest) -> APIResponse:
    """Chat endpoint to interactively generate a story with the Kobold."""
    return APIResponse(
        session_id=request.session_id,
        response_body=None,
        status=APIStatus.ERROR,
        error_message="Not implemented",
    )


@app.post("/api/latest/generate")
async def generate_story(request: UserRequest) -> APIResponse:
    """Generation endpoint to generate a story based on the user's request."""

    logging.debug(
        f"Received generation request - "
        f"User ID: {request.user_id if request.user_id else 'unknown'}, "
        f"Session ID: {request.session_id if request.session_id else 'unknown'}"
    )

    # Run the agent and extract response and attachments
    try:
        final_msg, response_attachments = await kobold_service.run(
            prompt=request.prompt,
            user_id=request.user_id,
            session_id=request.session_id,
        )
    except Exception as e:
        return APIResponse(
            session_id=request.session_id,
            response_body=None,
            status=APIStatus.ERROR,
            error_message=f"Failed to generate story: {e}",
        )

    # TODO make sure that the response body is in the expected format and can be parsed successfully into the required pydantic model
    return APIResponse(
        session_id=request.session_id,
        response_body=final_msg,
        status=APIStatus.SUCCESS,
        error_message=None,
    )


if __name__ == "__main__":
    # Use the PORT environment variable provided by Cloud Run, defaulting to 8080
    uvicorn.run(
        app=app,
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 8080)),
        app_dir=str(app_config.APP_PATH),  # Get the directory where main.py is located
    )
