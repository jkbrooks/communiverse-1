from langchain import Agent

class TechnicalAgent(Agent):
    def __init__(self):
        super().__init__()
        self.prompt = "What technical issue are you facing?"

    def speak(self, context):
        # Generate a response based on the context
        response = self.generate_response(context)
        return response
