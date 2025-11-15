import logging
import typing

import google.adk.models.lite_llm
import google.genai.types
import pydantic

logging.basicConfig(level=logging.ERROR)


class AgentSettings(pydantic.BaseModel):
    name: str
    model_name: str
    instruction: str
    description: str
    tools: list[typing.Callable]
    model_provider: str
    temperature: float = 1.0
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
