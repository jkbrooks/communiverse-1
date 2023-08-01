from langchain.schema import (
    HumanMessage,
    SystemMessage)
from langchain.chat_models import ChatOpenAI

from typing import Any

from workspace.settings import CHARACTER_DESCRIPTION_TEMPLATE, CHARACTER_HEADER_TEMPLATE,\
                        SYSTEM_MESSAGE_TEMPLATE


class CharacterGenerator():
    def __init__(self, character_names: list, topic: str, word_limit:int, 
                 player_descriptor_system_message: SystemMessage, 
                 game_description: str) -> None:
        
        self.character_names = character_names
        self.topic = topic
        self.word_limit = word_limit

        self.player_descriptor_system_message = player_descriptor_system_message
        self.game_description = game_description

        self.character_descriptions = []
        self.character_headers = []
        self.character_system_messages = []
    
    def generate_character_description(self, llm: Any = ChatOpenAI):
        for character_name in self.character_names:

            character_specifier_prompt = [
                self.player_descriptor_system_message,
                HumanMessage(
                    content=CHARACTER_DESCRIPTION_TEMPLATE.format(
                        character_name=character_name,
                        word_limit=self.word_limit
                    )
                ),
            ]
            character_description = llm(temperature=1.0)(
                character_specifier_prompt
            ).content
            self.character_descriptions.append(character_description)
    
    def generate_character_header(self):
        for i in range(len(self.character_names)):

            self.character_headers.append(CHARACTER_HEADER_TEMPLATE.format(
                        character_name=self.character_names[i],
                        game_description=self.game_description,
                        character_description = self.character_descriptions[i]
                    ))
    
    def generate_character_system_message(self):
        for i in range(len(self.character_names)):
            
            self.character_system_messages.append(SystemMessage(
                content=(SYSTEM_MESSAGE_TEMPLATE.format(
                        character_name=self.character_names[i],
                        word_limit=self.word_limit,
                        character_header = self.character_headers[i]
                    )
                )
            ))

    