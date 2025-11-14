# import google.adk
import litellm
from config import llm_config

# class Agent(google.adk.Agent):
#    def __init__(self, name: str):
#        super().__init__(name)
#
#    def run(self):
#        print(f"Running {self.name}")


def main():
    return litellm.completion(
        model=llm_config.MODEL_NAME,
        messages=[{"content": "Hello, how are you?", "role": "user"}],
    )


if __name__ == "__main__":
    response = main()
    print(response)
