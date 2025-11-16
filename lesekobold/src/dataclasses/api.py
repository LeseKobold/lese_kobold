from enum import StrEnum

import pydantic
from src.dataclasses.story_model import LeveledStoryModel


class APIStatus(StrEnum):
    SUCCESS = "success"
    ERROR = "error"


class UserRequest(pydantic.BaseModel):
    """Request model for the API endpoints."""

    session_id: str | None = None
    user_id: str | None = None
    prompt: str


class APIResponse(pydantic.BaseModel):
    """Response model for the API endpoints."""

    session_id: str
    response_body: LeveledStoryModel | None = None
    status: APIStatus = APIStatus.SUCCESS
    error_message: str | None = None
