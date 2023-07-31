from langchain import Agent

class CustomerServiceAgent(Agent):
    def __init__(self):
        super().__init__()
        self.prompt = "How can I help you with your customer service needs?"

    def speak(self, context):
        # Generate a response based on the context
        response = self.generate_response(context)
        return response
