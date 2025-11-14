# import google.adk
import litellm

# class Agent(google.adk.Agent):
#    def __init__(self, name: str):
#        super().__init__(name)
#
#    def run(self):
#        print(f"Running {self.name}")


def main():
    return litellm.completion(
        model="gpt-3.5-turbo",
        messages=[{"content": "Hello, how are you?", "role": "user"}],
    )


if __name__ == "__main__":
    response = main()
    print(response)
