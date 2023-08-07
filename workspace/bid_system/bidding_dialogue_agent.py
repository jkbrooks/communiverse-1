from langchain.schema import SystemMessage
from langchain import PromptTemplate
from typing import Any
from workspace.user import User

from workspace.dialogue_agent import DialogueAgent

class BiddingDialogueAgent(DialogueAgent):
    def __init__(
        self,
        name,
        id,
        system_message: SystemMessage,
        bidding_template: PromptTemplate,
        model: Any,
        user: User,
        version: float
    ) -> None:
        super().__init__(name, id, system_message, model, user, version)
        self.bidding_template = bidding_template
    
    
    def bid(self) -> str:
        """
        Asks the chat model to output a bid to speak
        """

        prompt = PromptTemplate(
            input_variables=["message_history", "recent_message"],
            template=self.bidding_template
        ).format(
            message_history="\n".join(self.message_history),
            recent_message=self.message_history[-1],
        )
        bid_string = self.model([SystemMessage(content=prompt)]).content
        
        return bid_string
