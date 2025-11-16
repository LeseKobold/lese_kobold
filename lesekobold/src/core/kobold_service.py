# This is the agent script
# TODO: add session management
# - https://github.com/google/adk-docs/blob/main/examples/python/agent-samples/youtube-shorts-assistant/agent.py
# - https://google.github.io/adk-docs/tutorials/agent-team/#step-1-your-first-agent-basic-weather-lookup
# TODO: move into a ADKAPp class?

import logging

import google.adk
import google.adk.runners
import google.genai.types
from src.core.agent_manager import build_kobold_agent  # noqa: E402
from src.core.session_manager import SessionManager

logging.basicConfig(level=logging.ERROR)


class KoboldService:
    """Service for running the Kobold story generation agent."""

    def __init__(self, name: str):
        self.name = name

        # Get the session manager and create a session service instance
        try:
            self.session_manager: SessionManager = SessionManager.get_session_service(
                app_name=name
            )
        except Exception as e:
            logging.error(
                f"Failed to get session manager for service '{name}' due to error: {e}"
            )
            raise e

        # Build the agent
        try:
            self.agent = build_kobold_agent()
        except Exception as e:
            logging.error(
                f"Failed to build kobold agent for service '{name}' due to error: {e}"
            )
            raise e

        # Build the agent runner
        try:
            self.runner = google.adk.runners.Runner(
                agent=self.agent,
                app_name=self.name,
                session_service=self.session_manager.session_service,
                artifact_service=None,  # TODO: add in memory artifact service
            )
        except Exception as e:
            logging.error(
                f"Failed to build runner for service '{name}' due to error: {e}"
            )
            raise e

    async def run(
        self, prompt: str, user_id: str, session_id: str | None = None
    ) -> tuple[str, list[google.genai.types.Part]]:
        """Run the story generation service."""

        # Step 1: Get or create the session
        session = await self.session_manager.get_or_create_session(
            user_id=user_id, session_id=session_id
        )
        if not session:
            raise Exception(
                f"Failed to run story generation service: Failed to get or create session for user '{user_id if user_id else 'unknown'}'."
            )

        # Step 2: Get the prompt into the correct format
        parts = [google.genai.types.Part.from_text(text=prompt)]
        new_message = google.genai.types.Content(role="user", parts=parts)

        # Step 3: Run the agent
        final_msg, response_attachments = await self._run(
            user_id=user_id, session_id=session.id, message=new_message
        )
        return final_msg, response_attachments

    async def _run(
        self, user_id: str, session_id: str, message: google.genai.types.Content
    ) -> tuple[str, list[google.genai.types.Part]]:
        logging.debug(
            f"Running agent '{self.name}' "
            f"for user '{user_id}' and session '{session_id}'"
        )

        final_msg = ""
        response_attachments: list[google.genai.types.Part] = []
        async for event in self.runner.run_async(
            user_id=user_id,
            session_id=session_id,
            new_message=message,
        ):
            if event.is_final_response() and event.content and event.content.parts:
                for part in event.content.parts:
                    if part.text:
                        final_msg += part.text
                    elif (
                        part.inline_data
                    ):  # Check for other types of parts (e.g., images)
                        response_attachments.append(part)
                    elif (
                        part.inline_data
                    ):  # Check for other types of parts (e.g., images)
                        response_attachments.append(part)
        return final_msg, response_attachments
