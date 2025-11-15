import pytest
from src.agent_manager import AgentManager
from src.dataclasses.agent_personas import pre_processing_agent_settings


@pytest.fixture
def agent_manager() -> AgentManager:
    return AgentManager(agent_settings=pre_processing_agent_settings)


@pytest.mark.unit_test
def test_agent_manager_build(agent_manager: AgentManager):
    import google.adk

    rval: google.adk.Agent | None = agent_manager.build()
    assert rval is not None
    assert isinstance(rval, google.adk.Agent)
