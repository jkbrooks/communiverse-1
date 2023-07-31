from langchain import Agent

class GeneralAgent(Agent):
    def __init__(self):
        super().__init__()
        self.prompt = "How can I assist you today?"

    def speak(self, context):
        # Generate a response based on the context
        response = self.generate_response(context)
        return response
