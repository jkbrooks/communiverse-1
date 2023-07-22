from general_agent import GeneralAgent
from technical_agent import TechnicalAgent
from customer_service_agent import CustomerServiceAgent

class DialogueSimulator:
    def __init__(self):
        self.general_agent = GeneralAgent()
        self.technical_agent = TechnicalAgent()
        self.customer_service_agent = CustomerServiceAgent()

    def start_conversation(self):
        # Start the conversation loop
        context = ""
        while True:
            context = self.general_agent.speak(context)
            context = self.technical_agent.speak(context)
            context = self.customer_service_agent.speak(context)
