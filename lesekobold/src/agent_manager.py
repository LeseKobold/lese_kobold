# import google.adk

import logging

import google.adk
import google.adk.agents

from src.dataclasses.agent_settings import AgentSettings
from src.dataclasses.story_settings import content_agent_settings, style_agent_settings

logging.basicConfig(level=logging.ERROR)


class AgentManager:
    """
    Agent for story generation.
    """

    def __init__(self, agent_settings: AgentSettings):
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
                input_schema=self.agent_settings.input_schema,
                output_schema=self.agent_settings.output_schema,
                output_key=self.agent_settings.output_key,
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


@staticmethod
def build_story_agent() -> google.adk.agents.SequentialAgent:
    logging.info("Building story agent...")
    content_agent: google.adk.Agent | None = AgentManager(
        agent_settings=content_agent_settings
    ).build()
    if not content_agent:
        raise Exception("Failed to build content agent.")

    logging.info("Building style agent...")
    style_agent: google.adk.Agent | None = AgentManager(
        agent_settings=style_agent_settings
    ).build()
    if not style_agent:
        raise Exception("Failed to build style agent.")

    logging.info("Building story agent...")
    story_agent: google.adk.agents.SequentialAgent | None = (
        google.adk.agents.SequentialAgent(
            name="story_generation_agent",
            sub_agents=[content_agent, style_agent],
            description="Executes the content agent and then the style agent.",
        )
    )

    return story_agent
