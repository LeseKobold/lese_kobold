import src.config as llm_config
from src.agent_manager import AgentManager
from src.agent_settings import story_agent_settings

# Step 1: Make sure that the environment variables are loaded
assert llm_config.OPENAI_API_KEY is not None
assert llm_config.OPENAI_MODEL_NAME is not None

agent_manager = AgentManager(agent_settings=story_agent_settings)
root_agent = agent_manager.build()
