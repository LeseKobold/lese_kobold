# import google.adk

import logging

import google.adk
import google.adk.models.lite_llm
from config import llm_config

logging.basicConfig(level=logging.ERROR)


class StoryAgent(google.adk.AgentTemplate):
    """
    Agent for story generation.
    """

    def __init__(self, name: str):
        super().__init__(name)

    def build(self) -> google.adk.Agent | None:
        try:
            # TODO check if this is valid
            model = google.adk.models.lite_llm.LiteLlm(
                model=f"openai/{llm_config.OPENAI_MODEL_NAME}"
            )
        except Exception as e:
            logging.error(
                f"Error creating model '{llm_config.OPENAI_MODEL_NAME}' due to: {e}"
            )
            return None

        # TODO: define agent settings and persona in a config file
        # TODO: move the prompts to a separate file and load them with jinja2
        try:
            rval = google.adk.Agent(
                name="story_agent_v1",
                model=model,  # Can be a string for Gemini or a LiteLlm object
                description="Generates stories based on a user's prompt.",
                instruction="You are a helpful story generator for educational children's stories. "
                "You create stories based on the content specified by the user. "
                "You then adjust the language and style of the story to make it more engaging and interesting for children. Make sure that the reading level is appropriate for the specified age group."
                "Write all stories in German.",
                # tools=[get_story],  # Pass the function directly
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
