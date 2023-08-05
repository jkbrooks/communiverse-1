from langchain.schema import (
    HumanMessage,
    SystemMessage,
    BaseMessage,
)

from workspace.user import User
from typing import Any

class DialogueAgent:
    def __init__(
        self,
        name: str,
        id: int,
        system_message: SystemMessage,
        model: Any,
        user: User,
        version: float
    ) -> None:
        self.name = name
        self.id = id
        self.system_message = system_message
        self.model = model
        self.user = user
        self.version = version

        self.prefix = f"{self.name}: "
        self.reset()
    
    def reset(self):
        self.message_history = ["Here is the conversation so far."]
    
    def send(self) -> str:
        """
        Applies the chatmodel to the message history
        and returns the message string
        """
        message = self.model(
            [
                self.system_message,
                HumanMessage(content="\n".join(self.message_history + [self.prefix])),
            ]
        )
        return message.content
    
    def set_history(self, history: list) -> None:
        self.message_history = history
    
    def receive(self, name: str, message: str) -> None:
        """
        Concatenates {message} spoken by {name} into message history
        """
        self.message_history.append(f"{name}: {message}")
        
        with open('conversation.txt', 'a') as f:
            f.write("New iteration\n")
            for line in self.message_history:
                f.write(f"{line}\n")

            f.write("\n\n")