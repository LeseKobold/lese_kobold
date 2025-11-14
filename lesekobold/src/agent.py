import adk


class Agent(adk.Agent):
    def __init__(self, name: str):
        super().__init__(name)

    def run(self):
        print(f"Running {self.name}")
