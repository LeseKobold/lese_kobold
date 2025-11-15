import pytest
from src.core.agent_manager import AgentManager, build_kobold_agent
from src.dataclasses.agent_personas import story_agent_settings


@pytest.fixture
def agent_manager() -> AgentManager:
    return AgentManager(agent_settings=story_agent_settings)


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
