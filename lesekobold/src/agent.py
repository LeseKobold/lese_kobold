# import google.adk

import logging

import google.adk

from src.agent_settings import AgentSettings, story_agent_settings

logging.basicConfig(level=logging.ERROR)


def get_lix_score(text: str) -> float: ...


class StoryAgent(google.adk.AgentTemplate):
    """
    Agent for story generation.
    """

    def __init__(self, agent_settings: AgentSettings = story_agent_settings):
        super().__init__()
        self.agent_settings = agent_settings

    def build(self) -> google.adk.Agent | None:
        """Builds the agent from the agent settings.

        Returns:
            The agent (google.adk.Agent) or None if the agent could not be created.
        """

        try:
            agent = google.adk.Agent(
                name=self.agent_settings.name,
                model=self.agent_settings.model,
                description=self.agent_settings.description,
                instruction=(self.agent_settings.instruction),
                tools=self.agent_settings.tools,
                generate_content_config=self.agent_settings.generate_content_config,
            )
        except Exception as e:
            logging.error(
                f"Error creating agent '{agent.name}' using model "
                f"'{self.agent_settings.model_provider}/{self.agent_settings.model_provider}' "
                f"due to error: {e}"
            )
            return None
        else:
            logging.info(
                f"Agent '{agent.name}' created using model "
                f"'{self.agent_settings.model_provider}/{self.agent_settings.model_name}'."
            )
        return agent


if __name__ == "__main__":
    print("Hello, world!")
