
class ConversationMemory:
    def __init__(self):
        self.memory = []

    def add(self, message):
        self.memory.append(message)

    def get_history(self):
        return self.memory