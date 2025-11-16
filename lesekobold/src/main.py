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
import google.adk.runners
import google.genai.types

# import google.adk.cli.fast_api
import uvicorn
from src.config import app_config
from src.core.agent_manager import build_kobold_agent
from src.core.session_manager import SessionManager
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
logging.debug("Initialising services...")
session_service = SessionManager.get_session_service(API_NAME)
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

    session_id = session_service.get_or_create_session(
        request.user_id, request.session_id
    )
    logging.debug(
        f"Received generation request - "
        f"User ID: {request.user_id}, Session ID: {session_id}"
    )

    # Construct the message parts
    parts = [google.genai.types.Part.from_text(text=request.prompt)]
    # Associate the role with the message
    new_message = google.genai.types.Content(role="user", parts=parts)

    # Create the runner
    # TODO: move the runner out of this function
    runner = google.adk.runners.Runner(
        agent=build_kobold_agent(),
        app_name=API_NAME,
        session_service=session_service,
        artifact_service=None,  # TODO: add in memory artifact service
    )
    # Run the agent and extract response and attachments
    logging.debug(f"Running agent for session: {session_id}")
    final_msg = ""
    response_attachments: list[google.genai.types.Part] = []
    async for event in runner.run_async(
        user_id=request.user_id,
        session_id=session_id,
        new_message=new_message,
    ):
        if event.is_final_response() and event.content and event.content.parts:
            for part in event.content.parts:
                if part.text:
                    final_msg += part.text
                elif part.inline_data:  # Check for other types of parts (e.g., images)
                    response_attachments.append(part)

    logging.debug(f"Agent for session {session_id} finished.")
    logging.debug(f"Final message snippet: {final_msg[:100]}...")

    # TODO figure out if this is returning the response in the expected format
    return APIResponse(
        session_id=session_id,
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
