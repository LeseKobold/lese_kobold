from src.config import llm_config
from src.core.prompt_reader import load_prompt
from src.core.readability_utils import get_grade_level
from src.core.readability_utils import ReadabilityUtils
from src.dataclasses.agent_settings import AgentSettings
from src.dataclasses.story_model import (
    LeveledStoryModel,
    StoryModel,
    StorySpecificationModel,
    JudgeOutputModel,
)
from src.core.readability_utils import (
    calculate_lix_score,
    get_text_is_covered_by_basic_vocab,
    get_basic_vocab_coverage,
)

ru = ReadabilityUtils()

content_agent_settings = AgentSettings(
    name="content_agent",
    model_name=llm_config.OPENAI_MODEL_NAME,
    model_provider="openai",
    instruction=load_prompt("story_prompt.md"),
    description="Generates a story outline and character descriptions based on a user's prompt.",
    tools=[],
    temperature=1.0,
    input_schema=StorySpecificationModel,
    output_schema=StoryModel,
    output_key="content",
)

style_agent_settings = AgentSettings(
    name="style_agent",
    model_name=llm_config.OPENAI_MODEL_NAME,
    model_provider="openai",
    instruction=load_prompt(
        prompt_name="style_prompt.md",
        variables={
            "get_grade_level": get_grade_level.__name__,
            "get_basic_vocab_coverage": ru.get_basic_vocab_coverage.__name__,
        },
    ),
    description="Generates a style for the story a story outline and character descriptions.",
    tools=[get_grade_level, ru.get_basic_vocab_coverage],
    temperature=1.0,
    input_schema=StoryModel,
    output_schema=LeveledStoryModel,
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

judge_agent_settings = AgentSettings(
    name="judge_agent_v1",
    model_name=llm_config.OPENAI_MODEL_NAME,
    model_provider="openai",
    instruction=load_prompt(
        prompt_name="judge_prompt.md",
        variables={
            "get_grade_level": get_grade_level.__name__,
            "get_text_is_covered_by_basic_vocab": get_text_is_covered_by_basic_vocab.__name__,
            "get_lix_score": calculate_lix_score.__name__,
            "get_basic_vocab_coverage": get_basic_vocab_coverage.__name__,
        },
    ),
    description="Judges the generated story and either triggers a story refinement or forwards the story to the user.",
    tools=[
        get_grade_level,
        get_text_is_covered_by_basic_vocab,
        calculate_lix_score,
        get_basic_vocab_coverage,
    ],
    temperature=1.0,
    input_schema=LeveledStoryModel,
    output_schema=JudgeOutputModel,
    output_key="judge_output",
)
