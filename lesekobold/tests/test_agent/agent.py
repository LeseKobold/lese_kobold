import sys
from pathlib import Path

# Add the package root to sys.path so we can import from src
# NOTE: Imports must come after sys.path modification
package_root = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(package_root))

from src.agent_manager import build_kobold_agent  # noqa: E402
from src.config import llm_config  # noqa: E402

# Step 1: Make sure that the environment variables are loaded
assert llm_config.OPENAI_API_KEY is not None
assert llm_config.OPENAI_MODEL_NAME is not None

root_agent = build_kobold_agent()
