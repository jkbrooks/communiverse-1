from langchain.schema import (
    HumanMessage,
    SystemMessage)
from langchain.chat_models import ChatOpenAI

from typing import Any

# from workspace.settings import AGENT_DESCRIPTION_TEMPLATE, AGENT_HEADER_TEMPLATE,\
#                         SYSTEM_MESSAGE_TEMPLATE


# class AgentGenerator():
#     def __init__(self, agent_names: list, topic: str, word_limit:int, 
#                  agent_descriptor_system_message: SystemMessage, 
#                  chat_description: str) -> None:
        
#         self.agent_names = agent_names
#         self.topic = topic
#         self.word_limit = word_limit

#         self.agent_descriptor_system_message = agent_descriptor_system_message
#         self.chat_description = chat_description

#         self.agent_descriptions = []
#         self.agent_headers = []
#         self.agent_system_messages = []
    
#     def generate_agent_description(self, llm: Any = ChatOpenAI):
#         for agent_name in self.agent_names:

#             agent_specifier_prompt = [
#                 self.agent_descriptor_system_message,
#                 HumanMessage(
#                     content=AGENT_DESCRIPTION_TEMPLATE.format(
#                         agent_name=agent_name,
#                         word_limit=self.word_limit
#                     )
#                 ),
#             ]
#             agent_description = llm(temperature=1.0)(
#                 agent_specifier_prompt
#             ).content
#             self.agent_descriptions.append(agent_description)
    
#     def generate_agent_header(self):
#         for i in range(len(self.agent_names)):

#             self.agent_headers.append(AGENT_HEADER_TEMPLATE.format(
#                         agent_name=self.agent_names[i],
#                         agent_description = self.agent_descriptions[i]
#                     ))
    
#     def generate_agent_system_message(self):
#         for i in range(len(self.agent_names)):
            
#             self.agent_system_messages.append(SystemMessage(
#                 content=(SYSTEM_MESSAGE_TEMPLATE.format(
#                         agent_name=self.agent_names[i],
#                         word_limit=self.word_limit,
#                         agent_header = self.agent_headers[i]
#                     )
#                 )
#             ))
    
    