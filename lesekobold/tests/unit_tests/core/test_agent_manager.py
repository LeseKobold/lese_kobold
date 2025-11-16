import logging
import uuid

import google.adk.sessions
import google.genai.types
import pytest
from src.config import app_config
from src.core.agent_manager import AgentManager, build_kobold_agent
from src.dataclasses.agent_personas import content_agent_settings

logging.basicConfig(level=logging.DEBUG)


@pytest.fixture
def agent_manager() -> AgentManager:
    return AgentManager(agent_settings=content_agent_settings)


@pytest.mark.unit_test
def test_agent_manager_build(agent_manager: AgentManager):
    import google.adk

    rval: google.adk.Agent | None = agent_manager.build()
    assert rval is not None
    assert isinstance(rval, google.adk.Agent)


@pytest.mark.unit_test
def test_build_story_agent():
    import google.adk.agents

    rval: google.adk.agents.SequentialAgent | None = build_kobold_agent()
    assert rval is not None
    assert isinstance(rval, google.adk.agents.SequentialAgent)


@pytest.mark.unit_test
@pytest.mark.asyncio
async def test_kobold_agent():
    # Create the session service
    session_service = google.adk.sessions.InMemorySessionService()
    session_id = uuid.uuid4()
    user_id = uuid.uuid4()
    try:
        await session_service.create_session(
            app_name="agents",
            user_id=user_id,
            session_id=session_id,
        )
    except Exception as e:
        logging.error(f"Failed to create session: {e}")

    # Build the agent
    root_agent = build_kobold_agent()
    runner = google.adk.runners.Runner(
        agent=root_agent,
        app_name=app_config.APP_NAME,
        session_service=session_service,
    )

    query = "Write a story about a cat for grade 2."
    response_text = ""
    async for event in runner.run_async(
        user_id=user_id,
        session_id=session_id,
        new_message=google.genai.types.Content(
            role="user", parts=[google.genai.types.Part.from_text(text=query)]
        ),
    ):
        if event.is_final_response():
            if event.content and event.content.parts and len(event.content.parts) > 0:
                response_text = event.content.parts[0].text
                logging.debug(f"Response: {response_text}")
            else:
                response_text = ""
            break

    assert isinstance(response_text, str)
    assert len(response_text) > 0
    assert len(response_text) > 0
