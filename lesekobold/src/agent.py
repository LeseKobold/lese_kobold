# import google.adk

import logging

import google.adk
import litellm
from config import llm_config

logging.basicConfig(level=logging.ERROR)


class StoryAgent(google.adk.AgentTemplate):
    """
    Agent for story generation.
    """

    def __init__(self, name: str):
        super().__init__(name)

    def build(self) -> google.adk.Agent:
        # TODO figure out how to use the model from litellm
        model = litellm.completion(llm_config.MODEL_NAME)

        # TODO: move the prompts to a separate file and load them with jinja2
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
        logging.info(
            f"Agent '{rval.name}' created using model '{llm_config.MODEL_NAME}'."
        )
        return rval


def main():
    return litellm.completion(
        model=llm_config.MODEL_NAME,
        messages=[{"content": "Hello, how are you?", "role": "user"}],
    )


if __name__ == "__main__":
    response = main()
    print(response)
