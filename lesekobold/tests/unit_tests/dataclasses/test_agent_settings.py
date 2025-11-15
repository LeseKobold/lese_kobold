import pytest
from src.config import llm_config
from src.dataclasses.agent_settings import AgentSettings


@pytest.fixture
def agent_settings() -> AgentSettings:
    return AgentSettings(
        name="test_agent",
        model_name=llm_config.OPENAI_MODEL_NAME,
        model_provider="openai",
        instruction="foo",
        description="bar",
        tools=[],
        temperature=0.5,
        max_output_tokens=10,
    )


@pytest.mark.unit_test
def test_agent_settings__model(agent_settings: AgentSettings):
    from google.adk.models.lite_llm import LiteLlm

    assert agent_settings.model is not None
    assert isinstance(agent_settings.model, LiteLlm)


@pytest.mark.unit_test
def test_agent_settings__generate_content_config(agent_settings: AgentSettings):
    import google.genai.types

    assert agent_settings.generate_content_config is not None
    assert isinstance(
        agent_settings.generate_content_config, google.genai.types.GenerateContentConfig
    )
