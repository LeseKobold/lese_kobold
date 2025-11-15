import logging
import typing

import google.adk.models.lite_llm
import google.genai.types
import pydantic

from src.config import llm_config

logging.basicConfig(level=logging.ERROR)


class AgentSettings(pydantic.BaseModel):
    name: str
    model_name: str
    instruction: str
    description: str
    tools: list[typing.Callable]
    model_provider: str
    temperature: float = 2.0
    max_output_tokens: int | None = None

    _model: google.adk.models.lite_llm.LiteLlm | None = None

    def model_post_init(self, context: typing.Any) -> None:
        self._init_model()

    def _init_model(self) -> None:
        try:
            self._model = google.adk.models.lite_llm.LiteLlm(
                model=f"{self.model_provider}/{self.model_name}"
            )
        except Exception as e:
            logging.error(f"Error creating model '{self.model_name}' due to: {e}")
            raise e

    @property
    def model(self) -> google.adk.models.lite_llm.LiteLlm:
        if self._model is None:
            self._init_model()
        return self._model

    @property
    def generate_content_config(self) -> google.genai.types.GenerateContentConfig:
        return google.genai.types.GenerateContentConfig(
            temperature=self.temperature,
            max_output_tokens=self.max_output_tokens,
        )


# TODO: move the prompts to a separate file and load them with jinja2
# TODO: use the prompt from resources/prompt
story_agent_settings = AgentSettings(
    name="story_agent_v1",
    model_name=llm_config.OPENAI_MODEL_NAME,
    model_provider="openai",
    instruction="You are a helpful story generator for educational children's stories. You create stories based on the content specified by the user. You then adjust the language and style of the story to make it more engaging and interesting for children. Make sure that the reading level is appropriate for the specified age group. Write all stories in German.",
    description="Generates stories based on a user's prompt.",
    tools=[],
)
