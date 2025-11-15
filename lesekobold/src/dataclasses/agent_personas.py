from src.config import llm_config
from src.core.prompt_reader import load_prompt
from src.dataclasses.agent_settings import AgentSettings
from src.dataclasses.story_model import (
    StorySpecificationModel,
    StyleInputModel,
    StyleOutputModel,
)

# TODO: move the prompts to a separate file and load them with jinja2
story_agent_settings = AgentSettings(
    name="story_orchestrator",
    model_name=llm_config.OPENAI_MODEL_NAME,
    model_provider="openai",
    instruction=load_prompt("story_prompt.md"),
    description="Generates stories based on a user's prompt.",
    tools=[],
    temperature=1.0,
    # max_output_tokens=10_000,  # TODO: get a reasonable limit
)

content_agent_settings = AgentSettings(
    name="content_agent",
    model_name=llm_config.OPENAI_MODEL_NAME,
    model_provider="openai",
    instruction=load_prompt("story_prompt.md"),
    description="Generates a story outline and character descriptions based on a user's prompt.",
    tools=[],
    temperature=1.0,
    input_schema=StorySpecificationModel,
    output_schema=StyleInputModel,
    output_key="content",
    # max_output_tokens=10_000,  # TODO: get a reasonable limit
)

style_agent_settings = AgentSettings(
    name="style_agent",
    model_name=llm_config.OPENAI_MODEL_NAME,
    model_provider="openai",
    instruction=load_prompt("style_prompt.md"),
    description="Generates a style for the story a story outline and character descriptions.",
    tools=[],
    temperature=1.0,
    input_schema=StyleInputModel,
    output_schema=StyleOutputModel,
    output_key="style",
)


pre_processing_agent_settings = AgentSettings(
    name="pre_processing_agent_v1",
    model_name=llm_config.OPENAI_MODEL_NAME,
    model_provider="openai",
    instruction=load_prompt("preprocessing_prompt.md"),
    description="Generates a story specification from a free user input.",
    tools=[],
    temperature=1.0,
    output_schema=StorySpecificationModel,
    output_key="story_specification",
)
