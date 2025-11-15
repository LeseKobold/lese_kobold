# This is the agent script
# TODO: add session management
# - https://github.com/google/adk-docs/blob/main/examples/python/agent-samples/youtube-shorts-assistant/agent.py
# - https://google.github.io/adk-docs/tutorials/agent-team/#step-1-your-first-agent-basic-weather-lookup
# TODO: move into a ADKAPp class?

import logging
import uuid

import google.adk
import google.adk.sessions
from google.adk.sessions import InMemorySessionService

from src.config import llm_config  # noqa: E402
from src.core.agent_manager import AgentManager  # noqa: E402
from src.dataclasses.agent_settings import story_agent_settings  # noqa: E402

logging.basicConfig(level=logging.ERROR)


class KoboldApp(google.adk.App):
    def __init__(self):
        self.name = "KoboldApp"
        self.session_service = InMemorySessionService()

        self.agent = AgentManager(agent_settings=story_agent_settings).build()

    async def run(self, user_id: str, session_id: str | None = None) -> None:
        """Run the app."""
        session = await self.get_or_create_session(
            user_id=user_id, session_id=session_id
        )
        if not session:
            raise Exception(
                f"Failed to run app: Failed to get or create session for user '{user_id}'."
            )
        self._run(user_id=user_id, session_id=session.id)

    async def get_or_create_session(
        self, user_id: str, session_id: str | None = None
    ) -> google.adk.sessions.Session | None:
        """Get or create a session for the user."""

        if not session_id:
            # Create a new session
            try:
                session_id = uuid.uuid4()
                new_session: google.adk.sessions.Session = (
                    self.session_service.create_session(
                        app_name=self.name,  # Use the consistent app name
                        user_id=user_id,
                        session_id=session_id,
                        state={},  # <<< Initialize state during creation
                    )
                )
            except Exception as e:
                logging.error(
                    f"Failed to create new session for user '{user_id}' "
                    f"for app '{self.name}' due to error: {e}"
                )
                return None
            logging.info(
                f"Created session '{new_session.id}' "
                f"for user '{new_session.user_id}' "
                f"for app '{new_session.app_name}'."
            )

        # Get an existing session (and check that creation was successful)
        try:
            session: google.adk.sessions.Session = (
                await self.session_service.get_session(
                    app_name=self.name,
                    user_id=user_id,
                    session_id=session_id,
                )
            )
        except Exception as e:
            logging.error(
                f"Failed to retrieve session '{session_id}' "
                f"for user '{user_id}' "
                f"for app '{self.name}' due to error: {e}"
            )
            return None
        logging.info(
            f"Retrieved session '{session.id}' "
            f"for user '{session.user_id}' "
            f"for app '{session.app_name}'."
        )
        return session

    def _run(self, user_id: str, session_id: str): ...


# Step 1: Make sure that the environment variables are loaded
assert llm_config.OPENAI_API_KEY is not None
assert llm_config.OPENAI_MODEL_NAME is not None

root_agent = AgentManager(agent_settings=story_agent_settings).build()
