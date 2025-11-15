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
    input_schema: typing.Type[pydantic.BaseModel] | None = None
    output_schema: typing.Type[pydantic.BaseModel] | None = None
    output_key: str | None = None

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


pre_processing_agent_settings = AgentSettings(
    name="pre_processing_agent_v1",
    model_name=llm_config.OPENAI_MODEL_NAME,
    model_provider="openai",
    instruction="""Convert the input into a single, JSON object with exactly three fields: content, style and appropriate read level (grade level).
- content: all story information, exactly like the input, dont actually generate a story.
- style: story metadata, only a string
- level: integer

Do not include any extra fields, arrays, or nested objects. Output must be exactly:
{"content": "...", "style": "...", "level": "..."}""",
    description="Generates a JSON object string for further processing.",
    tools=[],
    temperature=1.0,
    # max_output_tokens=10_000,  # TODO: get a reasonable limit
)
