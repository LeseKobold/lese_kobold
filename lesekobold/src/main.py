import os

import fastapi

# import google.adk.cli.fast_api
import uvicorn

# Get the directory where main.py is located
AGENT_DIR = os.path.dirname(os.path.abspath(__file__))  # FIXME: add agent directory

# Example allowed origins for CORS
ALLOWED_ORIGINS = ["http://localhost", "http://localhost:8080", "*"]

# Set web=True if you intend to serve a web interface, False otherwise
SERVE_WEB_INTERFACE = True

# Call the function to get the FastAPI app instance
# Ensure the agent directory name ('capital_agent') matches your agent folder
# app: fastapi.FastAPI = google.adk.cli.fast_api.get_fast_api_app(
#    agents_dir=AGENT_DIR,
#    # session_service_uri=SESSION_SERVICE_URI, # FIXME: add in memory session service
#    allow_origins=ALLOWED_ORIGINS,
#    web=SERVE_WEB_INTERFACE,
# )
app: fastapi.FastAPI = fastapi.FastAPI()


# You can add more FastAPI routes or configurations below if needed
# Example:
@app.get("/health")
async def health_check():
    return {"status": "ok"}


@app.get("/")
def read_root():
    """Root endpoint for the API."""
    return {"greeting": "Hello, World!"}


if __name__ == "__main__":
    # Use the PORT environment variable provided by Cloud Run, defaulting to 8080
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
