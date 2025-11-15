import os
import pathlib
import typing

import pydantic
import pydantic_settings


def get_root_path() -> pathlib.Path:
    current = pathlib.Path(__file__).resolve().parent
    while not (current / "pyproject.toml").exists() and current != current.parent:
        current = current.parent
    return current

class AppConfig(pydantic_settings.BaseSettings):
    PROCESS_ID: int = os.getpid()
    ROOT_PATH: pathlib.Path = get_root_path()
    APP_PATH: pathlib.Path = ROOT_PATH / "lesekobold"
    RESOURCES_PATH: pathlib.Path = APP_PATH / "resources"
    STORIES_PATH: pathlib.Path = RESOURCES_PATH / "stories"
    APP_VERSION: str = "0.1.0"  # TODO: Get from pyproject.toml


app_config = AppConfig()


class LLMConfig(pydantic_settings.BaseSettings):
    OPENAI_API_KEY: pydantic.SecretStr
    OPENAI_MODEL_NAME: str = "gpt-5-nano"

    model_config = pydantic_settings.SettingsConfigDict(
        env_file=app_config.ROOT_PATH / ".env", env_file_encoding="utf-8"
    )

    def model_post_init(self, context: typing.Any) -> None:
        # NOTE: this should not be needed,
        # but for some local envs it does not get loaded automatically
        os.environ["OPENAI_API_KEY"] = self.OPENAI_API_KEY.get_secret_value()


llm_config = LLMConfig()
