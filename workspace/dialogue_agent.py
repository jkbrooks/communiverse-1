from langchain.schema import (
    HumanMessage,
    SystemMessage,
    BaseMessage,
)
from langchain import PromptTemplate
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
        version: float,
        bidding_template: str,
        stage_template = None
    ) -> None:
        self.name = name
        self.id = id
        self.system_message = system_message
        self.model = model
        self.user = user
        self.version = version
        self.bidding_template = bidding_template
        self.stage_template = stage_template

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

    def generate_template_for_stage():
        pass

    def get_stage(self):
        """
        Asks the chat model to output the stage of his algorithm
        """
        if self.name == 'Action Plan Proposer':
            prompt = PromptTemplate(input_variables=['message_history'], 
                                    template=self.stage_template).format(message_history="\n".join(self.message_history))
    
        stage_string = self.model([SystemMessage(content=prompt)]).content
        return stage_string

    def bid(self) -> str:
        """
        Asks the chat model to output a bid to speak
        """
        prompt = PromptTemplate(
            input_variables=["message_history", "recent_message"],
            template=self.bidding_template,
        ).format(
            message_history="\n".join(self.message_history),
            recent_message=self.message_history[-1],
        )
        bid_string = self.model([SystemMessage(content=prompt)]).content
        return bid_string