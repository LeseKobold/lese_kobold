# import google.adk

import logging

import google.adk
import google.genai.types
from config import llm_config

from src.agent_settings import AgentSettings

logging.basicConfig(level=logging.ERROR)


def get_lix_score(text: str) -> float: ...


class StoryAgent(google.adk.AgentTemplate):
    """
    Agent for story generation.
    """

    def __init__(self, name: str):
        super().__init__(name)

    def build(self, agent_settings: AgentSettings) -> google.adk.Agent | None:
        """Builds an agent from the given agent settings.

        Args:
            agent_settings (AgentSettings): The settings for the agent.

        Returns:
            The agent (google.adk.Agent) or None if the agent could not be created.
        """
        # TODO: move the prompts to a separate file and load them with jinja2
        # TODO: use the prompt from resources/prompt
        try:
            rval = google.adk.Agent(
                name=agent_settings.name,
                model=agent_settings.model,
                description=agent_settings.description,
                instruction=(agent_settings.instruction),
                tools=agent_settings.tools,
                generate_content_config=agent_settings.generate_content_config,
            )
        except Exception as e:
            logging.error(
                f"Error creating agent '{rval.name}' using model "
                f"'{llm_config.OPENAI_MODEL_NAME}' due to: {e}"
            )
            return None
        else:
            logging.info(
                f"Agent '{rval.name}' created using model '{llm_config.OPENAI_MODEL_NAME}'."
            )
        return rval


if __name__ == "__main__":
    print("Hello, world!")
